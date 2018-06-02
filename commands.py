''' Commands for ballomare thermostat

Methods should 
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
