from fwbot import dispatcher, updater, TOKEN, LOGGER, FROM_CHAT, TO_CHAT
from telegram import Message, Chat, Update, Bot, User
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async

@run_async
def forward_message(bot: Bot, update: Update):
	message = update.effective_message
	try:
		message.forward(int(TO_CHAT))
	except BadRequest as excp:
		LOGGER.info(excp.message)


def main():
	FORWARD_HANDLER = MessageHandler(Filters.chat(int(FROM_CHAT)), forward_message)
	dispatcher.add_handler(FORWARD_HANDLER)

	LOGGER.info("Using long polling.")
	updater.start_polling(timeout=15, read_latency=4)

	updater.idle()

if __name__ == '__main__':
	LOGGER.info("Successfully started bot.")
	main()
