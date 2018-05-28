from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import Select
from bokeh.layouts import row, WidgetBox

def timeseries_tab(df):

    def make_dataset(country, indicator):
        by_country = df[(df['Country Name'] == country) & (df['Indicator Code'] == indicator)].T
        indicator_name = by_country[2:3]
        indicator_name = indicator_name.T.reset_index()['Indicator Name']
        indicator_name = indicator_name[0]
    
        series_data = by_country[4:62]
    
        series_data = series_data.reset_index()
        series_data.columns = ['Year', 'value']
        
        return ColumnDataSource(series_data), indicator_name
    
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
    
    def make_plot(src, indicator_name, country_name):
        # Blank plot with correct labels
        p = figure(plot_width = 700, plot_height = 700, 
                  title = country_name,
                  x_axis_label = 'Year', y_axis_label = indicator_name)
        p.line('Year', 'value', source=src)
        p = style(p)
        return p
    
    def update(attr, old, new):
        # Get the list of carriers for the graph
        # country_to_plot = [country_selection.labels[i] for i in 
        #                    country_selection.active]
        #indicator_to_plot = [indicator_selection.labels[i] for i in indicator_selection.active]
        country_to_plot = country_selection.value
        indicator_to_plot = indicator_selection.value
        # Make a new dataset based on the selected carriers and the 
        # make_dataset function defined earlier
        new_src, indicator_name = make_dataset(country_to_plot, indicator_to_plot)

        # Convert dataframe to column data source
        # = ColumnDataSource(new_src)

        # Update the source used the quad glpyhs
        src.data.update(new_src.data)
        p.yaxis.axis_label = indicator_name
        p.title.text = country_to_plot
        # indicator_name.data.update(new_indicator_name.data)

    available_countries = list(df['Country Name'].unique())
    available_countries.sort()

    available_indicators = list(df['Indicator Code'].unique())
    available_indicators.sort()

    country_selection = Select(options=available_countries, value='Australia',title='Country')
    country_selection.on_change('value', update)
    indicator_selection = Select(options=available_indicators, value='SP.URB.TOTL',title='Indicators')
    indicator_selection.on_change('value', update)

    country = 'Australia'
    indicator = 'SP.URB.TOTL'
    #by_country = make_dataset(country, indicator)


    src, indicator_name = make_dataset(country, indicator)
    p = make_plot(src, indicator_name, country)
    selection_layout = WidgetBox(country_selection, indicator_selection)
    layout = row(selection_layout,p)

    # Make a tab with the layout 
    tab = Panel(child=layout, title = 'Timeseries')

    return tab