from datetime import datetime
import os
from random import randint
from DynamicKey5 import *
import time

from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Process

appID   = "YOUR APPID"
appCertificate     = "YOUR APPCERTIFICATE"
unixts = int(time.time())
uid = 0
randomint = 2147483699
expiredts = 0

schedule_table = {}

def loadConfig():
    time = []
    channel = []

    for line in open('config.txt').readlines():
        if line.startswith('2018'):
            time.append(line.strip('\n'))
        elif line.startswith('i'):
            channel.append(line.strip('\n'))

    if len(time) == len(channel) and len(time):
        for i in range(len(time)):
            schedule_table[channel[i]] = time[i]
    else:
        print "config file error!"

def startRecording(channelName):
    p = Process(target=run_proc, args=(channelName,))
    p.start()

def run_proc(channelName):
    ChannelKey = generateMediaChannelKey(appID, appCertificate, channelName, unixts, randomint, uid, expiredts)
    cmd = "./recorder_local --appId YOUR APPID --channel {0} --appliteDir ../../bin --channelKey {1} --idle 6000 &".format(channelName, ChannelKey)
    print time.strftime("%Y-%m-%d %H:%M:%S")
    print cmd
#    os.system(cmd)

if __name__ == '__main__':
    loadConfig()
    scheduler = BackgroundScheduler()

    for key, value in schedule_table.items():
        # set run time 5 mins before schedule time
        run_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.mktime(time.strptime(value, "%Y-%m-%d %H:%M:%S")) - 300))
        print run_time + ': ' + key
        scheduler.add_job(startRecording, 'date', run_date=run_time, args=[key])
    scheduler.start()

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
