''' This version of the temperature probe utilizes default python libraries
to achieve the necessary data organization. The latest run time for this file is:

Probes		Time(s)		Date
2		2.2		04-06-2016

This driver is the current template for the Ballo Mare thermostat.
'''

# Import necessary libraries
import csv
import os
import glob
import time
from exportLogs import *
import paho.mqtt.client as mqtt
# Adds w1-gpio and w1-therm modules to kernel
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

# Initialize some globals
now = time.strftime('%H:%M')
today = time.strftime('%Y-%m-%d')
from globalVars import base_dir, home_dir, install_dir, base_channel
#base_dir = '/sys/bus/w1/devices/'

# Collects the list of desired devices from the devices.csv file
device_config = list()
with open(home_dir + install_dir + 'devices.csv') as f:
	device_config = list(csv.reader(f))
device_config = device_config[1:]

# Appends a list of device files to the device_config file
for row in device_config:
	row.append(base_dir+row[1]+'/w1_slave')

# Returns lines for a single file
def read_temp_raw(file):
	f = open(file, 'r')
	lines = f.readlines()
	f.close()
	return lines

# Collects the temperature from single w-1 file
def read_temps(file):
	lines = read_temp_raw(file)
	if lines[0].strip()[-3:] != 'YES':
		return('No Data')
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string)/1000
		return temp_c

# Drives data collection
# Checks for logfiles directory. If it doesn't exist it is created
if not os.path.isdir(home_dir + 'logfiles'):
	os.mkdir('logfiles')

# Write to a csv file
header = ['Date', 'Time', 'Sensor', 'TempC']

# Creates an output string to send via email
output = list()

# Connects to broker for MQTT publishing
client = mqtt.Client("tempMonitor")
client.connect("localhost")
client.publish(base_channel+'thermostat/lastrun', today+' '+now, retain = True)

# Iterates through the devices collected from the config file
for file in device_config:
	current_file = home_dir + 'logfiles/'+file[1]+'log.csv'

	# Checks current device is connected to the pi
	if not os.path.isfile(file[-1]):
		print('Device ' + file[0] + ' (' + file[1] + ')  not found in ' + base_dir + '\n--Continuing to next sensor--')
		continue

	# Adds condition for invalid data to continue to the next sensor
	tempFromDev = read_temps(file[-1])
	if tempFromDev == 'No Data':
		print('No good data found for ' + file[0] + ' (' + file[1] + '). Check connection')
		continue

	# Opens the log file for current device or creates one if blank
	with open(current_file, 'a+') as f:
		writer = csv.writer(f)
		reader = csv.reader(f)

		# Collects the temperature and stores it as a writable line
		temp_row = today,now,file[0],tempFromDev+float(file[2])
#		print(temp_row)

		# Checks if the file is empty
		if os.path.getsize(current_file) == 0:
			writer.writerow(header)
			writer.writerow(temp_row)

		# Collects the latest temperature from the current log file
		f.seek(0)
		last_temp = float(list(reader)[-1][-1])
		f.seek(0)

		# Writes temperature if +/-0.25 degrees from last recorded temp
		client.publish(base_channel+'thermostat/'+file[0],temp_row[3], retain = True)
		if (temp_row[3] > last_temp+.25) | (temp_row[3] < last_temp-.25):
			writer.writerow(temp_row)
			output.append(temp_row)
		else:
			continue
#			print('Current temp: '+str(temp_row[3])+' ---not written---\n')

if output:
	print(*output,sep='\n')
	exportLogs()

