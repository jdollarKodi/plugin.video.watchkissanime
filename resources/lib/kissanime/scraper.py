import cfscrape
import re
import sys
import urlresolver
from constants import *
from endpoints import *

from bs4 import BeautifulSoup

from collections import OrderedDict

## A class containing all of the scraping logic in order to extract
#  information from the kiss anime site
class KissAnimeScrape:
    ## Base URL/Host where the scraper will be pulling data from
    BASE_URL = 'http://kissanime.ru/'

    ANIME_IMAGE_REGEX = re.compile('src=\"(.*?)\"')
    ANIME_DESC_REGEX = re.compile('<p>(.*?)<\/p>', re.DOTALL)
    OPENLOAD_VIDEO_REGEX = re.compile('\"(http.*openload.*?)\"')
    GENRE_TITLE_REGEX = re.compile('genre')

    NEXT_RESPONSE_TEXT = 'Next'
    PREV_RESPONSE_TEXT = 'Prev'

    @staticmethod
    def scrape(data):
        scrapeType = data['scrapeType']
        scrapeData = {}

        if scrapeType == ALL_SCRAPE_TYPE:
            scrapeData = KissAnimeScrape.animeList(
                ANIME_LIST,
                ANIME_LIST_FILTER_MAP,
                KissAnimeScrape.commonParser,
                data
            )
        elif scrapeType == ONGOING_SCRAPE_TYPE:
            scrapeData = KissAnimeScrape.animeList(
                ONGOING,
                ONGOING_FILTER_MAP,
                KissAnimeScrape.commonParser,
                data
            )
        elif scrapeType == COMPLETED_SCRAPE_TYPE:
            scrapeData = KissAnimeScrape.animeList(
                COMPLETED,
                COMPLETED_FILTER_MAP,
                KissAnimeScrape.commonParser,
                data
            )
        elif scrapeType == NEW_AND_HOT_SCRAPE_TYPE:
            scrapeData = KissAnimeScrape.animeList(
                ANIME_LIST_NEW_AND_HOT,
                None,
                KissAnimeScrape.commonParser,
                data
            )
        elif scrapeType == EPISODE_SCRAPE_TYPE:
            scrapeData = KissAnimeScrape.episodes(data['url'])
        elif scrapeType == QUALITY_SELECTOR_SCRAPE_TYPE:
            scrapeData = KissAnimeScrape.quailitySelector(data['url'], data['data'])
        elif scrapeType == GENRES_SCRAPE_TYPE:
            scrapeData = KissAnimeScrape.genres(ANIME_LIST)
        elif scrapeType == VIDEO_SCRAPE_TYPE:
            scrapeData = KissAnimeScrape.video(data['url'], data['data'])
        elif scrapeType == SEARCH_SCRAPE_TYPE:
            scrapeData = KissAnimeScrape.search(data['keyword'])

        return scrapeData

    ## Scrapes the website and pulls the response from the server
    @staticmethod
    def getResponseFromServer(endpoint):
        scraper = cfscrape.create_scraper()
        scrapeUrl = KissAnimeScrape.BASE_URL + endpoint
        return scraper.get(scrapeUrl)

    @staticmethod
    def postResponseToServer(endpoint, data):
        scraper = cfscrape.create_scraper()
        scrapeUrl = KissAnimeScrape.BASE_URL + endpoint
        return scraper.post(scrapeUrl, data=data)

    @staticmethod
    def animeList(defaultUrl, filterMap, parser, data=None):
        url = data['url'] if data['url'] else defaultUrl
        data = data['data']

        if data and data['filter'] and filterMap and url is None:
            url = filterMap[data['filter']]

        response = KissAnimeScrape.getResponseFromServer(url)
        return KissAnimeScrape.parseIntoListType(response, parser, KissAnimeScrape.parseListingRows)

    @staticmethod
    def parseIntoListType(response, parser, linksParser, hasPaging=True):
        soup = BeautifulSoup(response.content,'html.parser')

        links = OrderedDict()
        links = linksParser(soup, links, parser)

        if hasPaging:
            links = KissAnimeScrape.addNextLink(soup, links)

        return {
            'links': links,
            'type': LIST_TYPE_DIR
        }

    ## Returns a list of all the episodes tied to the specified anime url passed in
    #
    #  @param episodesEndpoint string endpoint that points to the episode list
    @staticmethod
    def episodes(episodesEndpoint):
        response = KissAnimeScrape.getResponseFromServer(episodesEndpoint)
        return KissAnimeScrape.parseIntoListType(response, KissAnimeScrape.episodesParser, KissAnimeScrape.parseListingRows)

    @staticmethod
    def quailitySelector(qualitySelectorEndpoint, data):
        callback = data['callback']
        videoSource = KissAnimeScrape.getVideoSourceType()
        videoPageUrl = KissAnimeScrape.generateVideoPageUrl(qualitySelectorEndpoint, videoSource)
        response = KissAnimeScrape.getResponseFromServer(videoPageUrl)

        selectorOptionsLabels = []
        selectorOptionsValues = []

        soup = BeautifulSoup(response.content, 'html.parser')
        qualitySelector = soup.find('select', {"id": "selectQuality"})
        if qualitySelector:
            options = qualitySelector.find_all('option')

            for option in options:
                selectorOptionsLabels.append(option.string)
                selectorOptionsValues.append(option['value'])

        selectorResults = {
            'labels': selectorOptionsLabels,
            'values': selectorOptionsValues
        }

        callback(qualitySelectorEndpoint, selectorResults)

        return selectorResults

    @staticmethod
    def genres(genresEndpoint):
        response = KissAnimeScrape.getResponseFromServer(genresEndpoint)
        return KissAnimeScrape.parseIntoListType(response, KissAnimeScrape.genreParser, KissAnimeScrape.parseGenreList, False)

    ## Function to return a video url that the plugin will use to start playing
    #  @param videoPageUrl url pointing to the webpage where the video link will be found
    @staticmethod
    def video(videoPageUrl, data):
        videoSource = KissAnimeScrape.getVideoSourceType()
        videoPageUrl = KissAnimeScrape.generateVideoPageUrl(videoPageUrl, videoSource)
        response = KissAnimeScrape.getResponseFromServer(videoPageUrl)

        return KissAnimeScrape.getVideoSrcUrl(response, videoSource, data)

    @staticmethod
    def getVideoSourceType():
        videoSourceLabel = SETTINGS_VIDEO_SOURCE_DROPDOWN_MAP[int(ADDON.getSetting(SOURCE_SELECT_ID))]
        return VIDEO_SOURCE_MAP[videoSourceLabel]

    @staticmethod
    def generateVideoPageUrl(url, videoSource):
        url += '&s=' + videoSource
        return url

    @staticmethod
    def search(keyword):
        data = { "keyword": keyword }
        response = KissAnimeScrape.postResponseToServer(ANIME_SEARCH_ENDPOINT, data)
        return KissAnimeScrape.parseIntoListType(response, KissAnimeScrape.commonParser, KissAnimeScrape.parseListingRows)

    @staticmethod
    def commonParser(tableRow, links):
        cell = tableRow.td
        image = ''
        description = ''

        if cell['title'] is not None:
            image = re.search(KissAnimeScrape.ANIME_IMAGE_REGEX, cell['title']).group(1)
            description = re.search(KissAnimeScrape.ANIME_DESC_REGEX, cell['title']).group(1)

        anchor = cell.a
        links[anchor['href']] = KissAnimeScrape.generateLinkObj(
            anchor.string.strip(),
            image,
            description.strip()
        )

        return links

    @staticmethod
    def episodesParser(tableRow, links):
        anchor = tableRow.td.a
        links[anchor['href']] = KissAnimeScrape.generateLinkObj(
            anchor.string.strip(),
            '',
            ''
        )

        return links

    @staticmethod
    def genreParser(anchor, links):
        links[anchor['href']] = KissAnimeScrape.generateLinkObj(
            anchor.string.strip(),
            '',
            ''
        )

        return links

    @staticmethod
    def parseListingRows(soup, links, parser):
        tableRows = KissAnimeScrape.getListingRows(soup)

        if tableRows:
            for tableRow in tableRows:
                if tableRow.td is not None:
                    links = parser(tableRow, links)

        return links

    @staticmethod
    def parseGenreList(soup, links, parser):
        anchorTags = []
        barTitleDivs = soup.find_all('div', { "class": "barTitle" })

        if barTitleDivs:

            for barTitleDiv in barTitleDivs:
                if re.search(KissAnimeScrape.GENRE_TITLE_REGEX, barTitleDiv.string):
                    anchorTags = barTitleDiv.findNext('div').find_all('a')
                    break

            for anchorTag in anchorTags:
                if anchorTag is not None:
                    links = parser(anchorTag, links)

        return links

    @staticmethod
    def addPrevLink(soup, links):
        prevLink = soup.find('a', text=re.compile(KissAnimeScrape.PREV_RESPONSE_TEXT), attrs={'page':True})
        if prevLink is not None:
            links[prevLink['href']] = KissAnimeScrape.generateLinkObj(
                PREV_LABEL,
                DEFAULT_VIDEO_IMAGE,
                PREV_LABEL,
                PAGE_TYPE
            )

        return links

    @staticmethod
    def addNextLink(soup, links):
        nextLink = soup.find('a', text=re.compile(KissAnimeScrape.NEXT_RESPONSE_TEXT), attrs={'page':True})
        if nextLink is not None:
            links[nextLink['href']] = KissAnimeScrape.generateLinkObj(
                NEXT_LABEL,
                DEFAULT_VIDEO_IMAGE,
                NEXT_LABEL,
                PAGE_TYPE
            )

        return links

    @staticmethod
    def getListingRows(soup):
        tableRows = None
        listingObj = soup.find('table', { "class": "listing" })

        if listingObj:
            tableRows = listingObj.find_all('tr')

        return tableRows

    @staticmethod
    def generateLinkObj(name, image, description, itemType=ITEM_TYPE):
        return {
            "name": name,
            "image": image,
            "description": description,
            "type": itemType
        }

    @staticmethod
    def getVideoSrcUrl(response, videoSourceParam=KISS_ANIME_SOURCE_PARAM, data=None):
        videoUrl = ''
        if videoSourceParam == KISS_ANIME_SOURCE_PARAM:
            videoUrl = KissAnimeScrape.getKissAnimeVideoSrcUrl(data['selectorValue'])
        elif videoSourceParam == OPENLOAD_SOURCE_PARAM:
            videoUrl = KissAnimeScrape.getOpenloadVideoSrcUrl(response)

        return videoUrl

    @staticmethod
    def getKissAnimeVideoSrcUrl(selectorValue):
        videoUrl = KissAnimeScrape.getDecryptedVideoLink(selectorValue)
        return {
            'url': videoUrl
        }

    @staticmethod
    def getOpenloadVideoSrcUrl(response):
        videoUrl = None
        soup = BeautifulSoup(response.content, 'html.parser')
        scriptTags = soup.find_all('script')
        for script in scriptTags:
            if script.string:
                regexResult = re.search(KissAnimeScrape.OPENLOAD_VIDEO_REGEX, script.string)
                if regexResult:
                    foundUrl = regexResult.group(1)
                    print foundUrl
                    videoUrl = str(urlresolver.HostedMediaFile(foundUrl).resolve());
                    break

        return {
            'url': videoUrl if videoUrl else ''
        }

    @staticmethod
    def getDecryptedVideoLink(encrypted):
        encryptedLength = len(encrypted)
        enc = [None] * 4

        buff = []
        count = 0
        while count < encryptedLength:
            enc[0] = VIDEO_ENCRYPTION_LOOKUP[encrypted[count]]
            count += 1
            enc[1] = VIDEO_ENCRYPTION_LOOKUP[encrypted[count]]
            buff.append((enc[0] << 2) | (enc[1] >> 4))
            count += 1
            enc[2] = VIDEO_ENCRYPTION_LOOKUP[encrypted[count]]
            if enc[2] == 64:
                break

            buff.append(((enc[1] & 15) << 4) | (enc[2] >> 2))
            count += 1
            enc[3] = VIDEO_ENCRYPTION_LOOKUP[encrypted[count]]
            if enc[3] == 64:
                break

            buff.append((enc[2] & 3) << 6 | enc[3])
            count += 1

        result = ''
        count = 0
        bufferLength = len(buff)
        while count < bufferLength:
            if buff[count] < 128:
                result += unichr(buff[count])
                count += 1
            elif buff[count] > 191 and buff[count] < 224:
                first = (buff[count] & 31) << 6
                count += 1
                second = buff[count] & 63
                count += 1
                result += unichr(first | second)
            else:
                first = (buff[count] & 15) << 12
                count += 1
                second = (buff[count] & 63) << 6
                count += 1
                third = (buff[count] & 63)
                count += 1
                result += unichr(first | second | third)

        return result
