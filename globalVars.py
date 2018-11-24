""" This script contains the global variables that are shared among all
scripts in the pi-temp-sensor project

"""

# base_dir is the directory where the device directories live
base_dir = '/sys/bus/w1/devices/'

# home_dir is the directory where the install_dir is located
home_dir = '/home/pi/'

# install_dir is the name of the directory where the code is installed.
# leave off the leading "/", but include the ending "/"
install_dir = 'pi-temp-sensor/'

# Home level of the MQTT channel
base_channel = 'rasqi/'
