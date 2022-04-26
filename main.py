"""
This file is part of Giswater 3
The program is free software: you can redistribute it and/or modify it under the terms of the GNU 
General Public License as published by the Free Software Foundation, either version 3 of the License, 
or (at your option) any later version.
"""
# -*- coding: utf-8 -*-
import configparser
import os
import sys

from qgis.PyQt.QtCore import QObject, QSettings
from qgis.PyQt.QtWidgets import QActionGroup, QDockWidget, QToolBar

from . import global_vars
from .core.plugin_toolbar import PluginToolbar
from .settings import gw_global_vars, giswater_folder_path, tools_log,  tools_qgis, tools_os



class GWPluginExample(QObject):

    def __init__(self, iface):
        """ Constructor
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

        super(GWPluginExample, self).__init__()
        self.iface = iface
        self.plugin_toolbars = {}
        self.buttons = {}
        self.action = None
        self.buttons_module = None


    def unload(self, remove_modules=True):
        """ Removes plugin menu items and icons from QGIS GUI
            :param @remove_modules is True when plugin is disabled or reloaded
        """
        pass


    def initGui(self):
        """ Create the menu entries and toolbar icons inside the QGIS GUI """

        # Initialize plugin
        self.init_plugin()


    def init_plugin(self):
        """ Plugin main initialization function """

        # Check if Giswater plugin exists before attempting imports
        if giswater_folder_path is None:
            return

        # Import our toolbar after checking that Giswater plugin exists
        from .core.toolbars import buttons
        self.buttons_module = buttons

        # Initialize plugin global variables
        self.plugin_dir = os.path.dirname(__file__)
        print(self.plugin_dir)
        self.icon_folder = os.path.join(self.plugin_dir, 'icons', 'toolbars')
        self.plugin_name = self.get_plugin_metadata('name', 'giswater_plugin_example')
        tools_log.log_info(f"Our plugin folder: {self.plugin_dir}")
        tools_log.log_info(f"Our plugin name:   {self.plugin_name}")
        setting_file = os.path.join(self.plugin_dir, 'config', 'init.config')
        if not os.path.exists(setting_file):
            message = f"Config file not found at: {setting_file}"
            self.iface.messageBar().pushMessage("", message, 1, 20)
            return

        giswater_plugin_name = tools_qgis.get_plugin_metadata('name', 'giswater')
        get_major_version = tools_qgis.get_major_version()
        global_vars.roaming_user_dir = f'{tools_os.get_datadir()}{os.sep}{giswater_plugin_name}{os.sep}{get_major_version}'
        # Need init giswater global_vars if we can inherit from GwMaptool becouse example is loaded before giswater
        gw_global_vars.init_global(self.iface, self.iface.mapCanvas(), giswater_folder_path, self.plugin_name, global_vars.roaming_user_dir)

        global_vars.init_global(self.iface, self.iface.mapCanvas(), self.plugin_dir, self.plugin_name)

        self.settings = QSettings(setting_file, QSettings.IniFormat)
        self.settings.setIniCodec(sys.getfilesystemencoding())
        self.qgis_settings = QSettings()
        self.qgis_settings.setIniCodec(sys.getfilesystemencoding())

        # Check if user config folder exists
        user_folder_name = self.plugin_name.replace('gw_', '').replace('_plugin', '')
        self._manage_user_config_folder(f"{global_vars.roaming_user_dir}{os.sep}{user_folder_name}")
        global_vars.user_folder_name = user_folder_name

        # Create custom plugin toolbars
        self.create_toolbars()

        # Manage actions of the custom plugin toolbars
        self.manage_toolbars()

        # Manage global_vars
        self.manage_global_vars()


    def create_toolbars(self):
        """ Create custom plugin toolbars """

        # Get list of available toolbars
        list_toolbars = self.settings.value(f"toolbars/list_toolbars")
        if list_toolbars:
            # Check if list_values has only one value
            if type(list_toolbars) is str:
                list_toolbars = [list_toolbars]
        else:
            tools_log.log_info(f"Parameter 'list_toolbars' not set in section 'toolbars' of config file")
            return

        for toolbar_id in list(list_toolbars):
            self.create_toolbar(toolbar_id)


    def manage_toolbars(self):
        """ Manage actions of the custom plugin toolbars """

        # Manage action group of every toolbar
        parent = self.iface.mainWindow()
        for plugin_toolbar in list(self.plugin_toolbars.values()):
            ag = QActionGroup(parent)
            for index_action in plugin_toolbar.list_actions:
                button_def = self.settings.value(f"buttons_def/{index_action}")
                if button_def:
                    text = self.settings.value(f"buttons_text/{index_action}")
                    if text is None:
                        text = f'{index_action}_text'
                    icon_path = os.path.join(self.icon_folder, plugin_toolbar.toolbar_id, f"{index_action}.png")
                    if hasattr(self.buttons_module, button_def):
                        button_class = getattr(self.buttons_module, button_def)
                        button = button_class(icon_path, button_def, text, plugin_toolbar.toolbar, ag)
                        self.buttons[index_action] = button
                    else:
                        tools_log.log_warning(f"Class '{button_def}' not found in: {self.buttons_module.__file__}")


    def create_toolbar(self, toolbar_id):

        list_actions = self.settings.value(f"toolbars/{toolbar_id}")
        if list_actions is None:
            tools_log.log_info(f"Toolbar '{toolbar_id}' has no action set in config file")
            return

        if type(list_actions) != list:
            list_actions = [list_actions]

        toolbar_name = f'toolbar_{toolbar_id}_name'
        plugin_toolbar = PluginToolbar(toolbar_id, toolbar_name, True)

        # If the toolbar is ToC, add it to the Layes docker toolbar, else create a new toolbar
        if toolbar_id == "toc":
            plugin_toolbar.toolbar = self.iface.mainWindow().findChild(QDockWidget, 'Layers').findChildren(QToolBar)[0]
        else:
            plugin_toolbar.toolbar = self.iface.addToolBar(toolbar_name)

        plugin_toolbar.toolbar.setObjectName(toolbar_name)
        plugin_toolbar.list_actions = list_actions
        self.plugin_toolbars[toolbar_id] = plugin_toolbar


    def get_plugin_metadata(self, parameter, default_value):
        """ Get @parameter from metadata.txt file """

        # Check if metadata file exists
        metadata_file = os.path.join(self.plugin_dir, 'metadata.txt')
        if not os.path.exists(metadata_file):
            message = f"Metadata file not found: {metadata_file}"
            print(message)
            return default_value

        value = None
        try:
            metadata = configparser.ConfigParser()
            metadata.read(metadata_file)
            value = metadata.get('general', parameter)
        except configparser.NoOptionError:
            message = "Parameter not found: {parameter}"
            print(message)
            value = default_value
        finally:
            return value


    def manage_global_vars(self):

        schema_name = self.settings.value(f"database/schema_name")
        global_vars.schema_name = schema_name

    def _manage_user_config_folder(self, user_folder_dir):
        """ Check if user config folder exists. If not create empty files init.config and session.config """

        try:
            config_folder = f"{user_folder_dir}{os.sep}config{os.sep}"
            if not os.path.exists(config_folder):
                tools_log.log_info(f"Creating user config folder: {config_folder}")
                os.makedirs(config_folder)

            # Check if config files exists. If not create them empty
            filepath = f"{config_folder}{os.sep}init.config"
            if not os.path.exists(filepath):
                open(filepath, 'a').close()
            filepath = f"{config_folder}{os.sep}session.config"
            if not os.path.exists(filepath):
                open(filepath, 'a').close()

        except Exception as e:
            tools_log.log_warning(f"manage_user_config_folder: {e}")
