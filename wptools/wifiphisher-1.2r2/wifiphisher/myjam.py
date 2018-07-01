#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import subprocess
import time
from __main__ import *
from constants import *

def mj1(ap_mac, channel, essid):
    subprocess.call("sudo iw dev wlp3s0b1mon2 del && sudo iw dev wlp3s0b1mon3 del && sudo iw dev wlp3s0b1mon4 del && sudo iw dev wlp3s0b1mon5 del && sudo iw dev wlp3s0b1mon6 del", shell=True)
    time.sleep(1)
    print("create mon interfaces")
    subprocess.call("sudo iw dev wlp3s0b1 interface add wlp3s0b1mon2 type monitor && sudo iw dev wlp3s0b1 interface add wlp3s0b1mon3 type monitor && sudo iw dev wlp3s0b1 interface add wlp3s0b1mon4 type monitor && sudo iw dev wlp3s0b1 interface add wlp3s0b1mon5 type monitor && sudo iw dev wlp3s0b1 interface add wlp3s0b1mon6 type monitor", shell=True)
    time.sleep(3)
    sys.exit()
    
