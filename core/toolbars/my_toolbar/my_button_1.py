"""
This file is part of Giswater 3
The program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
"""
# -*- coding: utf-8 -*-
import importlib
import json
import os
import sys
from functools import partial

import global_vars
from ...ui.ui_manager import DlgButton1
from plotly import data
from qgis.core import QgsVectorLayer
from qgis.utils import iface

from ...ui.ui_manager import DlgButton1
from ....settings import giswater_folder, tools_qgis, tools_log, tools_qt, tools_gw,tools_pgdao,tools_db
dialog = importlib.import_module('.dialog', package=f'{giswater_folder}.core.toolbars')


class Graph(dialog.GwAction):

    def __init__(self, icon_path, action_name, text, toolbar, action_group):
        super().__init__(icon_path, action_name, text, toolbar, action_group)
        self.project_type = global_vars.project_type

    def clicked_event(self):
        self.open_dialog()

    def open_dialog(self):

        self.dlg_seaborn = DlgButton1()



        # Populate main
        base_column = [['node_id', 'node_id'], ['result_id', 'result_id']]
        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_values, rows=base_column)
        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_targetColumn, rows=base_column)
        sql = f"SELECT DISTINCT(column_name) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'rpt_node';"
        rows = tools_db.get_rows(sql)
        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_xaxis, rows=rows)
        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_yaxis, rows=rows)
        # Populate child
        self.populate_child_cmb()


        # Listeners
        self.dlg_seaborn.cmb_values.currentIndexChanged.connect(self.populate_child_cmb)
        self.dlg_seaborn.btn_insert.clicked.connect(self.populate_selected_lw)
        self.dlg_seaborn.btn_create.clicked.connect(self.get_graph)


        # Open dialog
        tools_gw.open_dialog(self.dlg_seaborn, dlg_name='seaborn')

    def populate_child_cmb(self):

        print(f"AA -> ")
        index_selected = tools_qt.get_combo_value(self.dlg_seaborn,self.dlg_seaborn.cmb_values)
        sql = f"SELECT DISTINCT({index_selected}) FROM rpt_node order by {index_selected};"
        rows_id = tools_db.get_rows(sql)
        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_basevalue, rows_id)
        self.dlg_seaborn.lw_defaultvalues.clear()
        self.dlg_seaborn.lw_selectedvalues.clear()
        if(index_selected == "node_id"):
            sql = f"SELECT DISTINCT(result_id) FROM rpt_node order by result_id;"
            rows = tools_db.get_rows(sql)
            s = json.dumps(rows)
            d = json.loads(s)
            for r in d:
                self.dlg_seaborn.lw_defaultvalues.addItems(r)
        elif(index_selected == "result_id"):
            sql = f"SELECT DISTINCT(node_id) FROM rpt_node order by node_id;"
            rows = tools_db.get_rows(sql)
            s = json.dumps(rows)
            d = json.loads(s)
            for r in d:
                self.dlg_seaborn.lw_defaultvalues.addItems(r)

    def populate_selected_lw(self):
        # item = self.dlg_seaborn.lw_defaultvalues.selectedItems()
        self.dlg_seaborn.lw_selectedvalues.addItems(item.text() for item in self.dlg_seaborn.lw_defaultvalues.selectedItems())
        for x in self.dlg_seaborn.lw_defaultvalues.selectedIndexes():
            self.dlg_seaborn.lw_defaultvalues.takeItem(x.row())

    def get_graph(self):

        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns
        import psycopg2

        table = tools_qt.get_text(self.dlg_seaborn, self.dlg_seaborn.txt_nameTable)
        base_column = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_values)
        base_value = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_basevalue)
        target_column = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_targetColumn)
        yaxis = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_yaxis)
        xaxis = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_xaxis)

        # query = f"select * from project_fraph.rpt_node where node_id='{node}' and result_id='{result}';"

        # timefi = sorted(time)
        # print(sorted(time))
        # print(timefi)
        if tools_qt.is_checked(self.dlg_seaborn, self.dlg_seaborn.rb_lines):
            legend = []
            # graph code
            sns.set()
            for x in range(self.dlg_seaborn.lw_selectedvalues.count()):

                target_value = self.dlg_seaborn.lw_selectedvalues.item(x).text()
                legend.append(target_value)
                query = f"SELECT {xaxis},{yaxis} FROM {table} WHERE {base_column}='{base_value}' AND {target_column}='{target_value}';"
                print(query)
                db_data = tools_db.get_rows(query)
                # close cursor and connection
                valuex, valuey = zip(*db_data)
                plt.plot(valuex, valuey)

            plt.legend(legend, ncol=2, loc='upper left');
            plt.show()
        elif tools_qt.is_checked(self.dlg_seaborn, self.dlg_seaborn.rb_bars):
            sns.set()
            for x in range(self.dlg_seaborn.lw_selectedvalues.count()-1):
                target_value = self.dlg_seaborn.lw_selectedvalues.item(x).text()
                query = f"SELECT {xaxis},{yaxis} FROM {table} WHERE {base_column}='{base_value}' AND {target_column}='{target_value}';"
                print(query)
                db_data = tools_db.get_rows(query)
                # close cursor and connection
                valuex, valuey = zip(*db_data)
                plt.bar(valuex, valuey)
            plt.show()








