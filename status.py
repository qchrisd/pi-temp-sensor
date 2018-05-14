""" This script provides the framework for collecting the status of the
currently connected suite of devices and provides a method to display that
status as terminal output.

"""

# Import some libraries
import glob
import csv
import os

# Initiate some globals
from globalVars import base_dir, home_dir
#baseDir = '/sys/bus/w1/devices/'

# Collects a list of currently connected devices
currentDevs = [os.path.basename(x) for x in glob.glob(base_dir+'28*')]

# Collects the list of devices in the device config file
deviceConfig = []
with open(home_dir + 'pi-temp-sensor/devices.csv') as f:
	deviceConfig = list(csv.reader(f))[1:]

# Compares the list of serial numbers in the devices.csv file
# and stores those files in the newDevs list
def getNewDevices():
	newDevs = []
	for device in currentDevs:
		found = False
		for row in deviceConfig:
			if device == row[1]:
				found = True
				break
		if not found:
			newDevs.append(device)
	return newDevs

def getMissingDevices():
	notConnected = []
	for row in deviceConfig:
		found = False
		for device in currentDevs:
			if device == row[1]:
				found = True
				break
		if not found:
			notConnected.append(row)
	return notConnected

def getConnected():
	connected = []
	for row in deviceConfig:
		found = False
		for device in currentDevs:
			if device == row[1]:
				found = True
				break
		if found:
			connected.append(row)
	return connected

def getStatus():
	# Outputs the list of devices currently connected to the pi
	print('\n-- Devices Currently Connected to the host --\n')
	for row in getConnected():
		print(row)

	# Outputs list of devices in the devices.csv list not connected
	missingDevs = getMissingDevices()
	if not missingDevs:
		print('\n-- All Devices Connected --\n')
	else:
		print('\n-- Devices Not Connected --\n')
		for device in missingDevs:
			print(device)

	# Outputs the list of devices not in the devices.csv list
	newDevs = getNewDevices()
	if not newDevs:
		print('\n-- No New Devices Found --\n')
	else:
		print('\n-- New Unnamed Devices Found --\n')
		for device in newDevs:
			print(device)
	print()

# Displays the status of the probes connected to the host
getStatus()
