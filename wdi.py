
# coding: utf-8

# In[210]:


from ipywidgets import interact


# In[13]:


import pandas as pd
import numpy as np


# In[201]:


from bokeh.io import show, output_notebook, push_notebook
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs, Dropdown, TextInput

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

output_notebook()


# In[14]:


from io import BytesIO


# In[15]:


import zipfile as zf


# In[16]:


from urllib.request import urlopen


# In[17]:


url = urlopen("http://databank.worldbank.org/data/download/WDI_csv.zip")


# In[18]:


wdi_zip = zf.ZipFile(BytesIO(url.read()))


# In[19]:


wdi_zip.namelist()


# In[59]:


df = pd.read_csv(wdi_zip.open('WDIData.csv'))


# In[60]:


df.shape


# In[90]:


df


# In[62]:


available_countries = list(df['Country Name'].unique())
available_countries.sort()


# In[74]:


available_indicators = list(df['Indicator Code'].unique())
available_indicators.sort()


# In[86]:


def make_dataset(country, indicator):
    return df[(df['Country Name'] == country) & (df['Indicator Code'] == indicator)].T


# In[118]:


def style(p):
        # Title 
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p


# In[182]:


def make_plot(src, column_names):
    # Blank plot with correct labels
    p = figure(plot_width = 700, plot_height = 700, 
              title = column_names[1],
              x_axis_label = column_names[0], y_axis_label = column_names[1])
    p.line(column_names[0], column_names[1], source=src)
    p = style(p)
    return p


# In[188]:


def update(attr, old, new):
    # Get the list of carriers for the graph
    country_to_plot = [country_selection.labels[i] for i in 
                        country_selection.active]
    indicator_to_plot = [indicator_selection.labels[i] for i in indicator_selection.active]
    # Make a new dataset based on the selected carriers and the 
    # make_dataset function defined earlier
    new_src = make_dataset(country_to_plot, indicator_to_plot)
    
    # Convert dataframe to column data source
    new_src = ColumnDataSource(new_src)

    # Update the source used the quad glpyhs
    src.data.update(new_src.data)


# In[91]:


country = 'Australia'
indicator = 'SP.URB.TOTL'
by_country = make_dataset(country, indicator)


# In[107]:


by_country


# In[174]:


indicator_name = by_country[2:3]
indicator_name = indicator_name.T.reset_index()['Indicator Name']
indicator_name = indicator_name[0]


# In[179]:


series_data = by_country[4:62]


# In[180]:


series_data = series_data.reset_index()
series_data.columns = ['Year', indicator_name]


# In[183]:


p = make_plot(ColumnDataSource(series_data), series_data.columns)
show(p)


# In[191]:


def form_menu_group(list):
    return [(x,x) for x in list]


# In[209]:


def country_change_handler(attr, old, new):
    print (country_selection.value)


# In[192]:


form_menu_group(available_countries)


# In[208]:


#country_selection = CheckboxGroup(labels=available_countries, active = [0])
country_selection = Dropdown(label="Country", button_type="success", menu = form_menu_group(available_countries))
country_selection.on_change('value', country_change_handler)
country_selection.on_click(country_change_handler)
indicator_selection = CheckboxGroup(labels=available_indicators, active = [0])
text_input = TextInput(value="default", title="Label:")
show(WidgetBox(country_selection, indicator_selection, text_input))


# In[186]:


[country_selection.labels[i] for i in country_selection.active]

