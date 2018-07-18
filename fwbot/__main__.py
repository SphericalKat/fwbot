from fwbot import dispatcher, updater, TOKEN, LOGGER
from telegram import Message, Chat, Update, Bot, User, ParseMode
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async
import requests, datetime, json, urllib

@run_async
def forward_message(bot: Bot, update: Update):
	send = "Devices to be built today are:\n"
	dow = int(datetime.datetime.today().weekday() + 1)
	devices = json.loads(urllib.request.urlopen("https://raw.githubusercontent.com/FireHound/jenkins/o8.1/build-targets.json").read().decode())
	for device in devices:
		if int(device.get("dow")) == dow:
			send = send + "*" + str(device.get("device"))+ "*" + "\n"

	update.effective_message.reply_text(send, parse_mode=ParseMode.MARKDOWN)

def start(bot, update):
	update.effective_message.reply_text("Yo, whadup")

def main():
	start_handler = CommandHandler ("start", start)
	FORWARD_HANDLER = CommandHandler("devices", forward_message)
	dispatcher.add_handler(FORWARD_HANDLER)
	dispatcher.add_handler(start_handler)

	LOGGER.info("Using long polling.")
	updater.start_polling(timeout=15, read_latency=4)

	updater.idle()

if __name__ == '__main__':
	LOGGER.info("Successfully started bot.")
	main()
