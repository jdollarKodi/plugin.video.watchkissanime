import cfscrape

from resources.lib.Scraper import ListingParser
from resources.lib.kissanime.constants import *
from resources.lib.kissanime.endpoints import *

class KissAnimeScraper:
    def __init__(self):
        self.scraper = cfscrape.create_scraper()

    def scrapeAnimeList(self, pageUrl=None):
        response = self.scraper.get('http://kissanime.ru/' + ANIME_LIST)

        listingParser = ListingParser()
        return listingParser.parse(response.content)

    def scrapeCompletedList(self):
        return True

    def scrapeEpisodeList(self):
        return True

    def scrapeVideoLink(self):
        return True
