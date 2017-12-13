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
	

	
#Function to convert inches to mm
def convert_mm(inches):
	inches = float(inches)
	mm = round(inches * 25.4)
	return int(mm)
	

#Make axes for temp and rainfall. Plot data. 
def two_scales(ax1, dates, rainfall_data, temp_data, c1, c2):
	ax2 = ax1.twinx()
	ax1.set_ylabel("Rainfall (mm)")
	ax1.bar(dates, rainfall_data, width=1.0, color=c1, label='Rainfall')
	
	ax2.plot(dates, temp_data, color=c2, alpha=0.7, label='Temperature')
	ax2.set_ylabel("Temperature (c)")
	return ax1, ax2
	
	
def read_csv(filename):
	with open(filename) as f:
		reader = csv.reader(f)
		header_row = next(reader)
		
		dates, rainfall, mean_temp = [], [], []
		for row in reader:
			try:
				current_date = datetime.strptime(row[0], "%Y-%m-%d")
				rain = convert_mm(row[19])
				temp = convert_celsius(row[2])
			except ValueError:
				print(current_date, 'missing data')
			else:
				rainfall.append(rain)
				mean_temp.append(temp)
				dates.append(current_date)
		return dates, rainfall, mean_temp
	

dates, rainfall, mean_temp = read_csv("data\sitka_weather_2014.csv")
fig, ax = plt.subplots(dpi=128, figsize=(10,6))
ax1, ax2 = two_scales(ax, dates, rainfall, mean_temp, 'skyblue', 'red')

#Set up how dates are displayed
mondays = mdates.WeekdayLocator(mdates.MONDAY)
months = mdates.MonthLocator()
myFmt = mdates.DateFormatter("%B %d %Y")

#format x_axis
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
title = "Climate graph"
plt.title(title, fontsize=24)
plt.legend(loc='upper right')
ax1.legend(loc='upper left')
plt.show()