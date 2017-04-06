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
<<<<<<< HEAD
DATE = "2017-04-06"
VERSION = "1.1.4"
=======
DATE = "2017-03-03"
VERSION = "1.1.3"
>>>>>>> origin/master
