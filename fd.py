import os
import tempfile
import time
import urllib2
import json
key = os.getenv("KEY")
url = 'http://api.wunderground.com/api/{}/hourly10day/q/MSP.json'.format(key)

def get_forecast():
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    forecast_list = parsed_json["hourly_forecast"]
    stimestamp = str(forecast_list[0]['FCTTIME']['epoch'])

    time_list = []
    temp_list = []
    for forecast in forecast_list:
        timestamp = int(forecast ['FCTTIME'] ['epoch'])
        time_list.append(timestamp)
        temp_list.append( float(forecast ['temp'] ['english']))
    return stimestamp, time_list, temp_list


def write_forecast():
    try:
        st, time_list, temp_list = get_forecast()
    except:
        print "failure in get_forecast"
        return

    filename = "_forecast.%s.txt" % st
    f = open(filename, "w")
    for time, temp in zip(time_list, temp_list):
        print >> f, "%i %lf" % (time, temp)
    f.flush()
    os.fsync(f.fileno())
    f.close()
    os.rename(filename, filename[1:])


if __name__ == '__main__':

    while True:
        time.sleep(12*60*60)
        write_forecast()
