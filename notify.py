#!/usr/bin/env python3

import json
import telegram
from telegram.ext import Updater, CommandHandler
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import pynvml
import time

class NotifyBot:
    def __init__(self):
        super().__init__()

        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                token = config["token"]
                self._whitelist = config["whitelist"]
        except FileNotFoundError:
            print("You need to have a config.json file in this directory")
            exit(1)

        self._last_thresh = -1

        self._updater = Updater(token, use_context=True)
        dp = self._updater.dispatcher
        dp.add_handler(CommandHandler("start", self._register))
        dp.add_handler(CommandHandler("gpu", self._get_gpu))
        self._updater.start_polling()

        self._poll_gpu(5)

    def _register(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        if user_id not in self._whitelist:
            update.message.reply_text("You are not yet on the whitelist. " +
                f"Add {user_id} to your config to receive notifications from me")
        else:
            update.message.reply_text("Hi! I will notify you when someone starts " +
                "to use the GPU and when it's available again")

    def _get_gpu(self, update: Update, context: CallbackContext):
        print(update.message.from_user.username, "requested gpu usage")
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        used_mb = info.used / 1024 / 1024
        update.message.reply_text("{:.0f}MB is in use".format(used_mb))

    def _poll_gpu(self, interval):
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)

        while True:
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            used_mb = info.used / 1024 / 1024
            thresh = int(used_mb / 500) * 500
            if thresh != self._last_thresh:
                self._last_thresh = thresh
                msg = f"GPU usage is approximately {thresh} MB"
                print(msg)

                for chat_id in self._whitelist:
                    try:
                        self._updater.bot.send_message(chat_id, msg)
                    except telegram.error.Unauthorized:
                        print("Unauthorized for", chat_id)

            time.sleep(interval)

if __name__ == "__main__":
    NotifyBot()
