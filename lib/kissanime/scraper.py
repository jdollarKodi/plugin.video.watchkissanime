import cfscrape
import re
from constants import *

from bs4 import BeautifulSoup

from collections import OrderedDict

class KissAnimeScrape:
    BASE_URL = 'http://kissanime.ru/'
    ANIME_LIST_ENDPOINT = 'AnimeList'

    def __init__(self):
        self.scraper = cfscrape.create_scraper()
    # End init

    def all(self):
        scrapeUrl = KissAnimeScrape.BASE_URL + KissAnimeScrape.ANIME_LIST_ENDPOINT
        response = self.scraper.get(scrapeUrl)
        videoLinks = self.getLinksFromListingObject(response)

        return {
            'links': videoLinks,
            'type': LIST_TYPE_DIR
        }
    # End all

    def episodes(self, episodesEndpoint):
        scrapeUrl = KissAnimeScrape.BASE_URL + episodesEndpoint
        response = self.scraper.get(scrapeUrl)
        videoLinks = self.getLinksFromListingObject(response)

        return {
            'links': videoLinks,
            'type': LIST_TYPE_DIR
        }
    # End episodes

    def addPageLinks(self, soup, links):
        nextLink = soup.find('a', text=re.compile('Next'), attrs={'page':True})
        if nextLink is not None:
            links[nextLink['href']] = 'Next Page'

        prevLink = soup.find('a', text=re.compile('Prev'), attrs={'page':True})
        if prevLink is not None:
            links[prevLink['href']] = 'Previous Page'

        return links
    # End addPageLinks

    def getLinksFromListingObject(self, response):
        soup = BeautifulSoup(response.content,'html.parser')
        listingObj = soup.find('table', { "class": "listing" })
        tableRows = listingObj.find_all('tr')
        videoLinks = OrderedDict()

        for tableRow in tableRows:
            if tableRow.td is not None:
                anchor = tableRow.td.a
                print anchor
                videoLinks[anchor['href']] = anchor.string.strip()
            # End if
        # End for

        videoLinks = self.addPageLinks(soup, videoLinks)

        return videoLinks
    #End getLinksFromListingObject

#End KissAnimeScrape
