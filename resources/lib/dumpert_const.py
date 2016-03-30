#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import xbmcaddon

#
# Constants
# 
ADDON = "plugin.video.dumpert"
SETTINGS = xbmcaddon.Addon(id=ADDON)
LANGUAGE = SETTINGS.getLocalizedString
IMAGES_PATH = os.path.join(xbmcaddon.Addon(id=ADDON).getAddonInfo('path'), 'resources', 'images')
DATE = "2016-03-30"
VERSION = "1.1.2"
COOKIES_SFW = {'nsfw': '0', 'cf_clearance' : 'd17cd7a057421e3d711e8effa876aabde408c558-1459337857-3600'}
COOKIES_NSFW = {'nsfw': '1', 'cf_clearance' : 'd17cd7a057421e3d711e8effa876aabde408c558-1459337857-3600'}