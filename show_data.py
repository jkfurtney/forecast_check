from matplotlib.collections import LineCollection
import glob
import matplotlib
import datetime
import numpy as np
import pylab as plt

rtimes, rt, rp = np.loadtxt("data/data.txt").T
rtimes = map(datetime.datetime.fromtimestamp, rtimes)
rtimes = matplotlib.dates.date2num(rtimes)
fig,axis  = plt.subplots()

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
plt.show()
