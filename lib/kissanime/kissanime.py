import sys
import urlparse
import urllib
import xbmc
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
        self.typeParam = args.get('type', 'None')
        if self.typeParam is not None:
            print self.typeParam[0]
        self.urlParam = args.get('url', None)
    # End init

    def run(self):
        if self.typeParam[0] == ALL_VIDEOS_ACTION:
            self.allVideoLinks()
        elif self.typeParam[0] == EPISODES_ACTION:
            self.episodeLinks(self.urlParam[0])
        elif self.typeParam[0] == VIDEO_ACTION:
            self.playVideo(self.urlParam[0])
        else:
            self.buildMainMenu()
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
            params = self.generateParamsObj(VIDEO_ACTION, videoLinkUrl)
            url = BASE_APP_URL + '?' + urllib.urlencode(params)
            li = xbmcgui.ListItem(videoLinkText, iconImage='DefaultVideo.jpg')
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)
        # End for

        xbmcplugin.endOfDirectory(ADDON_HANDLE)
    # End episodeLinks

    def playVideo(self, url):
        videoReturn = self.scraper.video(url)

        play_item = xbmcgui.ListItem(path=videoReturn)
        xbmc.Player().play(videoReturn, play_item)
        #xbmcplugin.setResolvedUrl(__handle__, True, listitem=play_item)
    # End playVideo

    def generateParamsObj(self, urlType, url):
        return { 'type': urlType, 'url': url }
    # End generateParamsObj
# End KissAnime
