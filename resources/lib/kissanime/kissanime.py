import sys
import urlparse
import urllib
import xbmc
import xbmcplugin
import xbmcgui

from scraper import KissAnimeScrape
from guiutil import GuiUtil
import cfscrape
from bs4 import BeautifulSoup
from constants import *

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

        self.typeParam = args.get('type', [None])
        self.urlParam = args.get('url', [None])
        self.filter = args.get('filter', [SORT_ALPHABETICALLY_ACTION])

    ## Router to generate menu items based on the type argument passed into
    # the plugin
    def run(self):
        self.route()

    def route(self):
        if self.typeParam[0] == FILTER_ALL_ACTION:
            self.filterSort(ALL_SCRAPE_TYPE, EPISODES_ACTION, self.animeListScrape)
        elif self.typeParam[0] == FILTER_ONGOING_ACTION:
            self.filterSort(ONGOING_SCRAPE_TYPE, EPISODES_ACTION, self.animeListScrape)
        elif self.typeParam[0] == FILTER_COMPLETED_ACTION:
            self.filterSort(COMPLETED_SCRAPE_TYPE, EPISODES_ACTION, self.animeListScrape)
        elif self.typeParam[0] == ALL_VIDEOS_ACTION:
            url = self.urlParam[0]
            self.animeListScrape(url, ALL_SCRAPE_TYPE, EPISODES_ACTION)
        elif self.typeParam[0] == EPISODES_ACTION:
            self.episodeLinks(self.urlParam[0])
        elif self.typeParam[0] == VIDEO_ACTION:
            self.playVideo(self.urlParam[0])
        elif self.typeParam[0] == ONGOING_ACTION:
            self.ongoing(self.urlParam[0])
        elif self.typeParam[0] == COMPLETED_ACTION:
            self.completed(self.urlParam[0])
        elif self.typeParam[0] == SEARCH_ACTION:
            self.search()
        else:
            self.buildMainMenu()

    ## Builds out the main menu for the starting point of the addon
    #
    # Generates menu items for the main menu of the application. Menu
    # Items are defined in the constants file
    def buildMainMenu(self):
        GuiUtil.mainMenu(MAIN_MENU_ITEMS)

    def animeListScrape(self, urlParam=None, scrapeType=ALL_SCRAPE_TYPE, action=EPISODES_ACTION):
        scrapeParams = {
            'scrapeType': scrapeType,
            'url': urlParam,
            'data': {'filter': self.filter[0]}
        }
        scrapeResults = KissAnimeScrape.scrape(scrapeParams)
        videoLinks = scrapeResults['links']
        GuiUtil.list(videoLinks, action)

    def filterSort(self, scrapeType, action, callback):
        filterChoice = self.getUserFilterChoice()
        if filterChoice: callback(scrapeType=scrapeType, action=action)

    def getUserFilterChoice(self):
        dialog = xbmcgui.Dialog()
        selectorPosition = dialog.select('Select', ANIME_LIST_SELECTOR)
        filterChoice = None
        if selectorPosition >= 0:
            filterChoice = ANIME_LIST_SELECTOR_MAP[ANIME_LIST_SELECTOR[selectorPosition]]
            self.filter = [filterChoice]
            # Really would like to do this, but can't. Container Update calls plugin twice.
            # Prevents users from scrolling up a directory
            #
            # allVideosUrl = '{}/?type={}&filter={}'.format(BASE_APP_URL, ALL_VIDEOS_ACTION, allFilter)
            # containerUpdateCommand = 'Container.Update({}, "{}")'.format(allVideosUrl, 'replace')
            # xbmc.executebuiltin(containerUpdateCommand)

        return filterChoice

    ## Builds out a menu for when the user selects a anime to watch that will
    #  display all of the various episodes
    #
    #  @param url string url of the webpage that contains a list of the episodes
    def episodeLinks(self, url):
        scrapeParams = { 'scrapeType': EPISODE_SCRAPE_TYPE, 'url': url }
        episodeReturn = KissAnimeScrape.scrape(scrapeParams)
        videoLinks = episodeReturn['links']
        GuiUtil.list(videoLinks, VIDEO_ACTION, False)

    def search(self):
        dialog = xbmcgui.Dialog()
        keywordInput = dialog.input(SEARCH_LABEL, type=xbmcgui.INPUT_ALPHANUM)
        print 'keyword: ' + keywordInput
        if keywordInput is None or keywordInput == '':
            return

        scrapeParams = { 'scrapeType': SEARCH_SCRAPE_TYPE, 'keyword': keywordInput }
        searchReturn = KissAnimeScrape.scrape(scrapeParams)
        videoLinks = searchReturn['links']
        GuiUtil.list(videoLinks, EPISODES_ACTION)

    ## Plays the video url passed into this function
    #
    #  @param url string url of the video stream that kodi will start playing
    def playVideo(self, url):
        scrapeParams = { 'scrapeType': VIDEO_SCRAPE_TYPE, 'url': url }
        videoObj = KissAnimeScrape.scrape(scrapeParams)
        videoUrl = videoObj['url']
        videoListItem = xbmcgui.ListItem(path=videoUrl)
        xbmc.Player().play(videoUrl, videoListItem)
