"""This driver utilizes the PANDAS library to achieve the necessary
data organization. The latest run time for this file to collect data:

Probes		Time(s)		Date
2		6		04-05-2018

This particular driver may not be the optimal solution in terms of
efficiency however the program is much more readable.
"""

# Import necessary libraries
import csv
import os
import time
import pandas
import re

# Adds w1-gpio and w1-therm modules to linux kernel
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Initialize some globals for more readable code
now = time.strftime('%H:%M')
today = time.strftime('%Y-%m-%d')
base_dir = '/sys/bus/w1/devices/'

# Reads the current devices.csv config file into a PANDAS dataframe
device_config = pandas.read_csv('/home/pi/pi-temp-sensor/devices.csv')

# Appends a list of device files to the device_config dataframe as a new column 'file'
device_config['file'] = base_dir+device_config['Serial Number']+'/w1_slave'

# Collects the temperature from a single w-1 slave given the file's location
def find_temp(file):
	temp_regex = re.compile(r'\d{5}')
	with open(file, 'r') as f:
		lines = f.read()
	temp_string = temp_regex.search(lines)
	return float(temp_string.group())/1000

# Drives the data collection
# Writes to a csv file
header = ['Date', 'Time', 'Sensor', 'TempC']
for index, row in device_config.iterrows():

	# Checks for the current device in the devices directory and continues to next device if not found
	if not os.path.isfile(str(row['file'])):
		print('Device '+str(row['Name'])+' in '+base_dir+'\n--Continuing to next sensor--')
		continue

	# Opens the log file for the current device
	log_file = '/home/pi/pi-temp-sensor-pandas/logfiles/'+row['Serial Number']+'log.csv'
	with open(log_file, 'a+') as f:
		writer = csv.writer(f)
		reader = csv.reader(f)

		# Creates the temporary row to write to the log file
		temp_row = today,now,row['Name'],find_temp(row['file'])

		# Writes header file and the temp_row to only empty files then continues to next device
		if os.path.getsize(log_file) == 0:
			writer.writerow(header)
			writer.writerow(temp_row)
			continue

		# Reads the current log file and returns the last temp recorded
		current_data = pandas.read_csv(log_file)
		last_temp = float(current_data.tail(1)['TempC'])

		# Checks to see if the current temperature is +/-0.5 degrees
		outside_range = (temp_row[-1] <= (last_temp-.5)) | (temp_row[-1] >= (last_temp+.5))

		# Checks to see if the last recorded temperature is outside the reference range
		# If yes, write a line in the log file, else do nothing
		if outside_range:
			writer.writerow(temp_row)
		else:
			continue
