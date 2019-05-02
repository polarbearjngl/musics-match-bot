from emoji import emojize


class Callbacks(object):
    """Class for storing callback commands and constant text."""

    START = 'start'
    TRACK_SEARCH = 'track_search'
    ARTIST_SEARCH = 'artist_search'
    LYRICS_SEARCH = 'lyrics_search'
    TEN = '10'
    TWENTY = '20'
    THIRTY = '30'

    START_TEXT = emojize(":notes: Выберите одно из возможных действий :notes:", use_aliases=True)
    TRACK_SEARCH_TEXT = emojize("Введите название трека и отправьте его Боту :robot_face:\n", use_aliases=True)
    ARTIST_SEARCH_TEXT = emojize("Введите имя Исполнителя и отправьте его Боту :robot_face:\n", use_aliases=True)
    LYRICS_SEARCH_TEXT = emojize("Введите строчку из песни и отправьте ее Боту :robot_face:\n", use_aliases=True)
    COUNT_OF_SEARCH = "Количество результатов поиска - {}"
