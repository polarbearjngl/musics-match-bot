import os
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from bot import Callbacks
from bot.handlers import call_handler, start, message_received

# get variables from heroku environment vars
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", "8443"))
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
# set logging level
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def run(updater_instance):
    updater_instance.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater_instance.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))


if __name__ == '__main__':
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler(Callbacks.START, callback=start, pass_user_data=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=call_handler, pass_user_data=True))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_received, pass_user_data=True))

    run(updater)
