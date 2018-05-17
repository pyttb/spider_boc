# -*- coding: utf-8 -*-
import time

from scrapy.cmdline import execute
import sys
import os
import logging
reload(sys)
sys.setdefaultencoding('utf-8')

def demo():
    pass

import datetime
starttime = time.time()
#long running
time.sleep(1)
endtime = time.time()
print (endtime-starttime)