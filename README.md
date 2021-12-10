# Telegram Bot : Whale Watcher

#### A straightforward telegram bot written in python to track whales activity on multiple blockchains, using [whale-alert API](https://docs.whale-alert.io/)

## Installation
#### 

### 1. Telegram Bot
First, you need to read the documentation on telegram bot, and create one : 
[telegram bot docs](https://core.telegram.org/bots).
Once you own a bot and you have securely stored his token, you can go to the next step!

### 2. Whale-alert API key
Once you have your bot, you need to be able to connect the to whale-alert api using one of the token they provide.
You will find all the required informations here to get 
your api key : [whale-alert authentication](https://docs.whale-alert.io/#authentication).

There is different pricing plans, the bot is well adapted for the free one with the base config.

### 3. Running the bot!
To run the bot, you'll need to either have python 3.9.7 already installed, 
or install using a virtual environment (recommended) 
with [pyenv](https://github.com/pyenv/pyenv) & [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv):

Go into the main folder, and simply run : 
```
pyenv install 3.9.7
pyenv virtualenv 3.9.7 whale_alert_bot
pyenv activate whale_alert_bot
```


Go into the main folder, and simply run : 
```
pip install -r requirements.txt
```

Finally, run the main script to run the bot, along with your tokens allocated to the right environment variables:
```
WHALE_ALERT_API_KEY=YOUR-TOKEN TELEGRAM_BOT_TOKEN=YOUR_TOKEN python src/bots/watcher_bot.py
```

Or add the environment variables to a `.env` file, within the same folder as the `settings.py` file (recommended).
They will be imported automatically while running the bot.

### 4. The environment variables

As we have seen previously, the bot can be personalised thanks to a bunch of environment variables to set in your .env 
file:
```
TRANSACTION_ENDPOINT
```
The endpoint to fetch transactions, defaults to the current on in whale-alert.
```
STATUS_ENDPOINT
```
The endpoint to fetch connection to blockchain statuses, defaults to the current on in whale-alert.
```
API_KEY
```
Your whale-alert API key. This is required.
```
TELEGRAM_BOT_KEY
```
Your telegram bot key. This is required.
```
MIN_INTERVAL
```
Minimum interval (in seconds) for which we want to allow the transaction alerts. Defaults to 15.
```
HISTORY_TIME_LIMIT
```
Maximum interval (in seconds) for which we want to allow the transaction alerts. 
Defaults to 3600 (free whale alert plan).

```
TX_VALUE_USD_THRESHOLD
```
Minimum value of the transactions we want to track (USD). Defaults to 500 000.
```
CURRENCY_WATCHED
```
Currency to watch. Default to None (all of them)
```
TX_ROWS_LIMIT
```
Limit amount of transactions per alert. Defaults to 100.

## Usage
#### 

### 1. Helpers
Once your bot is running, just like the normals bots, 
you can get more details about the commands with the following commands:
```
/help
/start
```

### 2. Status Checker
This command allows you to precisely check the status of the connection of 
whale-alert to the different blockchains it's monitoring.
```
/check_status <optional: data_keys>
```

The data_keys are arguments representing the specific data you want to fetch from the
[whale-alert blockchains status](https://docs.whale-alert.io/#status). Without this argument, all of them are returned.

##### Example : 
```
/check_status status name
```
Will only return the status and the name of each connected blockchain, in the payload.

### 3. Transaction watcher
This is the main command of the bot : it's monitoring the transactions on the blockchains and gives you an alert
of the statuses every `dt` seconds.

```
/watcher_timer seconds minutes <optional: data_keys>
```
Seconds and minutes are describing the interval between each alert sent by the bot.
(Max. 1h with the free version of the whale-alert API).

data_keys, are, like previously, the data you want to filter out in the `transactions` payload of the response.

##### Example : 
```
/watcher_timer 20 0 amount_usd symbol blockchain
```

Will give you an alert every 20 seconds of all the big transactions, 
only returning you the given arguments from the payload described [here](https://docs.whale-alert.io/#transactions)

### 4. Upcoming
More detailed commands and more commands in development :)