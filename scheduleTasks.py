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

schedule_table = {
"2018-07-01 12:55:00": 'i2672130092',
"2018-07-01 13:25:00": 'i2680272182',
"2018-07-01 11:25:00": 'i2721746229',
}

def startRecording(channelName):
    p = Process(target=run_proc, args=(channelName,))
    p.start()

def run_proc(channelName):
    ChannelKey = generateMediaChannelKey(appID, appCertificate, channelName, unixts, randomint, uid, expiredts)
    cmd = "./recorder_local --appId YOURAPPID --channel {0} --appliteDir ../../bin --channelKey {1} --idle 6000 &".format(channelName, ChannelKey)
    print cmd
    os.system(cmd)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()

    for key, value in schedule_table.items():
        scheduler.add_job(startRecording, 'date', run_date=key, args=[value])
    scheduler.start()

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
