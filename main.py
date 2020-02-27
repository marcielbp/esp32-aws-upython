import machine
import network
import time
from simple import MQTTClient

DISCONNECTED = 0
CONNECTING = 1
CONNECTED = 2
HOST = 
"a3gpjj3vmsemcn-ats.iot.eu-west-1.amazonaws.com"
"a3gpjj3vmsemcn-ats.iot.us-east-1.amazonaws.com"
TOPIC = "esp32"
state = DISCONNECTED
connection = None

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def pub_msg(msg):
    global connection
    connection.publish(topic=TOPIC, msg=msg, qos=0)
    print('Sending: ' + msg)

def run():
    global state
    global connection

    while True:
        while state != CONNECTED:
            try:
                state = CONNECTING
                connection = MQTTClient(client_id=TOPIC, server=HOST, port=8883, keepalive=10000, ssl=True, ssl_params={"certfile":"ESP32.cert.pem", "keyfile":"ESP32.private.pem", "ca_certs":"root-CA.crt"})
                connection.connect()
                state = CONNECTED
            except:
                print('Could not establish MQTT connection')
                time.sleep(0.5)
                continue

        print('MQTT LIVE!')

        while state == CONNECTED:
            msg = '{"device_id":"some_id", "data":"some_data"}'
            pub_msg(msg)
            time.sleep(2.0)


nets = wlan.scan()
for net in nets:
    if net.ssid == 'ARiDa-Lab':
        print(net.ssid +" was found!")
        wlan.connect(net.ssid, auth=(WLAN.WPA2, "!K1@B25#3&s"), timeout=5000)
        while not wlan.isconnected():
            machine.idle()
        print('Connected to '+ net.ssid)
        run()
        break
