"""
This file is part of Giswater 3
The program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
"""
# -*- coding: utf-8 -*-
import importlib
import os
import sys
from functools import partial

from plotly import data
from qgis.core import QgsVectorLayer
from qgis.utils import iface

from ...ui.ui_manager import DlgButton1
from ....settings import giswater_folder, tools_qgis, tools_log, tools_qt, tools_gw,tools_pgdao,tools_db
dialog = importlib.import_module('.dialog', package=f'{giswater_folder}.core.toolbars')


class Graph(dialog.GwAction):

    def __init__(self, icon_path, action_name, text, toolbar, action_group):
        super().__init__(icon_path, action_name, text, toolbar, action_group)


    def clicked_event(self):
        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns
        import psycopg2
        conn = psycopg2.connect(database="postgres", user="postgres", host="localhost", password="guillem12", port=5433)
        cursor = conn.cursor()

        query = "select * from ws_sample.rpt_node;"

        cursor.execute(query)
        conn.commit()

        rng = np.random.RandomState(0)
        x = np.linspace(0, 10, 500)
        y = np.cumsum(rng.randn(500, 6), 0)
        sns.set()
        plt.plot(x, y)
        plt.legend('ABCDEF', ncol=2, loc='upper left');
        plt.show()



