import pandas as pd
import numpy as np

from bokeh.io import show, output_notebook, push_notebook, curdoc
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, Dropdown, TextInput, Select

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.server.server import Server

# output_notebook()

from io import BytesIO

import zipfile as zf

from urllib.request import urlopen

from scripts.timeseries import timeseries_tab

# url = urlopen("http://databank.worldbank.org/data/download/WDI_csv.zip")
url = 'data/WDI_csv.zip'

# wdi_zip = zf.ZipFile(BytesIO(url.read()))
wdi_zip = zf.ZipFile(url)

wdi_zip.namelist()

df = pd.read_csv(wdi_zip.open('WDIData.csv'))


def modify_doc(doc):
    # Create each of the tabs
    tab1 = timeseries_tab(df)

    # Put all the tabs into one application
    tabs = Tabs(tabs = [tab1])
    doc.title = "World Development Indicator"
    doc.add_root(tabs)


'''
def form_menu_group(list):
    return [(x,x) for x in list]

def country_change_handler(attr, old, new):
    print (country_selection.value)

def indicator_change_handler(attr, old, new):
    print(indicator_selection.value)

form_menu_group(available_countries)

'''
# show(layout)

# curdoc().add_root(layout)
# curdoc().title="World Development Indicator"

# if __init__='__main__':
    
apps = {'/': Application(FunctionHandler(modify_doc))}

server = Server(apps, port=5000)
server.start()