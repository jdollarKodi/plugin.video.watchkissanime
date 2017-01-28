import xbmcplugin
import xbmcgui
import urllib

from resources.lib.Models.Link import Link
from resources.lib.kissanime.constants import *

class ListLinkDirectory:
    def create(self, linkList, isFolder=True):
        for link in linkList:
            action = LISTING_TYPE if link.type and link.type == PAGE_TYPE else SELECTION_TYPE
            url = self.generateUrl(action, link.url)
            li = self.generateListItem(link)
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=isFolder)

        xbmcplugin.endOfDirectory(ADDON_HANDLE)

    def generateListItem(self, link):
        li = xbmcgui.ListItem(link.text)
        li.setArt({'icon': link.image if link.image else DEFAULT_VIDEO_IMAGE})
        li.setInfo(type='video', infoLabels={'plot': link.description if link.description else None})
        return li

    def generateUrl(self, urlType, url=None, filter=None):
        params = {}
        params['type'] = urlType

        if url: params['url'] = url
        if filter: params['filter'] = filter

        return self.generateUrlObj(params)

    def generateUrlObj(self, data):
        return BASE_APP_URL + '?' + urllib.urlencode(data)
