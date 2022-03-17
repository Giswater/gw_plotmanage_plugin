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


class Bokeh(dialog.GwAction):

    def __init__(self, icon_path, action_name, text, toolbar, action_group):
        super().__init__(icon_path, action_name, text, toolbar, action_group)


    def clicked_event(self):
        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns
        import psycopg2
        conn = psycopg2.connect(database="giswater", user="postgres", host="localhost", password="guillem12", port=5432)
        cur = conn.cursor()

        node = '1001'
        result = 'r1'
        yaxis = 'head'
        xaxis = 'time'
        control = 'node_id'

        query = f"select * from project_fraph.rpt_node where result_id='{result}';"

        # execute the query
        cur.execute(query)
        # retrieve the whole result set
        data = cur.fetchall()
        # close cursor and connection
        cur.close()
        conn.close()
        id, result_id, node_id, elevation, demand, head, press, other, time, quality = zip(*data)
        timefi = sorted(time)
        print(sorted(time))
        print(timefi)
        # importing the modules
        from bokeh.plotting import figure, output_file, show

        # instantiating the figure object
        graph = figure(title="Bokeh Bar Graph")


        # height / thickness of the plot
        width = 0.1

        # plotting the bar graph
        graph.vbar(node_id, top=elevation, width=width)

        # displaying the model
        show(graph)





