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
def getCurrentDevices():
	currentDevs = [os.path.basename(x) for x in glob.glob(base_dir+'28*')]
	return currentDevs

# Collects the list of devices in the device config file
def getConfigDevices():
	deviceConfig = []
	with open(home_dir + 'pi-temp-sensor/devices.csv') as f:
		deviceConfig = list(csv.reader(f))[1:]
	return deviceConfig

# Compares the list of serial numbers in the devices.csv
# and returns those not listed in the newDevs list
def getNewDevices():
	currentDevs = getCurrentDevices()
	deviceConfig = getConfigDevices()

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

# Compares the list of serial numbers in the devices.csv
# and returns those that have no directory in the base_dir
def getMissingConfigDevices():
	currentDevs = getCurrentDevices()
	deviceConfig = getConfigDevices()

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

# Compares the list of serial numbers in the devices.csv
# and returns those that have a directory in the base_dir
def getConnectedConfigDevices():
	currentDevs = getCurrentDevices()
	deviceConfig = getConfigDevices()

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

# Displays modularly the status of all temp devices associated with the master
def printStatus():
	# Outputs the list of devices currently connected to the pi
	print('\n-- Devices Currently Connected to the host --\n')
	for row in getConnectedConfigDevices():
		print(row)

	# Outputs list of devices in the devices.csv list not connected
	missingDevs = getMissingConfigDevices()
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

# Drives the output
printStatus()
