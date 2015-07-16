#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool
from collections import OrderedDict
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter
import math
import numpy as np
from django.conf import settings
import os
from bokeh.models.mappers import LinearColorMapper

def _covert_matplotlib_palette_to_bokeh(name="rainbow"):
    '''
    See names here:
    http://matplotlib.org/examples/color/colormaps_reference.html
    '''
    import matplotlib as plt
    import matplotlib.cm as cm
    import numpy as np
    colormap =cm.get_cmap(name) #choose any matplotlib colormap here
    bokehpalette = [plt.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]
    return LinearColorMapper(bokehpalette)

def plot3():
    df = pd.read_csv(os.path.join(settings.BASE_DIR,'data/Land_Ocean_Monthly_Anomaly_Average.csv'))
    # List all the tools that you want in your plot separated by comas, all in one string.
    TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,previewsave"

    # Add the tools to your figure
    t = figure(x_axis_type = "datetime", width=800, height=600,tools=TOOLS)

    # Process data
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df[['anomaly','datetime']]
    df['moving_average'] = pd.rolling_mean(df['anomaly'], 12)

    # Line colors and legend
    t.line(df['datetime'], df['anomaly'], color='lightgrey', legend='anom')
    t.line(df['datetime'], df['moving_average'], color='red', legend='avg')
    # The hover tools doesn't render datetime appropriately. We'll need a string.
    df["datetime_s"]=df[["datetime"]].applymap(str)

    # To reference variables in the hover box, we'll need to use bokeh.ColumnDataSource instead of a pd.DataFrame
    source = ColumnDataSource(df)

    # Change plotting.line to get values from ColumnDataSource, name the renderer that you want to have the hover activated
    t.line('datetime', 'anomaly', color='lightgrey', legend='anom', source=source)
    t.line('datetime', 'moving_average', color='red', legend='avg', source=source, name="mva")

    # Set hover tool
    hover = t.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ("anomaly", "@anomaly"),
        ("datetime", "@datetime_s"),
    ])
    hover.renderers = t.select("mva")

    # Copy your style from the previous exercise
    xformatter = DatetimeTickFormatter(formats=dict(months=["%b %Y"], years=["%Y"]))
    t.xaxis[0].formatter = xformatter
    t.xaxis.major_label_orientation = math.pi/4
    t.yaxis.axis_label = 'Anomaly(ºC)'
    t.legend.orientation = "bottom_right"
    t.grid.grid_line_alpha=0.2
    t.toolbar_location=None

    return t

def plot4():
    from bokeh.models import HoverTool, BoxSelectTool
    TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,hover,previewsave"
    x = np.arange(-5, 5, 0.1)
    y = np.arange(-5, 5, 0.1)
    xx, yy = np.meshgrid(x, y, sparse=True)
    z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)

    p = figure(x_range=[-5, 5], y_range=[-5, 5])
    p.image(image=[z], x=[-5], y=[-5], dw=[10], dh=[10],
            dilate=True, tools=TOOLS,
            color_mapper=_covert_matplotlib_palette_to_bokeh())

    p.yaxis.axis_label = 'Label for Y'
    p.xaxis.axis_label = 'Label for X'
    p.title = 'Dummy 2D plot!'
    return p
