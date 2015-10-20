#!/usr/bin/env python
# -*- coding: utf-8 -*-


import matplotlib as plt
import matplotlib.cm as cm
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models import CustomJS
from collections import OrderedDict
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter
import math
import numpy as np
from django.conf import settings
import os
from bokeh import palettes
from bokeh.models.widgets import Dropdown
from bokeh.io import vform
import ast
import json

def get_color_map_from_matplotlib(name):
    '''
    @param name: any matplotlib colormap
    http://matplotlib.org/examples/color/colormaps_reference.html
    '''
    colormap = cm.get_cmap(name)
    bokehpalette = [plt.colors.rgb2hex(m)
                    for m in colormap(np.arange(colormap.N))]
    return bokehpalette


def plot3():
    df = pd.read_csv(
        os.path.join(settings.BASE_DIR, 'data/Land_Ocean_Monthly_Anomaly_Average.csv'))
    # List all the tools that you want in your plot separated by comas, all in
    # one string.
    TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,hover,previewsave"

    # Add the tools to your figure
    t = figure(x_axis_type="datetime", width=800, height=600, tools=TOOLS)

    # Process data
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df[['anomaly', 'datetime']]
    df['moving_average'] = pd.rolling_mean(df['anomaly'], 12)

    # Line colors and legend
    t.line(df['datetime'], df['anomaly'], color='lightgrey', legend='anom')
    t.line(df['datetime'], df['moving_average'], color='red', legend='avg')
    # The hover tools doesn't render datetime appropriately. We'll need a
    # string.
    df["datetime_s"] = df[["datetime"]].applymap(str)

    # To reference variables in the hover box, we'll need to use
    # bokeh.ColumnDataSource instead of a pd.DataFrame
    source = ColumnDataSource(df)

    # Change plotting.line to get values from ColumnDataSource, name the
    # renderer that you want to have the hover activated
    t.line('datetime', 'anomaly', color='lightgrey',
           legend='anom', source=source)
    t.line('datetime', 'moving_average', color='red',
           legend='avg', source=source, name="mva")

    # Set hover tool
    hover = t.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ("anomaly", "@anomaly"),
        ("datetime", "@datetime_s"),
    ])
    hover.renderers = t.select("mva")

    # Copy your style from the previous exercise
    xformatter = DatetimeTickFormatter(
        formats=dict(months=["%b %Y"], years=["%Y"]))
    t.xaxis[0].formatter = xformatter
    t.xaxis.major_label_orientation = math.pi / 4
    t.yaxis.axis_label = 'Anomaly(ºC)'
    t.legend.orientation = "bottom_right"
    t.grid.grid_line_alpha = 0.2
    t.toolbar_location = None

    return t


def plot4():
    TOOLS = "resize,crosshair,pan,wheel_zoom,box_zoom,reset,tap,previewsave,box_select,poly_select,lasso_select,hover"
    x, y = np.mgrid[-50:50, -50:50]
    dist = np.hypot(x, y)  # Linear distance from point 0, 0
    z = np.cos(dist / (2 * np.pi))

    p = figure(x_range=[-50, 50], y_range=[-50, 50], tools=TOOLS)

    cm = get_color_map_from_matplotlib('autumn')
    p.image(image=[z], x=np.linspace(-50, 50, 100),
            y=np.linspace(-50, 50, 100),
            dw=[100], dh=[100],
            # palette=palettes.Spectral11)
            palette=cm)
    return p


def plot5():
    all_color_maps = sorted( m for m in plt.cm.datad if not m.endswith("_r"))
    TOOLS = "resize,crosshair,pan,wheel_zoom,box_zoom,reset,tap,previewsave,box_select,poly_select,lasso_select,hover"
    x, y = np.mgrid[-50:50, -50:50]
    dist = np.hypot(x, y)  # Linear distance from point 0, 0
    z = np.cos(dist / (2 * np.pi))

    def get_colors(name = 'rainbow'):
        cm = get_color_map_from_matplotlib(name)
        # get colors form 0 to 255
        colors = np.rint((len(cm)-1) * ((z.flatten() +1)/2))
        return [ cm[i] for i in colors.astype(int)]

    source = ColumnDataSource(
        data=dict(
            x = x.flatten(),
            y = y.flatten(),
            z = z.flatten(),
            # get color values from index 0..255
            colors = get_colors(),
        )
    )


    p = figure(tools=TOOLS,plot_width=800, plot_height=800)

    p.rect('x', 'y', 1, 1, source=source, color='colors', line_color=None)


    hover = p.select(dict(type=HoverTool))

    hover.tooltips ="""
        <div>
            <span style="font-size: 17px; font-weight: bold;">@z</span>
            <span style="font-size: 15px; color: #966;">[$index]</span>
        </div>
        <div>
            <span style="font-size: 15px;">(@x, @y)</span>
            <span style="font-size: 10px; color: #696;">($x, $y)</span>
        </div>
        """
    #  OrderedDict([
    #     ('coords', 'x=@x, y=@y'),
    #     ('value', 'z=@z'),
    # ])

    # Dropdown
    # function(source,cb_obj,cb_data)
    callback = CustomJS(args=dict(source=source), code="""
        var cmaps = %s;
        var data = source.get('data');
        var cm_chosen = cb_obj.get('action');
        data['colors'] = cmaps[cm_chosen];
        source.trigger('change');
    """%( ast.literal_eval(json.dumps( { c: get_colors(c)  for c in all_color_maps } ))) )

    menu = [(c,c) for c in all_color_maps]
    dropdown = Dropdown(label="Change colormap", type="primary",
                        default_value='rainbow', menu=menu, callback=callback)

    layout = vform(dropdown, p)
    return layout
