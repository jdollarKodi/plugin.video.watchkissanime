import sys
from collections import OrderedDict

BASE_APP_URL = sys.argv[0][:-1]
DEFAULT_VIDEO_IMAGE = 'DefaultVideo.jpg'

KISS_ANIME_BASE_URL = 'http://kissanime.ru/'
ANIME_LIST_ENDPOINT = 'AnimeList'
CONTENT_TYPE_MOVIES = 'movies'

LIST_TYPE_VIDEO = 'video'
LIST_TYPE_DIR = 'directory'

LIST_ALL_ANIME_LABEL = 'List All Anime'
SEARCH_LABEL = 'Search'

ALL_VIDEOS_ACTION = 'allVideos'
SEARCH_ACTION = 'search'


MAIN_MENU_ITEMS = OrderedDict(
    [
        (ALL_VIDEOS_ACTION, LIST_ALL_ANIME_LABEL),
        (SEARCH_ACTION, SEARCH_LABEL)
    ]
)
