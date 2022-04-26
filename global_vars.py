"""
This file is part of Giswater 3
The program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
"""
# -*- coding: utf-8 -*-
import os
import sys

from qgis.PyQt.QtCore import QSettings

iface = None
canvas = None
plugin_dir = None
roaming_user_dir = None
user_folder_name = None
plugin_name = None
settings = None
schema_name = None


def init_global(p_iface, p_canvas, p_plugin_dir, p_plugin_name):

    global iface, canvas, plugin_dir, plugin_name
    iface = p_iface
    canvas = p_canvas
    plugin_dir = p_plugin_dir
    plugin_name = p_plugin_name


def init_settings(setting_file):

    global settings
    settings = QSettings(setting_file, QSettings.IniFormat)
    settings.setIniCodec(sys.getfilesystemencoding())

