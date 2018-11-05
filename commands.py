''' Commands for ballomare thermostat

Methods should be titled by topic, each level separated by an underscore.
'''

# Imports name of the module for dynamic method calling
self = __import__(__name__)

''' Decodes the message and splits it into the topic and payload '''
def decode_message(message):
	# gets topic, splits it into levels and discards ballomare/command
	topic = message.topic.split('/')
	topic = topic[2:]

	# parses command into a string
	payloadstr = str(message.payload.decode('utf-8'))

	# returns variables
	return payloadstr, topic

''' Triage command that calls the appropriate method '''
def triage(message):
	# splits the message into usable parts
	payloadstr, topic = decode_message(message)

	# prepares the method name based off the topic
	method_name = ''
	for level in topic:
		method_name += level+'_'
	method_name = method_name.rstrip("_")

	# calls the method described by topic level and catches errors
	try:
		method = getattr(self, method_name)
		method(payloadstr, topic, message)
	except:
		print('No method of topic: ' + method_name + ' found')

''' Print command on .../printtext topic '''
def printtext(payloadstr, topic, message):
	print(payloadstr)

''' Refreshes the status of the temperatures on topic .../thermostat/status '''
def thermostat_refresh_status(payloadstr, topic, message):
	# imports the status script for use
	import status

	# publishes the current status to the ballomare/thermostat/status topic
	status.publishMQTT(status.getStatus(),"ballomare/thermostat/status")
	print('Status published.')

''' Refreshes the temperatures '''
def thermostat_refresh_temperature(payloadstr, topic, message):
	# imports os module and globals
	import os
	from globalVars import home_dir,install_dir

	# runs the temp monitor script
	os.system('python3 '+ home_dir + install_dir + 'temperatureMonitor.py')
	print('Refreshed temperatures.')
