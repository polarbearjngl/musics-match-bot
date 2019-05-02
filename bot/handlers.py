# coding=utf-8
from telegram import InlineKeyboardMarkup, ParseMode
from bot import Callbacks
from bot.menu import Menu, MenuList
from bot.music_api import MusicMatch


def start(bot, update, user_data):
    """Handler that calling when user send /start"""
    user_data['state'] = None
    start_menu = Menu(buttons=MenuList.START, col_num=1).build_menu()
    reply_markup = InlineKeyboardMarkup(start_menu)
    update.message.reply_html(text=Callbacks.START_TEXT, reply_markup=reply_markup)


def call_handler(bot, update, user_data):
    """Handler that call method based on update.callback_query.data"""
    query = update.callback_query
    query_id = update.callback_query.id
    qdata = query.data
    message_id = query.message.message_id
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    user_data['chat_id'], user_data['user_id'] = chat_id, user_id

    # need for deleting bot message
    if user_data.get('msg_ids'):
        user_data['bot_msg_ids'].append(message_id)
    else:
        user_data['bot_msg_ids'] = []
        user_data['bot_msg_ids'].append(message_id)
    # building answer from bot with actions, if user chose search
    menu = Menu(buttons=MenuList.COUNT, col_num=3).build_menu(footer_buttons=MenuList.TO_START)
    reply_markup = InlineKeyboardMarkup(menu)

    if qdata == Callbacks.TRACK_SEARCH:
        user_data['state'] = Callbacks.TRACK_SEARCH
        _text = Callbacks.TRACK_SEARCH_TEXT

    elif qdata == Callbacks.ARTIST_SEARCH:
        user_data['state'] = Callbacks.ARTIST_SEARCH
        _text = Callbacks.ARTIST_SEARCH_TEXT

    elif qdata == Callbacks.LYRICS_SEARCH:
        user_data['state'] = Callbacks.LYRICS_SEARCH
        _text = Callbacks.LYRICS_SEARCH_TEXT

    elif qdata == Callbacks.START:
        user_data['state'] = None
        _text = Callbacks.START_TEXT
        # building answer from bot with actions, if user chose back to start
        start_menu = Menu(buttons=MenuList.START, col_num=1).build_menu()
        reply_markup = InlineKeyboardMarkup(start_menu)

    elif qdata in [Callbacks.TEN, Callbacks.TWENTY, Callbacks.THIRTY]:
        # notify user about changing count of items in search result
        bot.answerCallbackQuery(text=Callbacks.COUNT_OF_SEARCH.format(qdata), callback_query_id=query_id)
        user_data['count'] = int(qdata)

    user_data['count'] = user_data['count'] if user_data.get('count') else int(Callbacks.TEN)

    if qdata in [Callbacks.TRACK_SEARCH, Callbacks.ARTIST_SEARCH, Callbacks.LYRICS_SEARCH, Callbacks.START]:
        bot.editMessageText(message_id=message_id,
                            chat_id=chat_id,
                            text=_text,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup)
    elif qdata not in [Callbacks.TEN, Callbacks.TWENTY, Callbacks.THIRTY]:
        user_data['bot_msg_ids'].remove(message_id)


def message_received(bot, update, user_data):
    """Get text from user's message and try search with it"""
    text = update.effective_message.text
    music_match = MusicMatch()

    if user_data and user_data['state']:
        # send search request based on user_data['state']
        _text = ''.join(music_match.get_actions[str(user_data['state'])](text, count=user_data['count']))
        # send result of search to user
        update.message.reply_html(text=_text, disable_web_page_preview=True)
        # remove previous bot's menu and create new
        bot.deleteMessage(chat_id=user_data['chat_id'], message_id=user_data['bot_msg_ids'][-1])
        start(bot=bot, update=update, user_data=user_data)
        user_data['bot_msg_ids'].remove(user_data['bot_msg_ids'][-1])
