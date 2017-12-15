import csv
import os
import sys
from datetime import datetime
from random import randint

from matplotlib import pyplot as plt
import matplotlib.dates as mdates


#Class to handle rainfall, temperature and data data for alternative monthly 
#display option
class DataHandler():
	def __init__(self, current_date):
		self.current_date = current_date
		self.months = [current_date]
		
		self.temperature_average = 0
		self.monthly_temperature_average = []
		
		self.rainfall_average = 0
		self.monthly_rainfall_average = []
		
		self.count = 0
	

	#add data from new line in csv file. If a new month is detected, calculate 
	#averages and store the information. 
	def add_data(self, date, rainfall, temperature):
		if self.current_date.month == date.month:
			self.rainfall_average += rainfall
			self.temperature_average += temperature
			self.count += 1
		else:
			self.months.append(date)
			self.find_monthly_averages(date, rainfall, temperature)

	
	#method that calculates the monthly average rainfall, temperature
	def find_monthly_averages(self, date, rainfall, temperature):
		self.monthly_rainfall_average.append(
			int(round(self.rainfall_average/self.count)))
		self.monthly_temperature_average.append(
			int(round(self.temperature_average/self.count)))
		self.count = 1
		self.temperature_average = temperature
		self.rainfall_average = rainfall
		self.current_date = date
		
	
	#Gets the average rainfall, temperature data after calculating for December
	def get_data(self):
		date = datetime(2014,12,1)
		self.find_monthly_averages(date, 0, 0)
		return self.months, self.monthly_temperature_average, self.monthly_rainfall_average
	
	def print_data(self):
		print("dates: {}".format(self.months))
		print("rainfall {}".format(self.monthly_rainfall_average))
		print("temperature {}".format(self.monthly_temperature_average))
		
			
		

#Test function to make date data
def make_date():
	date = []
	for i in range (1,13):
		new_date = datetime(2017,i, 1)
		date.append(new_date)
	return date
	
	
#Test function to make fake rainfall data
def make_rainfall():
	rainfall = []
	for i in range(1,13):
		rainfall.append(randint(0,100))
	return rainfall


#Test function to make fake temperatrue data
def make_temp():
	temp = []
	for i in range(0,12):
		temp.append(randint(0,50))
	print(temp)
	return temp
	

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
def two_scales(ax1, dates, rainfall_data, temp_data, c1, c2, graph_type):
	"""
	#function calls to make fake data
	dates = make_date()
	rainfall_data = make_rainfall()
	temp_data = make_temp()
	"""
	ax2 = ax1.twinx()
	ax1.set_ylabel("Rainfall (mm)")
	if graph_type:
		ax1.bar(dates, rainfall_data, width=20.0, color=c1, label='Rainfall')
	else:
		ax1.bar(dates, rainfall_data, width=1.0, color=c1, label='Rainfall')
	
	ax2.plot(dates, temp_data, color=c2, alpha=0.7, label='Temperature')
	ax2.set_ylabel("Temperature (c)")
	return ax1, ax2
	
	
def read_csv(filename):
	with open(filename) as f:
		reader = csv.reader(f)
		header_row = next(reader)
		
		dates, rainfall, mean_temp = [], [], []
		data_handler = DataHandler(datetime.strptime('2014-01-01', "%Y-%m-%d"))
		
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
				data_handler.add_data(current_date, rain, temp)
		
		
		message = "Do you want to display data as monthly averages? (y/n) "
		user_input = input(message)
		
		if(user_input == 'y'):
			dates, rainfall, mean_temp = data_handler.get_data()
			#data_handler.print_data()
			return dates, rainfall, mean_temp, True
		else:
			return dates, rainfall, mean_temp, False
	

dates, rainfall, mean_temp, graph_type = read_csv("data\sitka_weather_2014.csv")
fig, ax = plt.subplots(dpi=128, figsize=(10,6))
ax1, ax2 = two_scales(ax, dates, rainfall, mean_temp, 'skyblue', 'red', 
	graph_type)

#Set up how dates are displayed
mondays = mdates.WeekdayLocator(mdates.MONDAY)
months = mdates.MonthLocator()
#myFmt = mdates.DateFormatter("%B %d %Y")
myFmt = mdates.DateFormatter("%B %Y")

#format x_axis
ax.xaxis.set_major_formatter(myFmt)
ax.xaxis.set_major_locator(months)
#ax.xaxis.set_minor_locator(mondays)
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