"""This driver utilizes the PANDAS library to achieve the necessary
data organization. The average run time for this file to collect data:

Probes		Time(s)		Date
2		6		04-03-2018

This particular driver may not be the optimal solution in terms of
efficiency however the program is much more readable.
"""


# Import necessary libraries
import csv
import os
import time
import pandas
import re

# Initializes necessary files
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Initialize some globals
now = time.strftime('%H:%M')
today = time.strftime('%Y-%m-%d')
base_dir = '/sys/bus/w1/devices/'

# Attempts to impliment pandas CSV reader
device_config = pandas.read_csv('/home/pi/pi-temp-sensor/devices.csv')

# Appends a list of device files to the device_config file as a new column 'file'
device_config['file'] = base_dir+device_config['Serial Number']+'/w1_slave'

# Collects the temperature from a single w-1 slave
def find_temp(file):
	temp_regex = re.compile(r'\d{5}')
	with open(file, 'r') as f:
		lines = f.read()
	temp_string = temp_regex.search(lines)
	return float(temp_string.group())/1000

# Driver Debugging
print('Compiled with no issue')
for f in device_config['file']:
	print(find_temp(f))

# Write to a csv file
header = ['Date', 'Time', 'Sensor', 'TempC']
for index, row in device_config.iterrows():
	with open('/home/pi/pi-temp-sensor-pandas/logfiles/'+row['Serial Number']+'log.csv', 'a+') as f:
		writer = csv.writer(f)
		reader = csv.reader(f)
		try:
			next(reader)
		except:
			writer.writerow(header)
		temp_row = today,now,row['Name'],find_temp(row['file'])
		writer.writerow(temp_row)
		print('written to /home/pi/pi-temp-sensor-pandas/logfiles'+row['Serial Number']+'log.csv')
