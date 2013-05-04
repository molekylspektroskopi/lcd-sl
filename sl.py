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
                ret.append(deque(" No Update "))
            else:
                ret.append(deque(re.sub(' +', ' ', unicode(re.sub('11 (A|K)', '\\1', metro.DisplayRow2) + " "))))
        return ret
d = LCDSysInfo()
d.clear_lines(TextLines.ALL, BackgroundColours.BLACK)
d.dim_when_idle(False)
d.set_brightness(127)
d.save_brightness(127, 255)
d.set_text_background_colour(BackgroundColours.BLACK)
col = TextColours.ORANGE
try:
    api = SLAPI('http://www1.sl.se/realtidws/RealTimeService.asmx?wsdl')
    last_check = 0
    while(True):
        if time.time() - last_check >= 15:
            c = api.get_departures(9301)
            s = ", ".join(c[1].split(',')[0:2])
            s2 = ", ".join("".join(c[3]).split(',')[0:2])
            last_check = time.time()
            try:
                f.close()
            except:
                pass
            f = open('yw', 'r')
        d.display_text_on_line(1, c[0], False, TextAlignment.LEFT, col)
        d.display_text_on_line(2, "".join(s), False, TextAlignment.LEFT, col)
        d.display_text_on_line(3, c[2], False, TextAlignment.LEFT, col)
        d.display_text_on_line(4, "".join(s2), False, TextAlignment.LEFT, col)
        d.display_text_on_line(6, f.read(), False, TextAlignment.CENTRE, TextColours.CYAN)
        f.seek(0)
#        c[1].rotate(-1)
#        c[3].rotate(-1)
        sleep(0.05)
except KeyboardInterrupt:
    exit()
