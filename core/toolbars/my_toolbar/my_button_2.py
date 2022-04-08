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

from plotly import data
from qgis.core import QgsVectorLayer
from qgis.utils import iface
from qgis.PyQt.QtCore import QSettings
from collections import OrderedDict
from ....lib import tools
from .... import global_vars
from ...ui.ui_manager import DlgButton2, DlgButton1
from ....settings import giswater_folder, tools_qgis, tools_log, tools_qt, tools_gw,tools_pgdao,tools_db
dialog = importlib.import_module('.dialog', package=f'{giswater_folder}.core.toolbars')


class Graph2(dialog.GwAction):

    def __init__(self, icon_path, action_name, text, toolbar, action_group):
        super().__init__(icon_path, action_name, text, toolbar, action_group)


    def clicked_event(self):
        self.open_dialog()

    def open_dialog(self):

        self.dlg_seaborn = DlgButton1()

        setting_file = os.path.join(global_vars.plugin_dir, 'config', 'plot.config')
        if not os.path.exists(setting_file):
            message = f"Config file not found at: {setting_file}"
            self.iface.messageBar().pushMessage("", message, 1, 20)
            return
        settings = QSettings(setting_file, QSettings.IniFormat)
        settings.setIniCodec(sys.getfilesystemencoding())

        if tools_gw.get_project_type() == "ws":
            base_tables = settings.value("tables/ws")
        elif tools_gw.get_project_type() == "ud":
            base_tables = settings.value("tables/ud")
        else:
            base_tables = settings.value("tables/other")

        base_tables = [[base_table] for base_table in base_tables]
        print(base_tables)
        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_nameTable, rows=base_tables)

        # Populate child
        # self.populate_child_cmb()

        # Listeners
        self.dlg_seaborn.cmb_nameTable.currentIndexChanged.connect(self.populate_table_child_cmb)
        self.dlg_seaborn.cmb_basecolumn.currentIndexChanged.connect(self.populate_base_child_cmb)
        self.dlg_seaborn.cmb_targetColumn.currentIndexChanged.connect(self.populate_target_child_cmb)
        # self.dlg_seaborn.btn_insert.clicked.connect(self.populate_selected_lw)
        self.dlg_seaborn.btn_create.clicked.connect(self.get_graph)
        self.dlg_seaborn.btn_save.clicked.connect(self.set_config)
        self.dlg_seaborn.btn_load.clicked.connect(self.get_config)
        self.dlg_seaborn.rb_dinamic.toggled.connect(self.populate_rb_child_cmb)
        self.dlg_seaborn.rb_static.toggled.connect(self.populate_rb_child_cmb)

        # Open dialog
        tools_gw.open_dialog(self.dlg_seaborn, dlg_name='seaborn')
    def populate_rb_child_cmb(self):
        if tools_qt.is_checked(self.dlg_seaborn, self.dlg_seaborn.rb_dinamic):
            base_column = [['2D_Histogram', '2D Histogram'], ['Bar_plot', 'Bar plot'], ['Box_plot', 'Box plot'], ['Contour_plot', 'Contour plot'],
                           ['Historgram', 'Histogram'], ['Pie_Chart', 'Pie Chart'], ['Polar_plot', 'Polar_plot'], ['Scatter plot', 'Scatter plot'],
                           ['Violin plot', 'Violin plot']]
            tools_qt.fill_combo_values(self.dlg_seaborn.cmb_plottype, rows=base_column)
        elif tools_qt.is_checked(self.dlg_seaborn, self.dlg_seaborn.rb_static):
            base_column = [['Bar plot', 'Bar plot'], ['Box plot', 'Box plot'], ['Scatter plot', 'Scatter plot'], ['Pie_Chart', 'Pie Chart'],
                           ['Histogram', 'Histogram'], ['contour', 'contour']]
            tools_qt.fill_combo_values(self.dlg_seaborn.cmb_plottype, rows=base_column)

    def populate_table_child_cmb(self):
        index_selected = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_nameTable)
        sql = f"SELECT DISTINCT(column_name) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{index_selected}';"
        rows = tools_db.get_rows(sql)

        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_basecolumn, rows=rows)
        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_targetColumn, rows=rows)
        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_xaxis, rows=rows)
        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_yaxis, rows=rows)


    def populate_base_child_cmb(self):

        table_selected = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_nameTable)
        index_selected = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_basecolumn)
        sql = f"SELECT DISTINCT({index_selected}) FROM {table_selected} order by {index_selected};"
        rows_id = tools_db.get_rows(sql)
        tools_qt.fill_combo_values(self.dlg_seaborn.cmb_basevalue, rows_id)


    def populate_target_child_cmb(self):

        table_selected = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_nameTable)
        index_selected = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_targetColumn)

        # self.dlg_seaborn.lw_defaultvalues.clear()
        # self.dlg_seaborn.lw_selectedvalues.clear()

        # sql = f"SELECT DISTINCT({index_selected}) FROM {table_selected} order by {index_selected};"
        # rows = tools_db.get_rows(sql)
        # s = json.dumps(rows)
        # d = json.loads(s)
        # for r in d:
        #     self.dlg_seaborn.lw_defaultvalues.addItems(r)


    def populate_selected_lw(self):
        # item = self.dlg_seaborn.lw_defaultvalues.selectedItems()
        self.dlg_seaborn.lw_selectedvalues.addItems(
            item.text() for item in self.dlg_seaborn.lw_defaultvalues.selectedItems())
        for x in self.dlg_seaborn.lw_defaultvalues.selectedIndexes():
            self.dlg_seaborn.lw_defaultvalues.takeItem(x.row())

    def get_graph(self):
        if tools_qt.is_checked(self.dlg_seaborn, self.dlg_seaborn.rb_dinamic):
            self.get_din_graph()
        elif tools_qt.is_checked(self.dlg_seaborn, self.dlg_seaborn.rb_static):
            self.get_stat_graph()

    def get_din_graph(self):

        import plotly.express as px
        import plotly.graph_objects as go

        table = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_nameTable)
        plot_type = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_plottype)
        base_column = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_basecolumn)
        base_value = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_basevalue)
        target_column = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_targetColumn)
        target_value = tools_qt.get_text(self.dlg_seaborn, self.dlg_seaborn.le_target)
        yaxis = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_yaxis)
        xaxis = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_xaxis)

        query = f"SELECT {target_column},{xaxis},{yaxis} FROM {table} WHERE {base_column}='{base_value}' {target_value};"
        # print(query)
        db_data = tools_db.get_rows(query)
        if plot_type == 'Scatter plot':
            num_keys = []
            # graph code
            fi = go.Figure()
            x_result = {}
            y_result = {}

            print(query)

            for target, x, y in db_data:

                key = target
                if key not in x_result:
                    x_result[key] = []
                    y_result[key] = []
                    num_keys.append(key)
                    x_result[key].append(x)
                    y_result[key].append(y)
                else:
                    x_result[key].append(x)
                    y_result[key].append(y)
            node = []
            for key in num_keys:
                fi.add_trace(go.Scatter(x=x_result[key], y=y_result[key]))
            for i in range(len(fi.data)):
                step = dict(
                    method="update",
                    args=[{"visible": [False] * len(fi.data)},
                          {"title": "Slider switched to node: " + str(num_keys[i])}],  # layout attribute
                )
                step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
                node.append(step)

            sliders = [dict(
                active=10,
                currentvalue={"prefix": "Frequency: "},
                pad={"b": 50},
                steps=node
            )]

            fi.update_layout(
                sliders=sliders
            )

            fi.show()
        elif plot_type == '2D_Histogram':
            num_keys = []
            # graph code
            fi = go.Figure()
            x_result = {}
            y_result = {}

            print(query)

            for target, x, y in db_data:

                key = target
                if key not in x_result:
                    x_result[key] = []
                    y_result[key] = []
                    num_keys.append(key)
                    x_result[key].append(x)
                    y_result[key].append(y)
                else:
                    x_result[key].append(x)
                    y_result[key].append(y)

            for key in num_keys:
                fi.add_trace(go.Histogram2d(x=x_result[key], y=y_result[key]))
            fi.show()
        elif plot_type == 'Bar_plot':
            num_keys = []
            # graph code
            fi = go.Figure()
            x_result = {}
            y_result = {}

            print(query)

            for target, x, y in db_data:

                key = target
                if key not in x_result:
                    x_result[key] = []
                    y_result[key] = []
                    num_keys.append(key)
                    x_result[key].append(x)
                    y_result[key].append(y)
                else:
                    x_result[key].append(x)
                    y_result[key].append(y)

            for key in num_keys:
                fi.add_trace(go.Bar(x=x_result[key], y=y_result[key]))
            fi.show()
        elif plot_type == 'Box_plot':
            num_keys = []
            # graph code
            fi = go.Figure()
            x_result = {}
            y_result = {}

            print(query)

            for target, x, y in db_data:

                key = target
                if key not in x_result:
                    x_result[key] = []
                    y_result[key] = []
                    num_keys.append(key)
                    x_result[key].append(x)
                    y_result[key].append(y)
                else:
                    x_result[key].append(x)
                    y_result[key].append(y)

            for key in num_keys:
                fi.add_trace(go.Box(x=x_result[key], y=y_result[key]))
            fi.show()
        elif plot_type == 'Contour_plot':
            num_keys = []
            # graph code
            fi = go.Figure()
            x_result = {}
            y_result = {}

            print(query)

            for target, x, y in db_data:

                key = target
                if key not in x_result:
                    x_result[key] = []
                    y_result[key] = []
                    num_keys.append(key)
                    x_result[key].append(x)
                    y_result[key].append(y)
                else:
                    x_result[key].append(x)
                    y_result[key].append(y)

            for key in num_keys:
                fi.add_trace(go.Contours(x=x_result[key], y=y_result[key]))
            fi.show()
        elif plot_type == 'Historgram':
            num_keys = []
            # graph code
            fi = go.Figure()
            x_result = {}
            y_result = {}

            print(query)

            for target, x, y in db_data:

                key = target
                if key not in x_result:
                    x_result[key] = []
                    y_result[key] = []
                    num_keys.append(key)
                    x_result[key].append(x)
                    y_result[key].append(y)
                else:
                    x_result[key].append(x)
                    y_result[key].append(y)

            for key in num_keys:
                fi.add_trace(go.Histogram(x=x_result[key], y=y_result[key]))
            fi.show()
        elif plot_type == 'Pie_Chart':
            num_keys = []
            # graph code
            fi = go.Figure()
            dict_result = {}
            xrows = []

            print(query)

            for target, x, y in db_data:

                key = target
                if key not in dict_result:
                    dict_result[key] = []
                    num_keys.append(key)
                    dict_result[key].append(y)
                else:
                    dict_result[key].append(y)
                xrows.append(x)

            for key in num_keys:
                fi.add_trace(go.Pie(values=db_data))
            fi.show()
        elif plot_type == 'Polar_plot':
            num_keys = []
            # graph code
            fi = go.Figure()
            dict_result = {}
            xrows = []

            print(query)

            for target, x, y in db_data:

                key = target
                if key not in dict_result:
                    dict_result[key] = []
                    num_keys.append(key)
                    dict_result[key].append(y)
                else:
                    dict_result[key].append(y)
                xrows.append(x)

            for key in num_keys:
                fi.add_trace(go.Barpolar(r=db_data))
            fi.show()
        elif plot_type == 'Violin plot':
            num_keys = []
            # graph code
            fi = go.Figure()
            x_result = {}
            y_result = {}

            print(query)

            for target, x, y in db_data:

                key = target
                if key not in x_result:
                    x_result[key] = []
                    y_result[key] = []
                    num_keys.append(key)
                    x_result[key].append(x)
                    y_result[key].append(y)
                else:
                    x_result[key].append(x)
                    y_result[key].append(y)

            for key in num_keys:
                fi.add_trace(go.Violin(x=x_result[key], y=y_result[key]))
            fi.show()



    def get_stat_graph(self):

        import matplotlib.pyplot as plt
        import seaborn as sns

        table = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_nameTable)
        plot_type = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_plottype)
        base_column = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_basecolumn)
        base_value = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_basevalue)
        target_column = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_targetColumn)
        target_value = tools_qt.get_text(self.dlg_seaborn, self.dlg_seaborn.le_target)
        yaxis = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_yaxis)
        xaxis = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_xaxis)
        query = f"SELECT {target_column},{xaxis},{yaxis} FROM {table} WHERE {base_column}='{base_value}' {target_value};"
        print(query)
        db_data = tools_db.get_rows(query)
        if plot_type == "Bar plot":
            num_keys = []
            # graph code
            sns.set()
            x_result = {}
            y_result = {}


            print(query)

            for target, x, y in db_data:

                key = target
                if key not in x_result:
                    x_result[key] = []
                    y_result[key] = []
                    num_keys.append(key)
                    x_result[key].append(x)
                    y_result[key].append(y)
                else:
                    x_result[key].append(x)
                    y_result[key].append(y)

            for key in num_keys:
                plt.bar(x_result[key], y_result[key])

            plt.legend(num_keys, ncol=2, loc='upper left');
            plt.show()
        elif plot_type == "Box plot":
            num_keys = []
            # graph code
            sns.set()
            x_result = {}
            y_result = {}


            print(query)

            for target, x, y in db_data:

                key = target
                if key not in x_result:
                    x_result[key] = []
                    y_result[key] = []
                    num_keys.append(key)
                    x_result[key].append(x)
                    y_result[key].append(y)
                else:
                    x_result[key].append(x)
                    y_result[key].append(y)

            for key in num_keys:
                plt.boxplot(db_data)

            plt.legend(num_keys, ncol=2, loc='upper left');
            plt.show()
        elif plot_type == "Scatter plot":
            num_keys = []
            # graph code
            sns.set()
            x_result = {}
            y_result = {}

            print(query)

            for target, x, y in db_data:

                key = target
                if key not in x_result:
                    x_result[key] = []
                    y_result[key] = []
                    num_keys.append(key)
                    x_result[key].append(x)
                    y_result[key].append(y)
                else:
                    x_result[key].append(x)
                    y_result[key].append(y)

            for key in num_keys:
                plt.scatter(x_result[key], y_result[key])

            plt.legend(num_keys,bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=3)
            plt.show()
        elif plot_type == "Pie_Chart":
            sns.set()
            for values in db_data:
                plt.pie(x=values)
            plt.show()
        elif plot_type == "Histogram":
            sns.set()
            for values in db_data:
                plt.hist(x=values[1], data=values)
            plt.show()
        elif plot_type == "contour":
            sns.set()
            for values in db_data:
                plt.contourf(data=values)
            plt.show()

    def set_config(self):
        rb_dinamic = tools_qt.is_checked(self.dlg_seaborn, self.dlg_seaborn.rb_dinamic)
        rb_static = tools_qt.is_checked(self.dlg_seaborn, self.dlg_seaborn.rb_static)
        plot = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_plottype)
        table = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_nameTable)
        base_column = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_basecolumn)
        base_value = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_basevalue)
        target_value = tools_qt.get_text(self.dlg_seaborn, self.dlg_seaborn.le_target)
        # target_selected_values =[self.dlg_seaborn.lw_selectedvalues.item(x) for x in range(self.dlg_seaborn.lw_selectedvalues.count())]
        # target_values =[self.dlg_seaborn.lw_defaultvalues.item(x) for x in range(self.dlg_seaborn.lw_defaultvalues.count())]
        xaxis = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_xaxis)
        yaxis = tools_qt.get_combo_value(self.dlg_seaborn, self.dlg_seaborn.cmb_yaxis)

        tools_gw.set_config_parser('my_button_2', 'rb_dinamic', f'{rb_dinamic}', prefix=True)
        tools_gw.set_config_parser('my_button_2', 'rb_static', f'{rb_static}', prefix=True)
        tools_gw.set_config_parser('my_button_2', 'plot', f'{plot}', prefix=True)
        tools_gw.set_config_parser('my_button_2', 'table', f'{table}', prefix=True)
        tools_gw.set_config_parser('my_button_2', 'base_column', f'{base_column}', prefix=True)
        tools_gw.set_config_parser('my_button_2', 'base_value', f'{base_value}', prefix=True)
        tools_gw.set_config_parser('my_button_2', 'target_value', f'{target_value}', prefix=True)
        #tools_gw.set_config_parser('my_button_2', 'target_values', f'{target_values}', prefix=True, file_name="plotmanager")
        # tools_gw.set_config_parser('my_button_2', 'target_selected_values', f'{target_selected_values}', prefix=True, file_name="plotmanager")
        tools_gw.set_config_parser('my_button_2', 'xaxis', f'{xaxis}', prefix=True)
        tools_gw.set_config_parser('my_button_2', 'yaxis', f'{yaxis}', prefix=True)

    def get_config(self):
        rb_dinamic = tools_gw.get_config_parser('my_button_2', 'rb_dinamic', "user", "session", prefix=True)
        rb_static = tools_gw.get_config_parser('my_button_2', 'rb_static', "user", "session", prefix=True)
        plot = tools_gw.get_config_parser('my_button_2', 'plot',  "user", "session",prefix=True)
        table = tools_gw.get_config_parser('my_button_2', 'table',  "user", "session",prefix=True)
        base_column = tools_gw.get_config_parser('my_button_2', 'base_column',  "user", "session",prefix=True)
        base_value = tools_gw.get_config_parser('my_button_2', 'base_value', "user", "session",prefix=True)
        # target_column = tools_gw.get_config_parser('my_button_2', 'target_column',  "user", "plotmanager",prefix=True)
        # target_selected_values = tools_gw.get_config_parser('my_button_2', 'target_selected_values',  "user", "plotmanager",prefix=True)
        target_value = tools_gw.get_config_parser('my_button_2', 'target_value', "user", "session",prefix=True)
        xaxis = tools_gw.get_config_parser('my_button_2', 'xaxis',  "user", "session", prefix=True)
        yaxis = tools_gw.get_config_parser('my_button_2', 'yaxis',  "user", "session", prefix=True)
        print(f"dinamic {rb_dinamic}")
        print(f"{rb_static=}")

        self.populate_table_child_cmb()

        tools_qt.set_checked(self.dlg_seaborn, self.dlg_seaborn.rb_dinamic, checked=self.set_boolean(rb_dinamic))
        tools_qt.set_checked(self.dlg_seaborn, self.dlg_seaborn.rb_static, checked=self.set_boolean(rb_static))
        tools_qt.set_selected_item(self.dlg_seaborn, self.dlg_seaborn.cmb_plottype, plot)
        tools_qt.set_selected_item(self.dlg_seaborn, self.dlg_seaborn.cmb_nameTable, table)
        tools_qt.set_selected_item(self.dlg_seaborn, self.dlg_seaborn.cmb_basecolumn, base_column)
        tools_qt.set_selected_item(self.dlg_seaborn, self.dlg_seaborn.cmb_basevalue, base_value)
        tools_qt.set_widget_text(self.dlg_seaborn, self.dlg_seaborn.le_target, target_value)
        self.populate_base_child_cmb()
        # self.populate_target_child_cmb()
        # self.populate_selected_lw()
        tools_qt.set_selected_item(self.dlg_seaborn, self.dlg_seaborn.cmb_xaxis, xaxis)
        tools_qt.set_selected_item(self.dlg_seaborn, self.dlg_seaborn.cmb_yaxis, yaxis)


    def set_boolean(self,param, default=True):
        """
        Receives a string and returns a bool
            :param param: String to cast (String)
            :param default: Value to return if the parameter is not one of the keys of the dictionary of values (Boolean)
            :return: default if param not in bool_dict (bool)
        """

        bool_dict = {True: True, "TRUE": True, "True": True, "true": True,
                     False: False, "FALSE": False, "False": False, "false": False}

        return bool_dict.get(param, default)