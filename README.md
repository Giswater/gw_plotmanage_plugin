## WELCOME TO GISWATER PROJECT (gw_plotmanage_plugin)

Here after you will find all the information you need to getting started with Plotmanage plugin.

## TABLE OF CONTENTS
Here after you will find all the information you need to getting started with gw_plotmanage_plugin<br>

	1- Requirements
	2- Install
	3- Graphs
	4- License
	5- Thanks to

## REQUIREMENTS
You will need QGIS (Geoprocessing software) and also to have Giswater plugin installed.

For more information about to getting started with Giswater<br> you can visit the README.md file of one the main repositories:

https://github.com/Giswater/docs<br>
https://github.com/Giswater/giswater_qgis_plugin.<br>
https://github.com/Giswater/giswater_dbmodel.<br>

## INSTALL
In this point you will learn how to install gw_plotmanage_plugin.<br>

To install the plugin you will need to download the source code. You can download the .ZIP file directly from this repository. Once you have de .ZIP file you must extract it in the QGIS plugins folder*:

`C:\Users\user\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`<br>

*This is the location of the QGIS plugins folder in Windows. The location may be diffrent in other operating systems.

After that you can open QGIS and a Giswater project and activate the plugin. To activate the plugin you must find _Plugins_ in the QGIS Menu Toolbar and then go to _Manage and Install Plugins_ > _Installed_ and click the checkbox for _gw_plotmanage_plugin_.


## GRAPHS

### GRAPH TYPE
You can select between HTML5 which will open a tap in your browser with the graph, and PNG will open a new window with the graph. <br>
![img.png](imgs/img.png)
### PLOT TYPE
This combo loads the plot types from the selected graph type.<br>
HTML5: <br>
![img.png](imgs/plottype.png)
### TABLE
Populates the available tables to get the data<br>
![img.png](imgs/table.png)
### BASE COLUMN
Select the base column<br>
![img.png](imgs/base_column.png)
### BASE VALUE
Select the base value<br>
![img.png](imgs/base_value.png)
### TARGET COLUMN
Select the target column. This will select the column that you will get the values you want to compare<br>
![img.png](imgs/targetcolumn.png)
### TARGET QUERY FILTER
Here you will put the values you want to get to compare<br>
![img.png](imgs/query_filter.png)
### XAXIS
Specifies the column that will be in x axis
<br>
![img.png](imgs/xaxis_yaxis.png)
### YAXIS
Specifies the column that will be in y axis
<br>
![img.png](imgs/xaxis_yaxis.png)
## CUSTOMIZE
![img.png](imgs/Customize.png)
### TITLE
#### XAXIS
Selects the title for the xaxis
#### YAXIS
Selects the title for the yaxis
#### TARGET
Selects the title for the target(Only in Plot Type: Line plot with scrollbar)
### MARKER
#### WIDTH
Selects the width from the line.<br>
Recommended:2
#### TYPE
Specifys wich type of line you want. <br>
Available: 
['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']



## LICENSE
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. See LICENSE file for more information.


## THANKS TO
GITS-BarcelonaTech University<br>
Aigües de Mataró<br>
Aigües de Girona<br>
Aigües de Blanes<br>
Aigües del Prat<br>
Aigües de Vic<br>
Aigües de Castellbisbal<br>
Aigües de Banyoles<br>
Figueres de Serveis, S.A<br>
Prodaisa<br>
Sabemsa<br>
Consorci Aigües de Tarragona<br>

-----------------------------------
