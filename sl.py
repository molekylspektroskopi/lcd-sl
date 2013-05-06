#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
from datetime import datetime
from pylcdsysinfo import BackgroundColours, TextColours, TextAlignment, TextLines, LCDSysInfo
from collections import deque
from time import sleep
from os import stat
import re
from suds.client import suds
from suds.client import Client

class SLAPI(object):
    def __init__(self, uri):
        self.client = Client(uri)
 
    def get_departures(self, station):
        ret = []
        for metro in self.client.service.GetDepartures(station).Metros.Metro:
#            print metro
            if metro.DisplayRow1 is None:
                ret.append(" No Update ")
            else:
                ret.append(re.sub(' +', ' ', unicode(re.sub('11  (A|K)', '\\1', metro.DisplayRow1) + " ")))
            if metro.DisplayRow2 is None:
                ret.append(" No Update ")
            else:
                ret.append(re.sub(' +', ' ', unicode(re.sub('11 (A|K)', '\\1', metro.DisplayRow2) + " ")))
        return ret
d = LCDSysInfo()
d.clear_lines(TextLines.ALL, BackgroundColours.BLACK)
d.dim_when_idle(False)
d.set_brightness(127)
d.save_brightness(127, 255)
d.set_text_background_colour(BackgroundColours.BLACK)
try:
    api = SLAPI('http://www1.sl.se/realtidws/RealTimeService.asmx?wsdl')
    last_check = 0
    r = re.compile(r'([^ ]+ ([0-9]{2}:[0-9]{2}|[0-9]{1,2} min))') 
    while(True):
        if time.time() - last_check >= 15:
            c = api.get_departures(9301)
            m = re.match(r, c[1])
            if m:
                s1 = m.group(0)
            else:
                s1 = c[1]
            m = re.match(r, c[3])
            if m:
                s2 = m.group(0)
            else:
                s2 = c[3]
            last_check = time.time()
            try:
                f.close()
            except:
                pass
            f = open('yw', 'r')
            yw = f.read()
            f.close()
        d.display_text_on_line(1, c[0], False, TextAlignment.LEFT, TextColours.ORANGE)
        d.display_text_on_line(2, s1, False, TextAlignment.LEFT, TextColours.ORANGE)
        d.display_text_on_line(3, c[2], False, TextAlignment.LEFT, TextColours.ORANGE)
        d.display_text_on_line(4, s2, False, TextAlignment.LEFT, TextColours.ORANGE)
        d.display_text_on_line(6, yw, False, TextAlignment.CENTRE, TextColours.CYAN)
#        c[1].rotate(-1)
#        c[3].rotate(-1)
        sleep(0.05)
except KeyboardInterrupt:
    exit()
