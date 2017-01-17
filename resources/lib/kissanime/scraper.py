import cfscrape
import re
import sys
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

    NEXT_RESPONSE_TEXT = 'Next'
    PREV_RESPONSE_TEXT = 'Prev'

    @staticmethod
    def scrape(data):
        scrapeType = data['scrapeType']
        scrapeData = {}

        if scrapeType == ALL_SCRAPE_TYPE:
            url = data['url']
            passedInData = data['data']
            scrapeData = KissAnimeScrape.all(url, passedInData)
        elif scrapeType == ONGOING_SCRAPE_TYPE:
            url = data['url']
            passedInData = data['data']
            scrapeData = KissAnimeScrape.ongoing(url, passedInData)
        elif scrapeType == COMPLETED_SCRAPE_TYPE:
            url = data['url']
            passedInData = data['data']
            scrapeData = KissAnimeScrape.completed(url, passedInData)
        elif scrapeType == EPISODE_SCRAPE_TYPE:
            url = data['url']
            scrapeData = KissAnimeScrape.episodes(url)
        elif scrapeType == VIDEO_SCRAPE_TYPE:
            url = data['url']
            scrapeData = KissAnimeScrape.video(url)
        elif scrapeType == SEARCH_SCRAPE_TYPE:
            keyword = data['keyword']
            scrapeData = KissAnimeScrape.search(keyword)

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

    ## Returns a list of all the anime currently on the site
    @staticmethod
    def all(urlParam, data=None):
        url = urlParam if urlParam else ANIME_LIST

        if data and data['filter'] and urlParam is None:
            url = ANIME_LIST_FILTER_MAP[data['filter']]

        response = KissAnimeScrape.getResponseFromServer(url)
        soup = KissAnimeScrape.setupSoup(response)

        links = OrderedDict()
        links = KissAnimeScrape.addPrevLink(soup, links)
        links = KissAnimeScrape.parseListingRows(soup, links, KissAnimeScrape.allParser)
        links = KissAnimeScrape.addNextLink(soup, links)

        return {
            'links': links,
            'type': LIST_TYPE_DIR
        }

    @staticmethod
    def ongoing(urlParam, data=None):
        url = urlParam if urlParam else ONGOING

        if data and data['filter'] and urlParam is None:
            url = ONGOING_FILTER_MAP[data['filter']]

        response = KissAnimeScrape.getResponseFromServer(url)
        soup = KissAnimeScrape.setupSoup(response)

        links = OrderedDict()
        links = KissAnimeScrape.addPrevLink(soup, links)
        links = KissAnimeScrape.parseListingRows(soup, links, KissAnimeScrape.ongoingParser)
        links = KissAnimeScrape.addNextLink(soup, links)

        return {
            'links': links,
            'type': LIST_TYPE_DIR
        }

    @staticmethod
    def completed(urlParam, data=None):
        url = urlParam if urlParam else COMPLETED

        if data and data['filter'] and urlParam is None:
            url = COMPLETED_FILTER_MAP[data['filter']]

        response = KissAnimeScrape.getResponseFromServer(url)
        soup = KissAnimeScrape.setupSoup(response)

        links = OrderedDict()
        links = KissAnimeScrape.addPrevLink(soup, links)
        links = KissAnimeScrape.parseListingRows(soup, links, KissAnimeScrape.ongoingParser)
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
        soup = KissAnimeScrape.setupSoup(response)

        links = OrderedDict()
        links = KissAnimeScrape.addPrevLink(soup, links)
        links = KissAnimeScrape.parseListingRows(soup, links, KissAnimeScrape.episodesParser)
        links = KissAnimeScrape.addNextLink(soup, links)

        return {
            'links': links,
            'type': LIST_TYPE_DIR
        }

    ## Function to return a video url that the plugin will use to start playing
    #  @param videoPageUrl url pointing to the webpage where the video link will be found
    @staticmethod
    def video(videoPageUrl):
        response = KissAnimeScrape.getResponseFromServer(videoPageUrl)
        return KissAnimeScrape.getVideoSrcUrl(response)

    @staticmethod
    def search(keyword):
        data = { "keyword": keyword }
        response = KissAnimeScrape.postResponseToServer(ANIME_SEARCH_ENDPOINT, data)
        soup = KissAnimeScrape.setupSoup(response)

        links = OrderedDict()
        links = KissAnimeScrape.addPrevLink(soup, links)
        links = KissAnimeScrape.parseListingRows(soup, links, KissAnimeScrape.searchParser)
        links = KissAnimeScrape.addNextLink(soup, links)
        return {
            'links': links,
            'type': LIST_TYPE_DIR
        }

    @staticmethod
    def allParser(tableRow, links):
        return KissAnimeScrape.commonParser(tableRow, links)

    @staticmethod
    def ongoingParser(tableRow, links):
        return KissAnimeScrape.commonParser(tableRow, links)

    @staticmethod
    def searchParser(tableRow, links):
        return KissAnimeScrape.commonParser(tableRow, links)

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
    def parseListingRows(soup, links, parser):
        tableRows = KissAnimeScrape.getListingRows(soup)

        if tableRows:
            for tableRow in tableRows:
                if tableRow.td is not None:
                    links = parser(tableRow, links)

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

    ## Traverses the dom tree, grabs the encrypted video url and decrypts it.
    #  @param response       dom tree obj returned by the scraper that will be
    #                       traversed to find the videoUrl
    @staticmethod
    def getVideoSrcUrl(response):
        soup = BeautifulSoup(response.content, 'html.parser')
        qualitySelector = soup.find('select', {"id": "selectQuality"})
        videoUrl = KissAnimeScrape.getDecryptedVideoLink(qualitySelector.option['value'])
        return {
            'url': videoUrl
        }

    @staticmethod
    def getListingRows(soup):
        tableRows = None
        listingObj = soup.find('table', { "class": "listing" })

        if listingObj:
            tableRows = listingObj.find_all('tr')

        return tableRows

    @staticmethod
    def setupSoup(response):
        return BeautifulSoup(response.content,'html.parser')

    @staticmethod
    def generateLinkObj(name, image, description, itemType=ITEM_TYPE):
        return {
            "name": name,
            "image": image,
            "description": description,
            "type": itemType
        }

    ## Python interpretation of kiss anime's decryption algorithm from their
    #  javascript. What will be used to decrypt their encoded video url
    #
    #  @param encrypted string encrypted string that will be decoded
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
