
import resource
import swarm
import apikey
import threading
import logging
import socket
import time
import sys
import json

class participationThread(threading.Thread):
    def __init__(self, api, resource, swarms, onMessage=False,
            onPresence=False, onError=False):
        self.api = api
        self.resource = resource
        self.swarms = swarms
        self.onMessage=onMessage
        self.onPresence=onPresence
        self.onError=onError
        if len(swarms) < 1:
            logging.error('At least one swarm must be specified')
            return
        #This needs to be a raw socket so that we can send HTTP headers, but
        #still independently read and write to the socket.
        self.sock = socket.socket()
        self.sock.settimeout(1.0)
        self.sock.connect((self.api.server, 80))
        req = "POST /stream?"
        for swrm in self.swarms:
            req += "swarm_id="+swrm.id+"&"
        req += "resource_id="+(resource.id)
        self.sock.sendall(req+" HTTP/1.1\r\n"
                "Host: "+self.api.server+"\r\n"
                "Accept-Encoding: identity\r\n"
                "x-bugswarmapikey: "+self.api.participation+"\r\n"
                "transfer-encoding: chunked\r\n"
                "connection: keep-alive\r\n"
                "\r\n")
        #TODO - actually wait for headers here, instead of guessing...
        # needs to have a non-blocking timeout...
        #time.sleep(1)
        self.fd = self.sock.makefile()
        resp = self.checkResp()
        if not resp[0] or resp[0] != 200:
            logging.error('Error trying to open stream: '+resp[1])
            return
        self.connected = True

        #Send a blank HTTP chunk to allow BUGSwarm to connect to the proxy
        self.sock.sendall('2\r\n\n\n\r\n')

        self.running = True
        threading.Thread.__init__(self)
        self.start()

    def checkResp(self):
        line = self.fd.readline()
        result = False
        response = ""
        while line != '\r\n':
            if line.find("HTTP/") != -1:
                result = int(line.split(' ')[1])
            response += line
            line = self.fd.readline()
        response = response.replace('\r\n','\\r\\n')
        return (result,response)

    def run(self):
        while self.running:
            try:
                txt = self.fd.readline()
            except socket.timeout:
                pass
            except socket.error:
                logging.error('Socket closed unexpectedly')
                self.connected = False
                self.running = False
                self.sock.close()
                return
            self.parse(txt)
        self.sock.sendall('0\r\n\r\n')
        self.sock.close()

    def stop(self):
        self.running = False
        self.join()

    def produce(self, msg, dest_swarm=False):
        if not dest_swarm:
            dest_swarm = self.swarms[0]
        stripped_payload = msg.strip()
        msg = '{"message":{"to":["'+dest_swarm.id+\
            '"],"payload":' + stripped_payload + '}}\r\n'
        size = hex(len(msg))[2:] + "\r\n"
        chunk = msg + "\r\n"
        self.sock.sendall(size+chunk)

    def parse(self, txt):
        if len(txt) < 6 or txt[0] != '{':
            #disregard if too small for json
            return
        txt = txt.rstrip()
        packet = json.loads(txt)
        if packet.has_key('presence') and self.onPresence:
            self.onPresence(packet['presence'])
        elif packet.has_key('message') and self.onMessage:
            self.onMessage(packet['message'])
        elif packet.has_key('error') and self.onError:
            self.onError(packet['errors'])
        else:
            logging.debug('SWARM: '+txt)




