import csv
import os
import sys
from datetime import datetime

from matplotlib import pyplot as plt
import matplotlib.dates as mdates



#Function to convert fahrenheit to degrees celsius
def convert_celsius(fahrenheit):
	fahrenheit = int(fahrenheit)
	celsius = round((fahrenheit-32)*5/9, 0)
	return int(celsius)



#function to extract data from .csv file	
def read_csv(filename):
	with open(filename) as f:
		reader = csv.reader(f)
		header_row = next(reader)
		
		"""
		#print out index of the headers
		for index, column_header in enumerate(header_row):
			print(index, column_header)
		"""
			
		dates, highs, lows = [], [], []
		for row in reader:
			try:
				current_date = datetime.strptime(row[0], "%Y-%m-%d")
				high = convert_celsius(row[1])
				low = convert_celsius(row[3])
			except ValueError:
				print(current_date, 'missing data')
			else:
				highs.append(high)
				lows.append(low)
				dates.append(current_date)
		return dates, highs, lows
	
	
	
#Prompt user for which data set to load. 
files = os.listdir('data')
for i in range(0, len(files)):
	print('{} - {}'.format(i, files[i]))	
user_input = input("Which data set do you want to see? (Enter number) ")

#Load the data set
try:
	data_path = files[int(user_input)]
	dates, highs, lows = read_csv(os.path.join('data', data_path))
	
except Exception:
	sys.exit("Invalid Input")
	
"""
#Plot Data
fig = plt.figure(dpi=128, figsize=(10,6))
plt.plot(dates, highs, c='red')

#Format Plot
plt.title("Daily high temperatures for Sitka, July 2014", fontsize=24)
plt.xlabel('', fontsize=16)
fig.autofmt_xdate()
plt.ylabel("Temperature (C)", fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=9)

plt.show()
"""
#Using the filename, get year and locaton info for use in graph title
data_info = data_path.split('_')
year = data_info[-1].replace('.csv', '')
location = " ".join(data_info[0:-1]).title()

#Set up how dates are displayed
mondays = mdates.WeekdayLocator(mdates.MONDAY)
months = mdates.MonthLocator()
myFmt = mdates.DateFormatter("%B %d %Y")

#plot data
fig, ax = plt.subplots(dpi=128, figsize=(10,6))
ax.plot(dates, highs, c='red', alpha=0.5, label='Highs')
ax.plot(dates, lows, c='blue', alpha=0.5, label='Lows')
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

#format x_axis
#ax.set_xticks(dates)
#ax.locator_params(axis='x', nbins=12)
ax.xaxis.set_major_formatter(myFmt)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(mondays)
ax.autoscale_view()
ax.grid(True)
fig.autofmt_xdate()

#format legend, labels, title
plt.ylabel("Temperature (C)", fontsize=16)
plt.xlabel('', fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=9)
title = "Daily high and low temperatures for {} - {}".format(location, year)
plt.title(title, fontsize=24)
plt.legend(loc='upper left')

plt.show()

		
