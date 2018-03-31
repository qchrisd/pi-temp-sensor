# Import necessary libraries
import csv
import os
import glob
import time

# Initializes necessary files
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Initialize some globals
now = time.strftime('%H:%M:%S')
today = time.strftime('%Y-%m-%d')
base_dir = '/sys/bus/w1/devices/'
device_config = list()
with open('/home/pi/devices.csv') as f:
	device_config = list(csv.reader(f))
device_config = device_config[1:]

# Appends a list of device files to the device_config file
for row in device_config:
		row.append(base_dir+row[1]+'/w1_slave')

#debugging
print("Config File Listings:")
for row in device_config:
	print(row)
print

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

#debugging driver
for row in device_config:
	print(today+' '+now+' '+row[0]+': '+str(read_temps(row[2])))

# Write to a csv file
header = ['Date', 'Name', 'Sensor', 'Temp C']
for file in device_config:
	with open('/home/pi/'+file[1]+'log.csv', 'a+') as f:
		writer = csv.writer(f)
		reader = csv.reader(f)
		try:
			next(reader)
		except:
			writer.writerow(header)
		temp_row = today,now,file[0],read_temps(file[2])
		writer.writerow(temp_row)
		print('written to /home/pi/'+file[1]+'log.csv')
