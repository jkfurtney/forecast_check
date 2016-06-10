import os
import tempfile
import time
import urllib2
import json

key = os.getenv("KEY")
url = 'http://api.wunderground.com/api/{}/hourly10day/q/MSP.json'.format(key)

datafile = "data/data.txt"

def get_t_p():
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    temp_f = parsed_json['current_observation']['temp_f']
    pres_m = float(parsed_json['current_observation']['pressure_mb'])
    epoch = int(parsed_json ['current_observation'] ['observation_epoch'])
    f.close()
    return epoch, temp_f, pres_m

def log_t_p():

    try:
        epoch, t,p = get_t_p()
    except:
        print "failed to read t p"
        return

    print "got", epoch, t, p
    handle, tmp_name = tempfile.mkstemp(prefix="wx", text=True)
    f = os.fdopen(handle,"w")
    data = open(datafile, "r")
    buff = data.readlines()
    data.close()
    for line in buff:
        print >> f, line,
    print >> f, epoch, t, p

    # atomic file update
    f.flush()
    os.fsync(f.fileno())
    f.close()
    os.rename(tmp_name, datafile)

if __name__ == '__main__':

    while True:
        time.sleep(600)
        log_t_p()
