''' This script creates a client to listen on the MQTT broker for commands on the ballomare/command channel
'''

# Iports necessary dependencies
import glob
import os
import time
import paho.mqtt.client as mqtt
from globalVars import base_channel
from commands import triage

# Create the client
client = mqtt.Client('ballomareListener')

# on_connect protocol to ensure a connection
def on_connect(client, userdata, flags, result_code):
	if result_code != 0:
		print('Connection refused')
	else:
		print('Connection successful')

# on_message protocol that activates commands.py script
def on_message(client, userdata, message):
	if str(message.payload.decode('utf8')) == 'kill':
		print('Kill recieved. Disconnecting from broker...')
		client.disconnect()
		print('Disconnection from broker successful.')
	else:
		triage(message)

# Sets the connect and message functions for the client
client.on_connect = on_connect
client.on_message = on_message

# Connect to the localhost broker (bridged to cloud broker)
client.connect('localhost', keepalive = 60)

# Subscribes to the commands topic
client.subscribe(base_channel+'command/#')

# Starts the loop indefinitely to listen for commands
client.loop_forever()
