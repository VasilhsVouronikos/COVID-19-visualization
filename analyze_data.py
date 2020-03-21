import os
import sys
import csv
from datetime import datetime
from operator import itemgetter
import itertools

import matplotlib.pyplot as plt
import pandas as pd


dates=[]
values=[]

avarage_con=0
avarage_list=[]
last_date=""

file_to_open=sys.argv[1]


virus_development_data=[]
active_occ=[]
avrg_counter=0

def proscess_data(country):
	global virus_development_data
	with open(file_to_open+"/"+"COVID-19 Cases.csv") as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		row=[r for r in reader]
		for i in range(len(row)):
			curr_row=row[i]
			if(curr_row[1]==country):
					country_data=[]
					country_data.append(curr_row[0])
					country_data.append(curr_row[1])
					country_data.append(curr_row[3])
					country_data.append(curr_row[4])
					virus_development_data.append(country_data)
		csvfile.close()
	return virus_development_data


def show_confirmed(country):
	global active_occ
	data=proscess_data(country)
	for i in range(len(data)):
		curr=data[i]
		if(curr[2]=="Confirmed"):
			active=[]
			active.append((curr[0]))
			active.append((curr[2]))
			active.append((curr[3]))
			active_occ.append(active)
			
	active_occ.sort(key=itemgetter(1), reverse=True)
	active_occ.sort(key=lambda L: datetime.strptime(L[0], '%m/%d/%Y'))
	return active_occ


def visualize_active():
	global dates,values,avrg_counter,avarage_con

	print("---REAL VISUALIZATION OF COVID-19 DATA OF CONFIRMED CASES AROUND THE WORLD---\n\n")
	print ("press 0 to exit")
	print ("press 1 to continue\n")
	choice=int(input())
	
	while(choice!=0):
		if(choice==1):
			avrg_counter+=1
			country=input("Type a country\nType here:")
			country=search_for_upper(country)
			
			active=show_confirmed(country)
			for i in range(len(active)):
				curr=active[i]
				dates.append(curr[0])
				values.append(int(curr[2]))
			
			avarage_con+=values[len(values)-1]
			values.sort()
			dates = [pd.to_datetime(d) for d in dates]
			df=pd.DataFrame({'x': dates, 'y': values })
						
			last_date=dates[len(dates)-1]			
			
			plt.title('Evolution of confirmed cases '+country)
			plt.xlabel('date')
			plt.ylabel('cases')

			plt.plot( 'x', 'y', data=df, linestyle='-', marker='o')
			plt.show()

			del values[:]
			del dates[:]
			del virus_development_data[:]
			del active_occ[:]
			
			print ("---Continue with another country---\n")					
			print ("press 0 to exit")
			print ("press 1 to continue")	
						
			choice=int(input())
	else:
		av=avarage_con/avrg_counter
		print("avarage confirmed cases of countries you searched is:",av,"\nupdated up to:",last_date,"\n")
		print("Exiting")
	
	return
	

def search_for_upper(country):
	c_list=list(country)
	if(c_list[0].islower()):
		c=country.capitalize()
		return c
	else:
		return country

visualize_active()




