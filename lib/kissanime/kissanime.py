import sys
import urllib2
import xbmcplugin
import xbmcgui
import js2py
import cfscrape

from bs4 import BeautifulSoup
from t0mm0.common.net import Net

ADDON_HANDLE = int(sys.argv[1])
KISS_ANIME_BASE_URL = 'http://kissanime.ru/'
ANIME_LIST_ENDPOINT = 'AnimeList'

class KissAnime:
    def __init__(self):
        xbmcplugin.setContent(ADDON_HANDLE, 'movies')
    # End init

    def run(self):
        self.buildMainMenu()
    # End run

    def buildMainMenu(self):
        scraper = cfscrape.create_scraper()
        response = scraper.get(KISS_ANIME_BASE_URL + ANIME_LIST_ENDPOINT)
        soup = BeautifulSoup(response.content,'html.parser')
        listingObj = soup.find('table', { "class": "listing" })
        videoLinks = listingObj.find_all('a')
        for videoLink in videoLinks:
           li = xbmcgui.ListItem(videoLink.renderContents(), iconImage='DefaultVideo.jpg')
           xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=videoLink['href'], listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(ADDON_HANDLE)
    #End buildMainMenu
# End KissAnime
