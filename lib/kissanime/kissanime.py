import sys
import urlparse
import urllib
import xbmcplugin
import xbmcgui

from scraper import KissAnimeScrape
import cfscrape
from bs4 import BeautifulSoup
from constants import *

ADDON_HANDLE = int(sys.argv[1])

class KissAnime:
    def __init__(self):
        xbmcplugin.setContent(ADDON_HANDLE, CONTENT_TYPE_MOVIES)
        args = urlparse.parse_qs(sys.argv[2][1:])

        self.scraper = KissAnimeScrape()
        self.typeParam = args.get('type', None)
        self.urlParam = args.get('url', None)
    # End init

    def run(self):
        if self.typeParam is None:
            self.buildMainMenu()
        elif self.typeParam[0] == ALL_VIDEOS_ACTION:
            self.allVideoLinks()
        elif self.typeParam[0] == EPISODES_ACTION:
            self.episodeLinks(self.urlParam[0])
    # End run

    def buildMainMenu(self):
        for menuItemKey, menuItemValue in MAIN_MENU_ITEMS.items():
            #url = UrlUtil().buildUrl({TYPE_PARAM:menuItemValue})
            url = BASE_APP_URL + '?' + urllib.urlencode({'type': menuItemKey})
            li = xbmcgui.ListItem(menuItemValue, iconImage=DEFAULT_VIDEO_IMAGE)
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(ADDON_HANDLE)
    #End buildMainMenu

    def allVideoLinks(self):
        allReturn = self.scraper.all()
        videoLinks = allReturn['links']
        for videoLinkUrl, videoLinkText in videoLinks.items():
            params = {'type': EPISODES_ACTION, 'url': videoLinkUrl}
            url = BASE_APP_URL + '?' + urllib.urlencode(params)
            li = xbmcgui.ListItem(videoLinkText, iconImage='DefaultVideo.jpg')
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)
        # End for

        xbmcplugin.endOfDirectory(ADDON_HANDLE)
    # End generateVideoLinks

    def episodeLinks(self, url):
        episodeReturn = self.scraper.episodes(url)
        videoLinks = episodeReturn['links']
        for videoLinkUrl, videoLinkText in videoLinks.items():
            params = {'type': EPISODES_ACTION, 'url': videoLinkUrl}
            url = BASE_APP_URL + '?' + urllib.urlencode(params)
            li = xbmcgui.ListItem(videoLinkText, iconImage='DefaultVideo.jpg')
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=videoLinkUrl, listitem=li, isFolder=True)
        # End for

        xbmcplugin.endOfDirectory(ADDON_HANDLE)
    # End episodeLinks
# End KissAnime
