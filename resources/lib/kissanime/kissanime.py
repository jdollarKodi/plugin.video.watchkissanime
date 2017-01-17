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

## Main class for the plugin.
#
# Handles generating the menus and delegating to scraper functions
# to pull data from the kissanime.ru website
class KissAnime:

    ## Constructor for KissAnime
    #
    # Specifies the content that is plugin will be providing, parses the
    # arguments passed into the plugin into class variables and generates
    # a new instance of the scraper that this class will be using to pull
    # video information from
    def __init__(self):
        xbmcplugin.setContent(ADDON_HANDLE, CONTENT_TYPE_MOVIES)
        args = urlparse.parse_qs(sys.argv[2][1:])

        self.scraper = KissAnimeScrape()
        self.typeParam = args.get('type', [None])
        self.urlParam = args.get('url', [None])
        self.filter = args.get('filter', [SORT_ALPHABETICALLY_ACTION])

    ## Router to generate menu items based on the type argument passed into
    # the plugin
    def run(self):
        self.route()

    def route(self):
        if self.typeParam[0] == FILTER_ALL_ACTION:
            self.filterAll()
        elif self.typeParam[0] == ALL_VIDEOS_ACTION:
            url = self.urlParam[0]
            self.allVideoLinks(url)
        elif self.typeParam[0] == EPISODES_ACTION:
            self.episodeLinks(self.urlParam[0])
        elif self.typeParam[0] == VIDEO_ACTION:
            self.playVideo(self.urlParam[0])
        elif self.typeParam[0] == SEARCH_ACTION:
            self.search()
        else:
            self.buildMainMenu()

    ## Builds out the main menu for the starting point of the addon
    #
    # Generates menu items for the main menu of the application. Menu
    # Items are defined in the constants file
    def buildMainMenu(self):
        for menuItemKey, menuItemValue in MAIN_MENU_ITEMS.items():
            url = self.generateUrl(menuItemKey)
            li = xbmcgui.ListItem(menuItemValue, iconImage=DEFAULT_VIDEO_IMAGE)
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(ADDON_HANDLE, updateListing=True)

    ## Builds out a menu for when the user specifies they want to view all
    #  available animes
    def allVideoLinks(self, urlParam=None):
        allReturn = self.scraper.all(urlParam, {'filter': self.filter[0]})
        videoLinks = allReturn['links']
        for videoLinkUrl, videoLinkObj in videoLinks.items():
            urlAction = ALL_VIDEOS_ACTION if videoLinkObj['type'] != ITEM_TYPE else EPISODES_ACTION
            url = self.generateUrl(urlAction, videoLinkUrl)
            li = xbmcgui.ListItem(videoLinkObj['name'])
            li.setArt({'icon': videoLinkObj['image']})
            li.setInfo(type='video', infoLabels={'plot': videoLinkObj['description']})
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(ADDON_HANDLE, cacheToDisc=True)

    def filterAll(self):
        dialog = xbmcgui.Dialog()
        selectorPosition = dialog.select('Select', ANIME_LIST_SELECTOR)
        if selectorPosition >= 0:
            allFilter = ANIME_LIST_SELECTOR_MAP[ANIME_LIST_SELECTOR[selectorPosition]]
            self.filter = [allFilter]
            # Really would like to do this, but can't. Container Update calls plugin twice.
            # Prevents users from scrolling up a directory
            #
            # allVideosUrl = '{}/?type={}&filter={}'.format(BASE_APP_URL, ALL_VIDEOS_ACTION, allFilter)
            # containerUpdateCommand = 'Container.Update({}, "{}")'.format(allVideosUrl, 'replace')
            # xbmc.executebuiltin(containerUpdateCommand)

        self.allVideoLinks()

    ## Builds out a menu for when the user selects a anime to watch that will
    #  display all of the various episodes
    #
    #  @param url string url of the webpage that contains a list of the episodes
    def episodeLinks(self, url):
        episodeReturn = self.scraper.episodes(url)
        videoLinks = episodeReturn['links']
        for videoLinkUrl, videoLinkObj in videoLinks.items():
            url = self.generateUrl(VIDEO_ACTION, videoLinkUrl)
            li = xbmcgui.ListItem(videoLinkObj['name'], iconImage='DefaultVideo.jpg')
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=False)

        xbmcplugin.endOfDirectory(ADDON_HANDLE)

    def search(self):
        dialog = xbmcgui.Dialog()
        keywordInput = dialog.input(SEARCH_LABEL, type=xbmcgui.INPUT_ALPHANUM)
        print 'keyword: ' + keywordInput
        if keywordInput is None or keywordInput == '':
            return

        searchReturn = self.scraper.search(keywordInput)
        videoLinks = searchReturn['links']

        for videoLinkUrl, videoLinkObj in videoLinks.items():
            url = self.generateUrl(EPISODES_ACTION, videoLinkUrl)
            li = xbmcgui.ListItem(videoLinkObj['name'])
            li.setArt({'icon': videoLinkObj['image']})
            li.setInfo(type='video', infoLabels={'plot': videoLinkObj['description']})
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(ADDON_HANDLE)

    ## Plays the video url passed into this function
    #
    #  @param url string url of the video stream that kodi will start playing
    def playVideo(self, url):
        videoObj = self.scraper.video(url)
        videoUrl = videoObj['url']
        videoListItem = xbmcgui.ListItem(path=videoUrl)
        xbmc.Player().play(videoUrl, videoListItem)

    ## Helper function that generates a params object that contains a type
    #  and url value. Will be used to pass back into this plugin to tell the
    #  addon where the user is trying to navigate to
    #
    #  @param urlType string specifies what kind of url is being passed
    #                         and is a value the plugin will use to route
    #                         to new menus
    #  @param url string     specifies the url that contains content that a new
    #                        menu will scrape information from
    def generateUrl(self, urlType, url=None, filter=None):
        params = {}
        params['type'] = urlType

        if url:
            params['url'] = url

        if filter:
            params['filter'] = filter

        return self.generateUrlObj(params)

    def generateUrlObj(self, data):
        return BASE_APP_URL + '?' + urllib.urlencode(data)
