from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

def ex1(request):

    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
    p.line(x, y, legend="Temp.", line_width=2)

    script, div = components(p, CDN)

    return render(request, "plot1/ex1.html", {"bokeh_script":script, "bokeh_div":div})
