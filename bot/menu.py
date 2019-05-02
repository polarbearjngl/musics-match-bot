from telegram import InlineKeyboardButton
from bot import Callbacks


class Menu(object):
    """Class for creating inline menu for telegram"""

    def __init__(self, buttons, col_num):
        self.buttons = buttons
        self.col_num = col_num

    def build_menu(self, header_buttons=None, footer_buttons=None):
        """Generating array that used in inline menu creating"""
        menu = [self.buttons[i:i + self.col_num] for i in range(0, len(self.buttons), self.col_num)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu


class MenuList(object):
    """List of menu for this bot"""

    START = [InlineKeyboardButton(u"Поиск по Названию Трека", callback_data=Callbacks.TRACK_SEARCH),
             InlineKeyboardButton(u"Поиск по Имени Исполнителя", callback_data=Callbacks.ARTIST_SEARCH),
             InlineKeyboardButton(u"Поиск по строке из текста песни", callback_data=Callbacks.LYRICS_SEARCH)]

    TO_START = [InlineKeyboardButton(text=u"Вернуться к выбору действия", callback_data=Callbacks.START)]

    COUNT = [InlineKeyboardButton(text=u"10", callback_data=Callbacks.TEN),
             InlineKeyboardButton(text=u"20", callback_data=Callbacks.TWENTY),
             InlineKeyboardButton(text=u"30", callback_data=Callbacks.THIRTY)]
