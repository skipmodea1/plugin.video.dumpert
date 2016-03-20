#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
# Imports
#
import os
import re
import requests
import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
from BeautifulSoup import BeautifulSoup
import json

from dumpert_const import ADDON, SETTINGS, LANGUAGE, IMAGES_PATH, DATE, VERSION


#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__(self):
        # Get the command line arguments
        # Get the plugin url in plugin:// notation
        self.plugin_url = sys.argv[0]
        # Get the plugin handle as an integer number
        self.plugin_handle = int(sys.argv[1])

        # Get plugin settings
        self.DEBUG = SETTINGS.getSetting('debug')

        if self.DEBUG == 'true':
            xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s, %s = %s" % (
                ADDON, VERSION, DATE, "ARGV", repr(sys.argv), "File", str(__file__)), xbmc.LOGNOTICE)

        # Parse parameters
        self.plugin_category = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['plugin_category'][0]
        self.video_list_page_url = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)['url'][0]

        if self.DEBUG == 'true':
            xbmc.log("[ADDON] %s v%s (%s) debug mode, %s = %s" % (
                ADDON, VERSION, DATE, "self.video_list_page_url", str(self.video_list_page_url)),
                     xbmc.LOGNOTICE)

        #
        # Get the videos...
        #
        self.getVideos()

    #
    # Get videos...
    #
    def getVideos(self):
        #
        # Init
        #
        shownsfw = (SETTINGS.getSetting('nsfw') == 'true')
        listing = []

        #
        # Get data
        #
        json_source = requests.get(self.video_list_page_url).text
        data = json.loads(json_source)
        if not data['success']:
            return
        for item in data['items']:
            title = item['title']
            description = item['description']
            thumbnail_url = item['thumbnail']
            nsfw = item['nsfw']
            if not nsfw or shownsfw:
                # grab first item (tablet)
                # skip embedded (youtube links) for now {"version":"embed","uri":"youtube:wOeZB7bnoxw"}
                if item['media'][0]['mediatype'] == 'VIDEO' and item['media'][0]['variants'][0]['version'] != 'embed':
                    url = item['media'][0]['variants'][0]['uri']
                    list_item = xbmcgui.ListItem(label=title, thumbnailImage=thumbnail_url)
                    list_item.setInfo("video", {"title": title, "studio": ADDON, "plot": description})
                    list_item.setArt({'thumb': thumbnail_url, 'icon': thumbnail_url,'fanart': os.path.join(IMAGES_PATH, 'fanart-blur.jpg')})
                    list_item.setProperty('IsPlayable', 'true')
                    is_folder = False
                    # Add refresh option to context menu
                    list_item.addContextMenuItems([('Refresh', 'Container.Refresh')])
                    # Add our item to the listing as a 3-element tuple.
                    listing.append((url, list_item, is_folder))

        # Add our listing to Kodi.
        # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
        # instead of adding one by ove via addDirectoryItem.
        xbmcplugin.addDirectoryItems(self.plugin_handle, listing, len(listing))
        # Disable sorting
        xbmcplugin.addSortMethod(handle=self.plugin_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE)
        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(self.plugin_handle)

