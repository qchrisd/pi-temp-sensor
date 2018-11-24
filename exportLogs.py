'''This script exports the data log files stored in the folder ~/logfiles.
Formats the data into one continuous CSV file timestamping it with the date
and time (YYYYMMDD-HHmm).
'''

# Import necessary libraries
import csv
import os
import glob
import time

# Checks for the target directory. If it does not exist it is created. Also looks for
# old export files and deletes them if present.
def prepareExportDirectory(home_dir, logfile_dir):
	if not os.path.isdir(home_dir + logfile_dir):
		os.mkdir(logfile_dir)
		return
	for f in glob.glob(home_dir + logfile_dir +'/*Export.csv'):
		os.remove(f)

# Opens a new file based on the time of export and writes all log files in ./Logs into
# one file located in the directory ./exports.
def exportLogs():

	from globalVars import base_dir, home_dir, logfile_dir

	prepareExportDirectory(home_dir,logfile_dir)

	logs = glob.glob(home_dir+'logfiles/*')
	today = time.strftime('%Y%m%d-')
	now = time.strftime('%H%M')
	with open(home_dir+ logfile_dir +'/'+ today + now +'Export.csv', 'a+') as f:
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

if __name__ == "__main__":
	exportLogs()
