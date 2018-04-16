'''This script exports the data log files stored in the folder ~/logfiles.
Formats the data into one continuous CSV file timestamping it with the date
and time (YYYYMMDD-HHmm).
'''

# Import necessary libraries
import csv
import os
import glob
import time

# Initialize some globals
today = time.strftime('%Y%m%d-')
now = time.strftime('%H%M')
base_dir = '/home/pi/'
logs = glob.glob(base_dir+'logfiles/*')

# Checks for the target directory. If it does not exist it is created.
if not os.path.isdir(base_dir+'exports/'):
	os.mkdir('exports')

# Opens a new file based on the time of export and writes all log files in ./Logs into
# one file located in the directory ./exports.
with open(base_dir+'exports/'+today+now+'export.csv', 'a+') as f:
	header = ['Date','Time','Sensor','TempC']
	writer = csv.writer(f)
	reader = csv.reader(f)
	try:
		next(reader)
	except:
		writer.writerow(header)
	for file in logs:
		with open(file) as temp_file:
			temp_list = list(csv.reader(temp_file, dialect='excel'))
			writer.writerows(temp_list[1:])
	print('Data exported at '+today+now)

