from constants import *

ANIME_LIST = 'AnimeList'
ANIME_LIST_POPULAR = ANIME_LIST + '/MostPopular'
ANIME_LIST_LATEST = ANIME_LIST + '/LatestUpdate'
ANIME_LIST_NEWEST = ANIME_LIST + '/Newest'

ONGOING = 'Status/Ongoing'
ONGOING_POPULAR = ONGOING + '/MostPopular'
ONGOING_LATEST = ONGOING + '/LatestUpdate'
ONGOING_NEWEST = ONGOING + '/Newest'

COMPLETED = 'Status/Completed'
COMPLETED_POPULAR = COMPLETED + '/MostPopular'
COMPLETED_LATEST = COMPLETED + '/LatestUpdate'
COMPLETED_NEWEST = COMPLETED + '/Newest'

ANIME_SEARCH_ENDPOINT = 'Search/Anime'

UPCOMING_ANIME = 'UpcomingAnime'

ANIME_LIST_FILTER_MAP = {
    SORT_ALPHABETICALLY_ACTION: ANIME_LIST,
    SORT_BY_POPULAR_ACTION: ANIME_LIST_POPULAR,
    LATEST_UPDATE_ACTION: ANIME_LIST_LATEST,
    NEW_ANIME_ACTION: ANIME_LIST_NEWEST
}

ONGOING_FILTER_MAP = {
    SORT_ALPHABETICALLY_ACTION: ONGOING,
    SORT_BY_POPULAR_ACTION: ONGOING_POPULAR,
    LATEST_UPDATE_ACTION: ONGOING_LATEST,
    NEW_ANIME_ACTION: ONGOING_NEWEST
}

COMPLETED_FILTER_MAP = {
    SORT_ALPHABETICALLY_ACTION: COMPLETED,
    SORT_BY_POPULAR_ACTION: COMPLETED_POPULAR,
    LATEST_UPDATE_ACTION: COMPLETED_LATEST,
    NEW_ANIME_ACTION: COMPLETED_NEWEST
}
