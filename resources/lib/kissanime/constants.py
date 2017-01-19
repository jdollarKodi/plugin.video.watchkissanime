import sys
import xbmc
import xbmcaddon
from collections import OrderedDict

ADDON_HANDLE = int(sys.argv[1])
BASE_APP_URL = sys.argv[0][:-1]

ADDON = xbmcaddon.Addon()
LAST_SEARCH_FILE = xbmc.translatePath( 'special://temp/' + ADDON.getAddonInfo('id') + '.lastSearch' ).decode("utf-8")

DEFAULT_VIDEO_IMAGE = 'DefaultVideo.png'
CONTENT_TYPE_MOVIES = 'movies'

ALL_SCRAPE_TYPE = 'all'
EPISODE_SCRAPE_TYPE = 'episode'
VIDEO_SCRAPE_TYPE = 'video'
SEARCH_SCRAPE_TYPE = 'search'
ONGOING_SCRAPE_TYPE = 'ongoing'
COMPLETED_SCRAPE_TYPE = 'completed'
NEW_AND_HOT_SCRAPE_TYPE = 'newandhot'

LIST_TYPE_DIR = 'directory'
ITEM_TYPE = 'item'
PAGE_TYPE = 'page'

LIST_ALL_ANIME_LABEL = 'List All Anime'
SEARCH_LABEL = 'Search'
NEXT_LABEL = 'Next Page'
PREV_LABEL = 'Previous Page'
SORT_ALPHABETICALLY_LABEL = 'Sort alphabetically'
SORT_BY_POPULAR_LABEL = 'Sort by popularity'
LATEST_UPDATE_LABEL = 'Latest update'
NEW_ANIME_LABEL = 'New anime'
UPCOMING_ANIME_LABEL = 'Upcoming anime'
ONGOING_LABEL = 'Ongoing'
COMPLETED_LABEL = 'Completed'
NEW_AND_HOT_LABEL = 'New and Hot'
SETTINGS_LABEL = 'Settings'

PAGE_ACTION = 'page'
FILTER_ALL_ACTION = 'filterAll'
FILTER_ONGOING_ACTION = 'filterOngoing'
FILTER_COMPLETED_ACTION = 'filterCompleted'
ALL_VIDEOS_ACTION = 'allVideos'
SEARCH_ACTION = 'search'
EPISODES_ACTION = 'episode'
VIDEO_ACTION = 'video'
UPCOMING_ANIME_ACTION = 'upcomingAnime'
ONGOING_ACTION = 'ongoing'
COMPLETED_ACTION = 'completed'
NEW_AND_HOT_ACTION = 'newandhot'
SETTINGS_ACTION = 'settings'

SORT_ALPHABETICALLY_ACTION = 'alphabetically'
SORT_BY_POPULAR_ACTION = 'popularity'
LATEST_UPDATE_ACTION = 'latestUpdate'
NEW_ANIME_ACTION = 'newAnime'


ANIME_LIST_SELECTOR = [
    SORT_ALPHABETICALLY_LABEL,
    SORT_BY_POPULAR_LABEL,
    LATEST_UPDATE_LABEL,
    NEW_ANIME_LABEL,
    #UPCOMING_ANIME_LABEL
]

ANIME_LIST_SELECTOR_MAP = {
    SORT_ALPHABETICALLY_LABEL: SORT_ALPHABETICALLY_ACTION,
    SORT_BY_POPULAR_LABEL: SORT_BY_POPULAR_ACTION,
    LATEST_UPDATE_LABEL: LATEST_UPDATE_ACTION,
    NEW_ANIME_LABEL: NEW_ANIME_ACTION,
    #UPCOMING_ANIME_LABEL: UPCOMING_ANIME_ACTION
}

MAIN_MENU_ITEMS = OrderedDict(
    [
        (FILTER_ALL_ACTION, LIST_ALL_ANIME_LABEL),
        (FILTER_ONGOING_ACTION, ONGOING_LABEL),
        (FILTER_COMPLETED_ACTION, COMPLETED_LABEL),
        (NEW_AND_HOT_ACTION, NEW_AND_HOT_LABEL),
        (SEARCH_ACTION, SEARCH_LABEL),
        (SETTINGS_ACTION, SETTINGS_LABEL)
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
