#import necessary libraries
import csv
import os
import glob
import time

#initializes necessary files
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#initialize some globals
now = time.strftime('%H:%M:%S')
today = time.strftime('%Y-%m-%d')

#collects a list of temperature file names
base_dir = '/sys/bus/w1/devices/'
device_folders = list()
device_folders = glob.glob(base_dir + '28*')
devices = list()
for i in device_folders:
	devices.append(i[-15:])
	print(i[-15:])
device_files = list()
for i in device_folders:
	print('i = ' + i)
	device_files.append(i + '/w1_slave')


#debugging
print('Folders:')
print(device_folders)
print

#debugging
print('Files:')
print(device_files)
print

#returns lines for a single file
def read_temp_raw(file):
	f = open(file, 'r')
	lines = f.readlines()
	f.close()
	return lines

#debugging
#print(read_temp_raw(device_files[0]))

#collects the temperature from single w-1 file
def read_temps(file):
	lines = read_temp_raw(file)
	while lines[0].strip()[-3:] != 'YES':
		lines = read_temp_raw(file)
#		print(lines)
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
#		print(temp_string)
		temp_c = float(temp_string)/1000
		return temp_c

#debugging
#print(read_temps(device_files[0]))

###### DRIVER ########
data = open(today+'log.csv', "wb")
writer = csv.writer(data,escapechar="\\" ,quoting=csv.QUOTE_NONE)
header = 'Date','Time','Label','Temp C'
while True:
	data = open(today+'log.csv', "wb")
	writer.writerow(header)
	while True:
		for i in device_files:
			row = (time.strftime('%Y-%m-%d'),time.strftime('%H:%M:%S'),i[-24:-9],str(read_temps(i)))
			print(row)
			writer.writerow(row)




#	equals_pos = lines[1].find('t=')
#	if equals_pos != -1:
#		temp_string = lines[1][equals_pos+2:]
#		temp_c = float(temp_string)/1000
#		return temp_c
#while True:
#	print(str(read_temp())+' degrees C')
