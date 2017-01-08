import sys
import xbmcplugin
import xbmcgui

ADDON_HANDLE = int(sys.argv[1])

class KissAnime:
    def __init__(self):
        xbmcplugin.setContent(ADDON_HANDLE, 'movies')
    # End init

    def run(self):
        self.buildMainMenu()
    # End run

    def buildMainMenu(self):
        li = xbmcgui.ListItem('allVideos', iconImage='DefaultVideo.jpg')
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=None, listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(ADDON_HANDLE)
    #End buildMainMenu
# End KissAnime
