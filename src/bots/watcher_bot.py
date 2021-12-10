import logging
import time
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
)

from telegram.ext import (
    Updater,
    CommandHandler,
)
from requests_backend.request_backend import (
    TransactionsDataRequestBackend,
    ConnexionStatusBackend,
)
from settings import (
    API_KEY,
    TRANSACTION_ENDPOINT,
    TELEGRAM_BOT_KEY,
    HISTORY_TIME_LIMIT,
    MIN_INTERVAL,
    STATUS_ENDPOINT,
    TX_VALUE_USD_THRESHOLD,
    CURRENCY_WATCHED,
    TX_ROWS_LIMIT,
)
from result_parser import (
    CheckStatusParser,
    TransactionsDetailParser,
)

if TYPE_CHECKING:
    from telegram.ext import CallbackContext
    from telegram import Update

logger = logging.getLogger(__name__)


class TransactionFetcher:
    """
    Class allowing to fetch transaction data with the appropriate arguments passed to the command,
    defined in 'interval_time'.
    """
    def __init__(self, interval_time: int, passed_args: Optional[List[str]] = None):
        self.interval_time = interval_time
        self.passed_data_points = passed_args

    def __call__(self, context: 'CallbackContext', *args, **kwargs):
        return self.fetch_transaction_data(context)

    def fetch_transaction_data(self, context: 'CallbackContext') -> None:
        """
        Function called by the repeating job.
        Fetching transaction data from Whale Alert.
        """
        backend = TransactionsDataRequestBackend(
            TRANSACTION_ENDPOINT,
            API_KEY,
        )
        # The start date for the transaction data = now - interval_time (in seconds)
        start_date = str(int(time.time()) - int(self.interval_time))

        result = backend.fetch_transactions(
            start_date,
            min_value=TX_VALUE_USD_THRESHOLD,
            currency=CURRENCY_WATCHED,
            limit=TX_ROWS_LIMIT,
        )

        parser = TransactionsDetailParser(result, self.passed_data_points)
        text = parser.parse_response()

        job = context.job
        if parser.errors:
            for error in parser.errors:
                context.bot.send_message(job.context, text=error)
            return

        context.bot.send_message(job.context, text=text)


def start(update: 'Update', context: 'CallbackContext') -> None:
    """
    Start command. Indication on the usage of the bot.
    """
    update.message.reply_text(
        'Hi! Use /watcher_timer <seconds> <minutes> <data points> to set an interval between whale alert messages.'
        'Data points allow you to select only particular data in your transaction responses.'
        'Use /unwatch to disable the watcher.'
    )


def remove_job_if_exists(name: str, context: 'CallbackContext') -> bool:
    """
    Remove job with given name. Returns whether job was removed.
    """
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def watcher_timer(update: 'Update', context: 'CallbackContext') -> None:
    """
    Adds a new fetch_transaction_data job every 'interval_time' to the queue.
    """
    chat_id = update.message.chat_id
    passed_args = context.args
    if len(passed_args) < 2:
        update.message.reply_text(
            'Error: both of the time parameters have to be passed (0 as a possible value). '
            'Usage : /watcher_timer <seconds> <minutes> <data points>'
        )
        logger.info('Wrong input')
        return
    try:
        interval_time = int(passed_args.pop(0)) + int(passed_args.pop(0) * 60)
        if not MIN_INTERVAL <= interval_time < HISTORY_TIME_LIMIT:
            update.message.reply_text(
                f'Wrong interval given, the interval should be comprised '
                f'between {MIN_INTERVAL} and {HISTORY_TIME_LIMIT} seconds'
            )
            logger.info('Wrong interval time input')
            return

    except (IndexError, ValueError):
        update.message.reply_text('Error. Usage : /watcher_timer <seconds> <minutes> <data points>')
        logger.error(passed_args)
        return

    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_repeating(
        TransactionFetcher(interval_time, passed_args),
        interval_time,
        context=chat_id,
        name=str(chat_id)
    )

    text = 'Timer successfully set!'
    if job_removed:
        text += ' Old one was removed.'
    update.message.reply_text(text)


def unwatch(update: 'Update', context: 'CallbackContext') -> None:
    """
    Remove the job if the user changed their mind.
    """
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Watcher successfully disabled!' if job_removed else 'You have no active watcher.'
    update.message.reply_text(text)


def check_status(update: 'Update', context: 'CallbackContext') -> None:
    """
    Command to check the blockchain statuses.
    """
    backend = ConnexionStatusBackend(
        STATUS_ENDPOINT,
        API_KEY,
    )
    result = backend.check_status()
    parser = CheckStatusParser(result, context.args)
    text = parser.parse_response()
    if parser.errors:
        for error in parser.errors:
            update.message.reply_text(error)

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, text=text)


def main() -> None:
    """
    Function Registers the commands and runs watcher bot.
    """
    updater = Updater(TELEGRAM_BOT_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', start))
    dispatcher.add_handler(CommandHandler('watcher_timer', watcher_timer))
    dispatcher.add_handler(CommandHandler('unwatch', unwatch))
    dispatcher.add_handler(CommandHandler('check_status', check_status))

    # Start the Bot
    # TODO: Replace by WebHook for performance improvement
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
