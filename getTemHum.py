#!/usr/bin/python

import argparse
import psycopg2 as pg
import numpy as  np
import time
import FuncRawData2 as frd
import matplotlib.pyplot as plt
import scipy.signal as sps
import csv

lenNames  =  ['LenEmfiB', 'LenEmfiS', # 0 1
'Len1B', 'Len2B', 'Len3B', 'Len4B', 'Len5B', # 2 3 4 5 6
'LenTemp', 'LenHum',  # 7 8
'LenSpO2', 'LenSpO2HR', #  9 10 
'Lenp1S', 'Lenp2S', 'Lenp3S', 'Lenp4S', #  11 12 13 14 
'LenX', 'LenY', 'LenZ'] # 15 16 17

class ProcessScript:
	def __init__(self):
		conn = pg.connect("dbname=tbh_summer user=liyihua")  # connect to laptop server
		self.cur = conn.cursor()
	def SelectData(self, chnum,startTime):
		self.cur.execute("SELECT raw_data, time_pack FROM wheelchair" + str(chnum) + " WHERE time_pack>"+ str(startTime)+" ORDER BY time_pack ASC limit 7;")
		data = self.cur.fetchall()
		return data
	
	def RunProcess(self, chnum,startTime):
		f = open('Process_Log', 'a')
		f.write('\nBeginning process on wheelchair ' + str(chnum))
		f.close()
		self.unpkData = frd.unpacking() 	# create the unpacking object
		data = self.SelectData(chnum,startTime);	# retrieve data from dataBase
		f = open('Process_Log', 'a')
		f.write('\nData for wheelchair ' + str(chnum) + ' retrieved, moving on to raw_data comprehension')	
		t0 = data[ 0][ 1 ] - (data[ 1 ][ 1 ] - data[ 0][ 1 ])
		self.TimeVector = []
		f.write('\nBeginning comprehension algorithm, total data lines to interpret is: ' + str(len(data)))	
		f.close()
		for i in xrange(0, len(data)):
			if (i % 10000 == 0 and i != 0):
				f = open('Process_Log', 'a')
				f.write('\nCompleted ' + str(i) + ' data lines so far')
				f.close()
			if ( len(data[ i ][ 0 ]) != 0 ):
				lenVect = self.unpkData.separate( np.frombuffer( data[ i ][ 0 ], dtype = np.uint8) )
				
				for j in xrange(0,2):
					if( i == 0):		
						self.TimeVector.append( np.linspace(t0, data[ i ][ 1 ], lenVect.get(lenNames[ j +7])) )
					else:
						self.TimeVector[ j ] = np.concatenate( (self.TimeVector[ j ], np.linspace( data[ i - 1 ][ 1 ], data[ i ][ 1 ], lenVect.get(lenNames[ j+7 ])) ) )

