"""
This file is part of Giswater 3
The program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
"""
# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMainWindow, QDialog


class GwDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


def get_ui_class(ui_file_name, subfolder=None):
    """ Get UI Python class from @ui_file_name """

    ui_folder_path = os.path.dirname(__file__)
    if subfolder:
        ui_folder_path = os.path.join(ui_folder_path, subfolder)
    ui_file_path = os.path.abspath(os.path.join(ui_folder_path, ui_file_name))
    if not os.path.exists:
        print(f"File not found: {ui_file_path}")
        return None

    return uic.loadUiType(ui_file_path)[0]


# Dialogs of toolbar: my_toolbar
FORM_CLASS = get_ui_class('dlg_static.ui', 'my_toolbar')
class DlgButton1(GwDialog, FORM_CLASS):
    pass
FORM_CLASS = get_ui_class('dlg_dinamic.ui', 'my_toolbar')
class DlgButton2(GwDialog, FORM_CLASS):
    pass

# FORM_CLASS = get_ui_class('dlg_button_2.ui', 'my_toolbar')
# class DlgButton2(GwDialog, FORM_CLASS):
#     pass

FORM_CLASS = get_ui_class('dlg_save.ui', 'my_toolbar')
class DlgSave(GwDialog, FORM_CLASS):
    pass

FORM_CLASS = get_ui_class('dlg_button_7.ui', 'my_toolbar')
class DlgButton7(GwDialog, FORM_CLASS):
    pass

