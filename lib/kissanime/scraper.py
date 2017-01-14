import cfscrape
import re
import sys
from constants import *

from bs4 import BeautifulSoup

from collections import OrderedDict

class KissAnimeScrape:
    BASE_URL = 'http://kissanime.ru/'
    ANIME_LIST_ENDPOINT = 'AnimeList'
    VIDEO_REGEX = re.compile('http.*googlevideo(.*?)\"')

    def __init__(self):
        self.scraper = cfscrape.create_scraper()

    # End init

    def getResponseFromServer(self, endpoint):
        scrapeUrl = KissAnimeScrape.BASE_URL + endpoint
        return self.scraper.get(scrapeUrl)
    # End getResponseFromServer

    def all(self):
        response = self.getResponseFromServer(KissAnimeScrape.ANIME_LIST_ENDPOINT)
        videoLinks = self.getLinksFromListingObject(response)

        return {
            'links': videoLinks,
            'type': LIST_TYPE_DIR
        }
    # End all

    def episodes(self, episodesEndpoint):
        response = self.getResponseFromServer(episodesEndpoint)
        videoLinks = self.getLinksFromListingObject(response)

        return {
            'links': videoLinks,
            'type': LIST_TYPE_DIR
        }
    # End episodes

    def video(self, videoUrl):
        response = self.getResponseFromServer(videoUrl)
        return self.getVideoSrcUrl(response)
    # End video

    def addPageLinks(self, soup, links):
        prevLink = soup.find('a', text=re.compile('Prev'), attrs={'page':True})
        if prevLink is not None:
            links[prevLink['href']] = 'Previous Page'

        nextLink = soup.find('a', text=re.compile('Next'), attrs={'page':True})
        if nextLink is not None:
            links[nextLink['href']] = 'Next Page'

        return links
    # End addPageLinks

    def getVideoSrcUrl(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        qualitySelector = soup.find('select', {"id": "selectQuality"})
        return self.getDecryptedVideoLink(qualitySelector.option['value'])
    # End getVideoSrcUrl

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
