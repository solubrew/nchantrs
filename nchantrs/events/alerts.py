"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""
from os.path import abspath, dirname, join
import datetime as dt
import logging
from kahndor import kahndor
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')
ONE_HOUR_SECONDS = 3600
DEFAULT_NOTIFICATION_TIMEOUT = 10
import time
from plyer import notification
if __name__ == '__main__':
    while True:
        notification.notify(title='ALERT!!!', message='Take a break! It has been an hour!', timeout=DEFAULT_NOTIFICATION_TIMEOUT)
        time.sleep(ONE_HOUR_SECONDS)