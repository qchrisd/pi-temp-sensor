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

# Adds w1-gpio and w1-therm modules to kernel
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

# Initialize some globals
now = time.strftime('%H:%M')
today = time.strftime('%Y-%m-%d')
base_dir = '/sys/bus/w1/devices/'

# Collects the list of desired devices from the devices.csv file
device_config = list()
with open('/home/pi/pi-temp-sensor/devices.csv') as f:
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
	while lines[0].strip()[-3:] != 'YES':
		lines = read_temp_raw(file)
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string)/1000
		return temp_c

# Drives data collection
# Write to a csv file
header = ['Date', 'Time', 'Sensor', 'TempC']

# Iterates through the devices collected from the config file
for file in device_config:
	current_file = '/home/pi/logfiles/'+file[1]+'log.csv'
	# Checks current device is connected to the pi
	if not os.path.isfile(file[-1]):
		print('Device ' + file[1] + ' not found in ' + base_dir + '\n--Continuing to next sensor--')
		continue

	# Opens the log file for current device or creates one if blank
	with open(current_file, 'a+') as f:
		writer = csv.writer(f)
		reader = csv.reader(f)

		# Collects the temperature and stores it as a writable line
		temp_row = today,now,file[0],read_temps(file[-1])-float(file[2])
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
		if (temp_row[3] >= last_temp+.25) | (temp_row[3] <= last_temp-.25):
			writer.writerow(temp_row)
			print(temp_row)
		else:
			continue
#			print('Current temp: '+str(temp_row[3])+' ---not written---\n')
