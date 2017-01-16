from constants import *

ANIME_LIST_ENDPOINT = 'AnimeList'
ANIME_LIST_POPULAR = ANIME_LIST_ENDPOINT + '/MostPopular'
ANIME_LIST_LATEST = ANIME_LIST_ENDPOINT + '/LatestUpdate'
ANIME_LIST_NEWEST = ANIME_LIST_ENDPOINT + '/Newest'

ANIME_LIST_FILTER_MAP = {
    SORT_ALPHABETICALLY_ACTION: ANIME_LIST_ENDPOINT,
    SORT_BY_POPULAR_ACTION: ANIME_LIST_POPULAR,
    LATEST_UPDATE_ACTION: ANIME_LIST_LATEST,
    NEW_ANIME_ACTION: ANIME_LIST_NEWEST
}

UPCOMING_ANIME = 'UpcomingAnime'

ANIME_SEARCH_ENDPOINT = 'Search/Anime'