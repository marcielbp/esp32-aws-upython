import machine
import network
import time
from umqtt.robust import MQTTClient

def cb(topic,msg):
    print(msg)

HOST = b'a3gpjj3vmsemcn-ats.iot.us-east-1.amazonaws.com'
 #el host debe ser reemplazado por uno propio
#TOPIC = bytes('ESP32', 'utf-8')
TOPIC = b'ESP32'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("ARiDa-Lab","!K1@B25#3&s")
time.sleep(4)

cert="8851cd3501-certificate.pem.crt"
key="8851cd3501-private.pem.key"
root="AmazonRootCA3.pem"

with open(cert, 'rb') as f:
    certf = f.read()
print(certf)

with open(key, 'rb') as f:
    keyf = f.read()
print(keyf)

with open(root, 'rb') as f:
    rootf = f.read()
print(rootf)

time.sleep(1)

conn = MQTTClient(client_id=TOPIC, server=HOST, port=8883, ssl=True, ssl_params={"cert":certf, "key":keyf})

conn = MQTTClient(client_id=TOPIC, server=HOST, port=8883, ssl=False)
conn.set_callback(cb)
conn.connect()
conn.subscribe(TOPIC)

msg='mensaje'

while True:
  connection.publish(topic=TOPIC, msg=msg, qos=0)
  sleep(2)