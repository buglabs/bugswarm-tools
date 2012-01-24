#!/usr/bin/python
from optparse import OptionParser
from lib import swarmtoolscore
import sys
import httplib
import os
import time
import signal
import serial
import random
ser = serial.Serial('/dev/ttyACM0')  # open first serial port
print ser.portstr       # check which port was really used
ser.flush()
ser.write('AT*E2OTR?\r\n')      # write a string
ser.flush()
reading = ser.readline()
reading = ser.readline()
readings = reading.split(',')
temp = readings[len(readings)-1]
print temp
conn = None;

def usage(script_name):
    print "%s [produce] \n"%(script_name)
    print "Use '%s [method] --help' for a method's usage and options."%(script_name)
    sys.exit()

def signal_handler(signal, frame):
        global conn
        conn.close()        
        sys.exit(0)

def produce(hostname, api_key, swarm_id, resource_id, raw):
    global conn
    conn = httplib.HTTPConnection(hostname)
    sel = "/stream?swarm_id=%s&resource_id=%s"%(swarm_id, resource_id)
    conn.putrequest("POST", sel)
    conn.putheader("x-bugswarmapikey", api_key)
    conn.putheader("transfer-encoding", "chunked")
    conn.putheader("connection", "keep-alive")
    conn.endheaders()
    
    #Sleep required to allow the swarm server time to respond with header
    time.sleep(1)

  #Send a blank http body to open the connection
    conn.send('2\r\n\n\n\r\n')
    stripped_payload = '{"capabilities": {"feeds": ["Temperature", "Acceleration", "Location"]}}'.strip()
    msg = '{"message": {"to": ["' + swarm_id + '"], "payload": ' + stripped_payload + '}}'
    size = hex(len(msg))[2:] + "\r\n"
    chunk = msg + "\r\n"
    conn.send(size+chunk)
 
    #Execute further messages
    while True:
       try:
           ser.write('AT*E2OTR?\r\n')      # write a string
           ser.flush()
           reading = ''
           while (not ',' in reading):
               reading = ser.readline()
           readings = reading.split(',')
           temp = readings[len(readings)-1].rstrip('\r\n')
           payload = '{"name":"Temperature", "feed":{"Temperature" : "'+temp+'"}}'
           print payload
           if (len(payload) < 1):
                break
           stripped_payload = payload.rstrip('\n')
           msg = '{"message": {"to": ["' + swarm_id + '"], "payload": ' + stripped_payload + '}}'
           size = hex(len(msg))[2:] + "\r\n"
           chunk = msg + "\r\n"
           conn.send(size+chunk)
	   payload ='{"name":"Acceleration", "feed":{"x":'+str(random.random())+', "y": '+str(random.random())+', "z": '+str(random.random())+'}}'
           stripped_payload = payload.rstrip('\n')
           msg = '{"message": {"to": ["' + swarm_id + '"], "payload": ' + stripped_payload + '}}'
           size = hex(len(msg))[2:] + "\r\n"
           chunk = msg + "\r\n"
           conn.send(size+chunk)
           payload = '{"name":"Location", "feed":{"latitude": "40.724'+str(random.randint(10,99))+'","longitude": "-73.9965'+str(random.randint(10,99))+'"}}'
	   print payload
           stripped_payload = payload.rstrip('\n')
           msg = '{"message": {"to": ["' + swarm_id + '"], "payload": ' + stripped_payload + '}}'
           size = hex(len(msg))[2:] + "\r\n"
           chunk = msg + "\r\n"
           conn.send(size+chunk)
           time.sleep(2)
       except Exception as e:
               print "some sort of problem", e

def main():
    server_info = swarmtoolscore.get_server_info()
    print server_info
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "produce":
        signal.signal(signal.SIGINT, signal_handler)
        opt_usage = "usage: \n  ./produce.py %s SWARM_ID RESOURCE_ID [options]"%(sys.argv[1])
        opt_usage += "\n\n  *SWARM_ID: The ID of the swarm to produce to." \
                    +"\n  *RESOURCE_ID: The ID of the resource to produce with." \
                    +"\n\n  NOTE: Data may also be produced by piping into the function (DATA | ./produce.py produce SWARM_ID RESOURCE_ID [options])."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-r", action="store_true", dest="raw", help="Require that messages be sent in the raw formatting as specified in the 'Sending Messages' section at http://developer.bugswarm.net/participation_api.html.", default=False)
        (options, args) = parser.parse_args()
        if len(args) != 3:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        swarm_id = args[1]
        resource_id = args[2]
        produce(server_info["hostname"], keys['participation'], swarm_id, resource_id, options.raw)
    else:
        usage(sys.argv[0])

main()
