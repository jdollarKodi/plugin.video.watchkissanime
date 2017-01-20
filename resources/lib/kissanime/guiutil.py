import xbmcgui
import xbmcplugin
import urllib

from constants import *

class GuiUtil:

    @staticmethod
    def mainMenu(dataMap):
        for menuItemKey, menuItemValue in dataMap.items():
            url = GuiUtil.generateUrl(menuItemKey)
            li = GuiUtil.generateListItem(url, menuItemValue)
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)

        xbmcplugin.endOfDirectory(ADDON_HANDLE)

    @staticmethod
    def list(dataMap, urlAction, pageAction, isFolder=True):
        for urlKey, obj in dataMap.items():
            action = pageAction if obj and obj['type'] == PAGE_TYPE else urlAction
            url = GuiUtil.generateUrl(action, urlKey)
            name = obj['name'] if obj['name'] else ''
            image = obj['image'] if obj['image'] else DEFAULT_VIDEO_IMAGE
            description = obj['description'] if obj['description'] else None
            li = GuiUtil.generateListItem(url, name, image, description)
            xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=isFolder)

        xbmcplugin.endOfDirectory(ADDON_HANDLE)

    @staticmethod
    def generateListItem(url, name, image=DEFAULT_VIDEO_IMAGE, description=None):
        li = xbmcgui.ListItem(name)
        li.setArt({'icon': image})
        li.setInfo(type='video', infoLabels={'plot': description})
        return li

    @staticmethod
    def displayLoading(functionCall, args):
        busyDialog = xbmcgui.DialogBusy()
        try:
            busyDialog.create()
            functionCall(*args)
        except Exception as e:
            xbmc.log(e)
        finally:
            busyDialog.close()

    @staticmethod
    def generateUrl(urlType, url=None, filter=None):
        params = {}
        params['type'] = urlType

        if url: params['url'] = url
        if filter: params['filter'] = filter

        return GuiUtil.generateUrlObj(params)

    @staticmethod
    def generateUrlObj(data):
        return BASE_APP_URL + '?' + urllib.urlencode(data)
