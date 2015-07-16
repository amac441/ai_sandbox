#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from . import views_util

# Bokeh
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

def ex1(request):
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
    p.line(x, y, legend="Temp.", line_width=2)

    script, div = components(p, CDN)
    return render(request, "plot1/ex1.html", {"bokeh_script":script, "bokeh_div":div})

def ex2(request):
    x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    y0 = [i**2 for i in x]
    y1 = [10**i for i in x]
    y2 = [10**(i**2) for i in x]

    # create a new plot
    p = figure(
       tools="pan,box_zoom,reset,save",
       y_axis_type="log", y_range=[0.001, 10**11], title="log axis example",
       x_axis_label='sections', y_axis_label='particles'
    )

    # add some renderers
    p.line(x, x, legend="y=x")
    p.circle(x, x, legend="y=x", fill_color="white", size=8)
    p.line(x, y0, legend="y=x^2", line_width=3)
    p.line(x, y1, legend="y=10^x", line_color="red")
    p.circle(x, y1, legend="y=10^x", fill_color="red", line_color="red", size=6)
    p.line(x, y2, legend="y=10^x^2", line_color="orange", line_dash="4 4")

    script, div = components(p, CDN)
    return render(request, "plot1/ex2.html", {"bokeh_script":script, "bokeh_div":div})

def ex3(request):
    p = views_util.plot3()
    script, div = components(p, CDN)
    return render(request, "plot1/ex3.html", {"bokeh_script":script, "bokeh_div":div})

def ex4(request):
    p = views_util.plot4()
    script, div = components(p, CDN)
    return render(request, "plot1/ex4.html", {"bokeh_script":script, "bokeh_div":div})
