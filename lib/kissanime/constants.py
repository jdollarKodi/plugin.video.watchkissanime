import sys
from collections import OrderedDict

BASE_APP_URL = sys.argv[0][:-1]
DEFAULT_VIDEO_IMAGE = 'DefaultVideo.jpg'

CONTENT_TYPE_MOVIES = 'movies'

LIST_TYPE_DIR = 'directory'
ITEM_TYPE = 'item'
PAGE_TYPE = 'page'

LIST_ALL_ANIME_LABEL = 'List All Anime'
SEARCH_LABEL = 'Search'
NEXT_LABEL = 'Next Page'
PREV_LABEL = 'Previous Page'

PAGE_ACTION = 'page'
ALL_VIDEOS_ACTION = 'allVideos'
SEARCH_ACTION = 'search'
EPISODES_ACTION = 'episode'
VIDEO_ACTION = 'video'

MAIN_MENU_ITEMS = OrderedDict(
    [
        (ALL_VIDEOS_ACTION, LIST_ALL_ANIME_LABEL),
        (SEARCH_ACTION, SEARCH_LABEL)
    ]
)

#Found through the loop in kissAnime's video link encoding
VIDEO_ENCRYPTION_LOOKUP = {
    '+': 62,
    '/': 63,
    '1': 53,
    '0': 52,
    '3': 55,
    '2': 54,
    '5': 57,
    '4': 56,
    '7': 59,
    '6': 58,
    '9': 61,
    '8': 60,
    '=': 64,
    'A': 0,
    'C': 2,
    'B': 1,
    'E': 4,
    'D': 3,
    'G': 6,
    'F': 5,
    'I': 8,
    'H': 7,
    'K': 10,
    'J': 9,
    'M': 12,
    'L': 11,
    'O': 14,
    'N': 13,
    'Q': 16,
    'P': 15,
    'S': 18,
    'R': 17,
    'U': 20,
    'T': 19,
    'W': 22,
    'V': 21,
    'Y': 24,
    'X': 23,
    'Z': 25,
    'a': 26,
    'c': 28,
    'b': 27,
    'e': 30,
    'd': 29,
    'g': 32,
    'f': 31,
    'i': 34,
    'h': 33,
    'k': 36,
    'j': 35,
    'm': 38,
    'l': 37,
    'o': 40,
    'n': 39,
    'q': 42,
    'p': 41,
    's': 44,
    'r': 43,
    'u': 46,
    't': 45,
    'w': 48,
    'v': 47,
    'y': 50,
    'x': 49,
    'z': 51
}
