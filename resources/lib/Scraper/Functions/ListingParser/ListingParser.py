import re
from bs4 import BeautifulSoup

from resources.lib.Models.Link import Link
from resources.lib.kissanime.constants import LISTING_TYPE, NEXT_LABEL, DEFAULT_VIDEO_IMAGE, NEXT_LABEL, PAGE_TYPE

class ListingParser:
    ANIME_IMAGE_REGEX = re.compile('src=\"(.*?)\"')
    ANIME_DESC_REGEX = re.compile('<p>(.*?)<\/p>', re.DOTALL)
    NEXT_RESPONSE_TEXT = 'Next'

    def parse(self, responseContent):
        soup = BeautifulSoup(responseContent,'html.parser')

        links = self.parseListingRows(soup)
        #links.append(self.parseNextLink(soup))

        return links

    def parseListingRows(self, soup):
        tableRows = None
        links = []
        listingObj = soup.find('table', { "class": "listing" })

        if listingObj:
          tableRows = listingObj.find_all('tr')

        if tableRows:
          for tableRow in tableRows:
            parsedCell = self.parseListingCell(tableRow)
            if parsedCell:
                links.append(parsedCell)

        #links.append(self.parseNextLink(soup))

        return links

    def parseListingCell(self, tableRow):
        link = None

        if tableRow.td:
            link = Link()
            cell = tableRow.td

            if cell['title']:
                link.image = re.search(ListingParser.ANIME_IMAGE_REGEX, cell['title']).group(1)
                description = re.search(ListingParser.ANIME_DESC_REGEX, cell['title']).group(1)

                if description:
                    link.description = description.strip()

            anchor = cell.a

            link.url = anchor['href']
            link.text = anchor.string.strip()
            link.type = LISTING_TYPE

        return link

    def parseNextLink(self, soup):
        link = None
        nextLink = soup.find('a', text=re.compile(ListingParser.NEXT_RESPONSE_TEXT), attrs={'page':True})
        if nextLink:
            link = Link(nextLink['href'], NEXT_LABEL, DEFAULT_VIDEO_IMAGE, NEXT_LABEL, PAGE_TYPE)
        return link
