# plotmanager_qgis_plugin

## TABLE OF CONTENTS
Here after you will find all the information you need to getting started with Plotmanage plugin<br>

	1- Requirements
	2- Install
    3- Create Graph
    4- Customize

## REQUIREMENTS
To work with Plotmanage plugin you will need:

QGIS: Geoprocessing software<br>
Giswater: QGIS plugin
## INSTALL
Download the project in PATH_OF_YOUR_QGIS_USER\python\plugins
## CREATE GRAPH
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