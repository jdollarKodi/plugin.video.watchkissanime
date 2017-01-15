import cfscrape
import re
import sys
from constants import *

from bs4 import BeautifulSoup

from collections import OrderedDict

## A class containing all of the scraping logic in order to extract
#  information from the kiss anime site
class KissAnimeScrape:
    ## Base URL/Host where the scraper will be pulling data from
    BASE_URL = 'http://kissanime.ru/'

    ## Endpoint where all of the anime is listed in a list format
    ANIME_LIST_ENDPOINT = 'AnimeList'

    ANIME_IMAGE_REGEX = re.compile('src=\"(.*?)\"')
    ANIME_DESC_REGEX = re.compile('<p>(.*?)<\/p>', re.DOTALL)

    NEXT_RESPONSE_TEXT = 'Next'
    PREV_RESPONSE_TEXT = 'Prev'

    ## constructor
    def __init__(self):
        self.scraper = cfscrape.create_scraper()

    ## Scrapes the website and pulls the response from the server
    def getResponseFromServer(self, endpoint):
        scrapeUrl = KissAnimeScrape.BASE_URL + endpoint
        return self.scraper.get(scrapeUrl)

    ## Returns a list of all the anime currently on the site
    def all(self, urlParam):
        url = KissAnimeScrape.ANIME_LIST_ENDPOINT if urlParam is None else urlParam
        response = self.getResponseFromServer(url)
        self.setupSoup(response)

        links = OrderedDict()
        links = self.addPrevLink(links)
        links = self.parseListingRows(links, self.allParser)
        links = self.addNextLink(links)

        return {
            'links': links,
            'type': LIST_TYPE_DIR
        }

    ## Returns a list of all the episodes tied to the specified anime url passed in
    #
    #  @param episodesEndpoint string endpoint that points to the episode list
    def episodes(self, episodesEndpoint):
        response = self.getResponseFromServer(episodesEndpoint)
        self.setupSoup(response)

        links = OrderedDict()
        links = self.addPrevLink(links)
        links = self.parseListingRows(links, self.episodesParser)
        links = self.addNextLink(links)

        #videoLinks = self.getLinksFromListingObject(response)

        return {
            'links': links,
            'type': LIST_TYPE_DIR
        }

    ## Function to return a video url that the plugin will use to start playing
    #  @param videoPageUrl url pointing to the webpage where the video link will be found
    def video(self, videoPageUrl):
        response = self.getResponseFromServer(videoPageUrl)
        return self.getVideoSrcUrl(response)

    def allParser(self, tableRow, links):
        cell = tableRow.td
        image = ''
        description = ''

        if cell['title'] is not None:
            image = re.search(KissAnimeScrape.ANIME_IMAGE_REGEX, cell['title']).group(1)
            description = re.search(KissAnimeScrape.ANIME_DESC_REGEX, cell['title']).group(1)

        anchor = cell.a
        links[anchor['href']] = self.generateLinkObj(
            anchor.string.strip(),
            image,
            description.strip()
        )

        return links

    def episodesParser(self, tableRow, links):
        anchor = tableRow.td.a
        links[anchor['href']] = self.generateLinkObj(
            anchor.string.strip(),
            '',
            ''
        )

        return links

    def parseListingRows(self, links, parser):
        tableRows = self.getListingRows()

        for tableRow in tableRows:
            if tableRow.td is not None:
                links = parser(tableRow, links)

        return links

    def addPrevLink(self, links):
        prevLink = self.soup.find('a', text=re.compile(KissAnimeScrape.PREV_RESPONSE_TEXT), attrs={'page':True})
        if prevLink is not None:
            links[prevLink['href']] = self.generateLinkObj(
                PREV_LABEL,
                DEFAULT_VIDEO_IMAGE,
                PREV_LABEL,
                PAGE_TYPE
            )

        return links

    def addNextLink(self, links):
        nextLink = self.soup.find('a', text=re.compile(KissAnimeScrape.NEXT_RESPONSE_TEXT), attrs={'page':True})
        if nextLink is not None:
            links[nextLink['href']] = self.generateLinkObj(
                NEXT_LABEL,
                DEFAULT_VIDEO_IMAGE,
                NEXT_LABEL,
                PAGE_TYPE
            )

        return links

    ## Traverses the dom tree, grabs the encrypted video url and decrypts it.
    #  @param response       dom tree obj returned by the scraper that will be
    #                       traversed to find the videoUrl
    def getVideoSrcUrl(self, response):
        self.soup = BeautifulSoup(response.content, 'html.parser')
        qualitySelector = self.soup.find('select', {"id": "selectQuality"})
        videoUrl = self.getDecryptedVideoLink(qualitySelector.option['value'])
        return {
            'url': videoUrl
        }

    def getListingRows(self):
        listingObj = self.soup.find('table', { "class": "listing" })
        tableRows = listingObj.find_all('tr')
        return tableRows

    def setupSoup(self, response):
        self.soup = BeautifulSoup(response.content,'html.parser')

    def generateLinkObj(self, name, image, description, itemType=ITEM_TYPE):
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
    def getDecryptedVideoLink(self, encrypted):
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
