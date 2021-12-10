import os

from dotenv import load_dotenv

load_dotenv()

TRANSACTION_ENDPOINT = os.getenv(
    'WHALE_ALERT_TRANSACTION_ENDPOINT',
    default='https://api.whale-alert.io/v1/transactions'
)
STATUS_ENDPOINT = os.getenv(
    'WHALE_ALERT_TRANSACTION_ENDPOINT',
    default='https://api.whale-alert.io/v1/status'
)
API_KEY = os.getenv('WHALE_ALERT_API_KEY', 'token')
TELEGRAM_BOT_KEY = os.getenv('TELEGRAM_BOT_TOKEN', 'token')
MIN_INTERVAL = os.getenv('WHALE_ALERT_MINIMUM_INTERVAL', 15)
HISTORY_TIME_LIMIT = os.getenv('WHALE_ALERT_TIME_LIMIT', 3600)  # Limit time boundary to fetch transactions data
TX_VALUE_USD_THRESHOLD = os.getenv('TX_VALUE_USD_THRESHOLD', 500000)
CURRENCY_WATCHED = os.getenv('CURRENCY_WATCHED')
TX_ROWS_LIMIT = os.getenv('TX_ROWS_LIMIT', 100)
