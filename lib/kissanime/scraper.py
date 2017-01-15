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

    ## constructor
    def __init__(self):
        self.scraper = cfscrape.create_scraper()
    # End init

    ## Scrapes the website and pulls the response from the server
    def getResponseFromServer(self, endpoint):
        scrapeUrl = KissAnimeScrape.BASE_URL + endpoint
        return self.scraper.get(scrapeUrl)
    # End getResponseFromServer

    ## Returns a list of all the anime currently on the site
    def all(self):
        response = self.getResponseFromServer(KissAnimeScrape.ANIME_LIST_ENDPOINT)
        videoLinks = self.getLinksFromListingObject(response)

        return {
            'links': videoLinks,
            'type': LIST_TYPE_DIR
        }
    # End all

    ## Returns a list of all the episodes tied to the specified anime url passed in
    #
    #  @param episodesEndpoint string endpoint that points to the episode list
    def episodes(self, episodesEndpoint):
        response = self.getResponseFromServer(episodesEndpoint)
        videoLinks = self.getLinksFromListingObject(response)

        return {
            'links': videoLinks,
            'type': LIST_TYPE_DIR
        }
    # End episodes

    ## Function to return a video url that the plugin will use to start playing
    #  @param videoPageUrl url pointing to the webpage where the video link will be found
    def video(self, videoPageUrl):
        response = self.getResponseFromServer(videoPageUrl)
        return self.getVideoSrcUrl(response)
    # End video

    ## Generates next and pervious page menu items if they are found on the webpage
    def addPageLinks(self, soup, links):
        prevLink = soup.find('a', text=re.compile('Prev'), attrs={'page':True})
        if prevLink is not None:
            links[prevLink['href']] = 'Previous Page'

        nextLink = soup.find('a', text=re.compile('Next'), attrs={'page':True})
        if nextLink is not None:
            links[nextLink['href']] = 'Next Page'

        return links
    # End addPageLinks

    ## Traverses the dom tree, grabs the encrypted video url and decrypts it.
    #  @param response       dom tree obj returned by the scraper that will be
    #                       traversed to find the videoUrl
    def getVideoSrcUrl(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        qualitySelector = soup.find('select', {"id": "selectQuality"})
        videoUrl = self.getDecryptedVideoLink(qualitySelector.option['value'])
        return {
            'url': videoUrl
        }
    # End getVideoSrcUrl

    ## Traverses the table object for anime lists and episode lists to return
    #  All of the links to various animes or episodes.
    #
    #  @param response      dom tree obj returned by the scraper that will be
    #                       traversed to find the link
    def getLinksFromListingObject(self, response):
        soup = BeautifulSoup(response.content,'html.parser')
        listingObj = soup.find('table', { "class": "listing" })
        tableRows = listingObj.find_all('tr')
        videoLinks = OrderedDict()

        for tableRow in tableRows:
            if tableRow.td is not None:
                anchor = tableRow.td.a
                videoLinks[anchor['href']] = anchor.string.strip()
            # End if
        # End for

        videoLinks = self.addPageLinks(soup, videoLinks)

        return videoLinks
    #End getLinksFromListingObject

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
    #End getDecryptedVideoLink

#End KissAnimeScrape
