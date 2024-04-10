# ipydialog: Dialogs Using ipywidgets & ipyleaflet

**NOTE**: This package is a WIP

**ipywidgets**, also known as jupyter-widgets or simply widgets, are
[interactive HTML widgets](https://github.com/jupyter-widgets/ipywidgets/blob/main/docs/source/examples/Index.ipynb)
for Jupyter notebooks and the IPython kernel.

**ipyleaflet** is a Jupyter / Leaflet bridge enabling [interactive maps](https://github.com/jupyter-widgets/ipyleaflet/tree/master) in the Jupyter notebook.

This package contains a python implimentation of dialog mediator classes. These mediator objects facilitate communication between component objects, which utilise ipywidget core interactive widgets. The package was inspired by [ipyfilechooser](https://github.com/crahan/ipyfilechooser/tree/master) and [leafmap](https://github.com/opengeos/leafmap) and was designed as a solution to a specific project involving a custom ipleaflet WidgetControl implimentation for geospatial data.

## Core Dialog Classes

- FileDialog [IN PROGRESS]

Currently only the FileDialog dialog is being added. This dialog acts a local file explorer and selection widget within Jupyter Notebooks/IPython context.

### Screenshots


![Screenshot 1](https://github.com/AndyRids/ipydialog/examples/images/FileDialog_Browse.png)

![Screenshot 2](https://github.com/AndyRids/ipydialog/examples/images/FileDialog_Selected.png)

![Screenshot 3](https://github.com/AndyRids/ipydialog/examples/images/FileDialog_Selected_Properties.png)

- WidgetControlDialog [TBC]

The WidgetControlDialog provides a custom toolbar dialog for an ipyleaflet Map. The toolbar uses the FileDialog to add geospatial data from local files to a Map.

