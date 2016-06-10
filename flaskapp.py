from matplotlib.collections import LineCollection
import random
import StringIO
import glob
from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
import numpy as np
import datetime
import pylab as plt
app = Flask(__name__)
from mpld3 import fig_to_html


@app.route("/d3/")
def d3():
    rtimes, rt, rp = np.loadtxt("data/data.txt").T
    mask = np.logical_and(rtimes>1391000000, rtimes<1393000000)
    rtimes = rtimes[mask]
    rt = rt[mask]
    rtimes = map(datetime.datetime.fromtimestamp, rtimes)
    rtimes = matplotlib.dates.date2num(rtimes)
    fig, axis = plt.subplots()

    axis.xaxis_date()
    fig.autofmt_xdate()
    axis.plot_date(rtimes, rt, "-",linewidth=3, color="black")

    forecast_list = []
    for fname in glob.glob("data/forecast.1391*.txt"):
        stamp = fname.split(".")[1]
        times, tempa = np.loadtxt(fname).T
        times = map(datetime.datetime.fromtimestamp, times)
        times = matplotlib.dates.date2num(times)

        points = np.array([times, tempa]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap=plt.get_cmap("jet"),
                            norm=plt.Normalize(0, 1))
        lc.set_array(np.linspace(0,1,len(times)))
        lc.set_linewidth(1)
        axis.add_collection(lc)

        axis.plot_date(times, tempa, "-", linewidth=2)



    return fig_to_html(fig)


@app.route("/png/")
def hello():

    rtimes, rt, rp = np.loadtxt("data/data.txt").T
    rtimes = map(datetime.datetime.fromtimestamp, rtimes)
    rtimes = matplotlib.dates.date2num(rtimes)
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.xaxis_date()
    fig.autofmt_xdate()

    forecast_list = []
    for fname in glob.glob("data/forecast.*.txt"):
        stamp = fname.split(".")[1]
        times, tempa = np.loadtxt(fname).T
        times = map(datetime.datetime.fromtimestamp, times)
        times = matplotlib.dates.date2num(times)

        points = np.array([times, tempa]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap=plt.get_cmap("jet"),
                            norm=plt.Normalize(0, 1))
        lc.set_array(np.linspace(0,1,len(times)))
        lc.set_linewidth(1)
        axis.add_collection(lc)

        axis.plot_date(times, tempa, "-", linewidth=0)

    axis.plot_date(rtimes, rt, "-",linewidth=1, color="black")

    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


if __name__ == "__main__":
    app.run(debug=True)
