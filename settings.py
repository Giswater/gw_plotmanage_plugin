"""
This file is part of Giswater plugin example
The program is free software: you can redistribute it and/or modify it under the terms of the GNU 
General Public License as published by the Free Software Foundation, either version 3 of the License, 
or (at your option) any later version.
Author(s): Iván Moreno, Nestor Ibáñez, David Erill
"""
# -*- coding: utf-8 -*-
import configparser, os, sys, glob, importlib

from qgis.core import QgsApplication

# Pointer to the module object instance itself
this = sys.modules[__name__]

this.giswater_folder = None
this.giswater_folder_path = None
this.tools_db = None
this.tools_log = None
this.tools_os = None
this.tools_qgis = None
this.tools_qt = None
this.tools_pgdao = None
this.tools_gw = None
this.dialog = None
this.gw_global_vars = None


def init_plugin(iface):

    # Find and return Giswater plugin folder path
    this.giswater_folder_path = get_giswater_folder()
    if this.giswater_folder_path is None:
        iface.messageBar().pushMessage("", "Giswater plugin folder not found", 1, 15)
        return False

    this.giswater_folder = os.path.basename(this.giswater_folder_path)
    if not os.path.exists(this.giswater_folder_path):
        iface.messageBar().pushMessage("", f"Giswater plugin folder not found: {this.giswater_folder_path}", 1, 15)
        return False

    # Define imports from Giswater modules
    this.gw_global_vars = importlib.import_module('.global_vars', package=f'{this.giswater_folder}')
    this.tools_db = importlib.import_module('.tools_db', package=f'{this.giswater_folder}.lib')
    this.tools_log = importlib.import_module('.tools_log', package=f'{this.giswater_folder}.lib')
    this.tools_os = importlib.import_module('.tools_os', package=f'{this.giswater_folder}.lib')
    this.tools_qgis = importlib.import_module('.tools_qgis', package=f'{this.giswater_folder}.lib')
    this.tools_qt = importlib.import_module('.tools_qt', package=f'{this.giswater_folder}.lib')
    this.tools_gw = importlib.import_module('.tools_gw', package=f'{this.giswater_folder}.core.utils')
    this.dialog = importlib.import_module('.dialog', package=f'{this.giswater_folder}.core.toolbars')
    this.dialog = importlib.import_module('.tools_pgdao', package=f'{this.giswater_folder}.lib')

    # Use Giswater library to both show and log message
    this.tools_qgis.show_info(f"Giswater example plugin successfully initialized", 15)
    this.tools_log.log_info(f"Giswater plugin folder: {this.giswater_folder_path}")

    return True


def get_giswater_folder(filename_to_find='metadata.txt'):
    """ Find and return Giswater plugin folder path """

    # Get QGIS plugin root folder from environment variables
    qgis_plugin_root_folder = None
    try:
        if sys.platform == "win32":
            qgis_plugin_root_folder = os.environ['QGIS_PLUGINPATH']
        elif sys.platform == "linux":
            qgis_plugin_root_folder = os.environ['QGIS_PLUGINPATH']
        elif sys.platform == "darwin":
            qgis_plugin_root_folder = os.environ['QGIS_PLUGINPATH']
    except KeyError:
        pass

    list_folders = []
    if qgis_plugin_root_folder is not None:
        list_folders.append(qgis_plugin_root_folder)

    # Search Giswater plugin in your profile folder
    profile_folder = QgsApplication.qgisSettingsDirPath()
    profiles_plugins_folder = os.path.join(profile_folder, 'python', 'plugins')
    list_folders.append(profiles_plugins_folder)

    for folder in list_folders:
        # Find @filename recursively inside this folder
        for filename in glob.glob(f"{folder}/**/{filename_to_find}", recursive=True):
            parser = configparser.ConfigParser()
            parser.read(filename)
            if not parser.has_section('general'):
                continue
            if not parser.has_option('general', 'name'):
                continue
            if parser['general']['name'] == 'giswater':
                giswater_folder_path = os.path.dirname(filename)
                return giswater_folder_path

    return None

