#!/usr/bin/python
from BUGswarm import apikey
from BUGswarm import resource
from BUGswarm import participation
import psutil
from ifconfig import ifconfig
import RPi.GPIO as GPIO
import logging
import time
import sys

logging.basicConfig(level=logging.DEBUG)
INTERVAL = 5.0
CAPABILITIES = 2
gpio_list = [0, 1, 4, 7, 8, 9, 10, 11, 14, 15, 17, 18, 21, 22, 23, 24, 25]
gpio_value = {}
gpio_direction = {}

if len(sys.argv) != 2:
    logging.error('usage: '+sys.argv[0]+' <resource name>')
    sys.exit(1)

GPIO.setmode(GPIO.BCM)
for i in gpio_list:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.LOW)
    gpio_value[i] = "low" 
    gpio_direction[i] = "out" 
api = apikey.apikey("demo","buglabs55")
res = resource.getResourceByName(api,sys.argv[1])
swarms = res.getSwarms()

print "Press Control-C to quit\r\n"


def presence(obj):
    logging.info("presence from "+obj['from']['resource'])
def message(obj):
    global gpio_list
    global gpio_value
    global gpio_direction
    if "name" in obj['payload'] and obj['payload']['name'] == "gpio_setup":
        pin = int(obj['payload']['feed']['pin'])
        direction = obj['payload']['feed']['direction']
        pull = obj['payload']['feed']['pull']
        logging.info("Setting GPIO "+str(pin)+" to mode "+direction+" with pullup "+pull)
        if not pin in gpio_list:
            logging.error("Invalid GPIO number "+pin)
            return
        gpio_direction[pin] = direction
        if direction == "in":
            direction = GPIO.IN
        elif direction == "out":
            direction = GPIO.OUT
        else:
            logging.error("Invalid direction "+direction)
            return
        if pull == "up":
            pull = GPIO.PUD_UP
        elif pull == "down":
            pull = GPIO.PUD_DOWN
        else:
            pull = GPIO.PUD_OFF
        GPIO.setup(pin, direction, pull_up_down=pull)
        sendGPIOStatus()

    if "name" in obj['payload'] and obj['payload']['name'] == "gpio_output":
        pin = int(obj['payload']['feed']['pin'])
        value = obj['payload']['feed']['value']
        logging.info("Setting GPIO "+str(pin)+" "+value)
        if not pin in gpio_list:
            logging.error("Invalid GPIO number "+pin)
            return
        gpio_value[pin] = value
        if value == "high":
            value = GPIO.HIGH
        elif value == "low":
            value = GPIO.LOW
        else:
            logging.error("Invalid value "+value)
            return
        GPIO.output(pin, value)
        sendGPIOStatus()
    
    if "name" in obj['payload'] and obj['payload']['name'] == "gpio_toggle":
        pin = int(obj['payload']['feed']['pin'])
        logging.info("toggling GPIO "+str(pin))
        if not pin in gpio_list:
            logging.error("Invalid GPIO number "+pin)
            return
        if gpio_value[pin] == "high":
            gpio_value[pin] = "low"
            GPIO.output(pin, GPIO.LOW)
        elif gpio_value[pin] == "low":
            gpio_value[pin] = "high"
            GPIO.output(pin, GPIO.HIGH)
        else:
            logging.error("Invalid value "+value)
            return
        sendGPIOStatus()
    
    if "name" in obj['payload'] and obj['payload']['name'] == "gpio_input_toggle":
        pin = int(obj['payload']['feed']['pin'])
        logging.info("toggling GPIO input "+str(pin))
        if not pin in gpio_list:
            logging.error("Invalid GPIO number "+pin)
            return
        if gpio_direction[pin] == "out":
            gpio_direction[pin] = "in"
            GPIO.setup(pin, GPIO.IN)
        elif gpio_direction[pin] == "in":
            gpio_direction[pin] = "out"
            GPIO.setup(pin, GPIO.OUT)
        else:
            logging.error("Invalid value "+value)
            return
        sendGPIOStatus()

    if "name" in obj['payload'] and obj['payload']['name'] == "gpio_read":
        for pin in gpio_list:
            if gpio_direction[pin] == "in":
                gpio_value = GPIO.input(pin)
        sendGPIOStatus()

def error(obj):
    logging.info("error "+str(obj['errors']))

pt = participation.participationThread(api,res, swarms,
        onPresence=presence, onMessage=message, onError=error)
def sendGPIOStatus():
    global gpio_list
    global gpio_value
    global gpio_direction
    message = '{"name":"gpio","feed":['
    for pin in gpio_list:
        message += '{"pin":'+str(pin)+',"direction":"'+gpio_direction[pin]+'","value":"'+gpio_value[pin]+'"},'
    message = message[:-1]
    message += ']}'
    pt.produce(message)


try:
    idx = 0
    sendGPIOStatus()
    while(True):
        idx = idx + 1
        net_before = psutil.network_io_counters(pernic=True)['eth0']
        disk_before = psutil.disk_io_counters()
        time.sleep(INTERVAL)
        net_after = psutil.network_io_counters(pernic=True)['eth0']
        disk_after = psutil.disk_io_counters()
        disk_usage = psutil.disk_usage('/').percent
        disk_free = psutil.disk_usage('/').free
        disk_read = (disk_after.read_bytes - disk_before.read_bytes)/INTERVAL
        disk_write = (disk_after.write_bytes - disk_before.write_bytes)/INTERVAL
        sent_bytes = (net_after.bytes_sent - net_before.bytes_sent)/INTERVAL
        recv_bytes = (net_after.bytes_recv - net_before.bytes_recv)/INTERVAL
        cpu = psutil.cpu_percent()
        ip = ifconfig('eth0')
        pt.produce('{"name":"Network","feed":{'+
                '"addr":"'+ip['addr']+
                '","hwaddr":"'+ip['hwaddr']+
                '","sentBps":'+str(sent_bytes)+
                ',"recvBps":'+str(recv_bytes)+'}}')
        pt.produce('{"name":"Disk","feed":{'+
                '"readBps":'+str(disk_read)+
                ',"writeBps":'+str(disk_write)+
                ',"free":'+str(disk_free)+
                ',"usage":'+str(disk_usage)+'}}')
        pt.produce('{"name":"CPU","feed":{'+
                '"utilization":'+str(cpu)+'}}')
        if idx%CAPABILITIES == 0:
            pt.produce('{"capabilities": {"feeds": ["Network","Disk","CPU","GPIO"]}}')
except KeyboardInterrupt:
    pass
pt.stop()
