Get notifications via Telegram when your nvidia GPU is available again.

## How it works

+ If memory usage of the GPU drops below 200MB, you will get a message "The GPU is available"
+ If memory usage of the GPU goes above 500MB, you will get a message "The GPU is in use"

If you want to know the current memory usage of the GPU, send `/gpu` to the bot and it will respond you with a message like "9376MB is in use"

## Setup

Run

    pipenv install

to install the required packages. Alternatively you can manually install the packages from the `[packages]` section in the Pipfile using pip.

Next, you have to create a `config.json` file in this directory containing the bot token and a list of user ids that the bot should send messages to:

```json
{
    "token": "1008150085:AAHea1JBSof0yEVRrHfkbL2W_fDg9xEs-bE",
    "whitelist": [
        123456789,
        987654321
    ]
}
```

If you don't know how to set up a bot or get the bot token, take a look at https://core.telegram.org/bots

If you start a chat with the bot and your user id is not listed in the whitelist, the bot will tell you:

> You are not yet on the whitelist. Add 987654321 to your config to receive notifications from me
