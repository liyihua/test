#!/usr/bin/python
import numpy as np
import scipy as sp

class unpacking:
	def __init__(self):
		self.IDx = [0xa1, 0x00]               # 0
		self.IDy = [0xa2, 0x01]             # 1    
		self.IDz = [0xa3, 0x02]               # 2
		self.IDp1S = [0xb1, 0x03]         # 3
		self.IDp2S = [0xb2, 0x04]         # 4
		self.IDp3S = [0xb3, 0x05]         # 5
		self.IDp4S = [0xb4, 0x06]         # 6
		self.IDp1B = [0xc1, 0x07]     # 7
		self.IDp2B = [0xc2, 0x08]     # 8
		self.IDp3B= [0xc3, 0x09]     # 9
		self.IDp4B = [0xc4, 0x0a]     # A
		self.IDp5B = [0xc5, 0x0b]     # B    
		self.IDemfiB = [0xd1, 0x0c]          # C
		self.IDemfiS = [0xd2, 0x0d]          # D
		self.IDtemp = [0xe1, 0x0e]            # E
		self.IDhum = [0xe2, 0x0f]             # F
		self.IDspO2Hr = 0xf1
		self.IDspO2Sat = 0xf2
		self.x = []
		self.y = []
		self.z = []
		self.temp = []
		self.hum = []        
		self.p1_seat = []
		self.p2_seat = []
		self.p3_seat = []
		self.p4_seat = []
		self.p1_backrest = []
		self.p2_backrest = []
		self.p3_backrest = []
		self.p4_backrest = []
		self.p5_backrest = []
		self.emfi_seat = []
		self.emfi_backrest = []
		self.spO2_sat = []
		self.spO2_hr = []
				
	def indentifierBelongsTo(self, identifier):
		return (self.dataFromDB[self.i] == identifier[0] and np.right_shift(self.dataFromDB[self.i + 1], 4) == identifier[1])
		
	def reconstruct(self):
		shifted_masked_msb_data= np.left_shift(np.bitwise_and(self.dataFromDB[self.i + 1], 0x0f), 8)
		result = np.bitwise_or(shifted_masked_msb_data, self.dataFromDB[self.i + 2],)
		return result
		
	def separate(self, dataFromDB):
		self.dataFromDB = dataFromDB
		self.i = 0
		
		deltaLenX = len(self.x)
		deltaLenY = len(self.y)
		deltaLenZ = len(self.z)
		
		deltaLenp1S = len(self.p1_seat)
		deltaLenp2S = len(self.p2_seat)
		deltaLenp3S = len(self.p3_seat)
		deltaLenp4S = len(self.p4_seat)
		
		deltaLenp1B = len(self.p1_backrest)
		deltaLenp2B = len(self.p2_backrest)
		deltaLenp3B = len(self.p3_backrest)
		deltaLenp4B = len(self.p4_backrest)
		deltaLenp5B = len(self.p5_backrest)
	
		deltaLenEmfiB = len(self.emfi_backrest)
		deltaLenEmfiS = len(self.emfi_seat)
		
		deltaLenTemp = len(self.temp)
		deltaLenHum = len(self.hum)
		
		deltaLenSpO2Sat = len(self.spO2_sat)
		deltaLenSpO2HR = len(self.spO2_hr)
		
		while(self.i < len(self.dataFromDB) - 3):   
			if(self.indentifierBelongsTo(self.IDx)):
				self.x.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDy)):
				self.y.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDz)):
				self.z.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDp1S)):
				self.p1_seat.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDp2S)):
				self.p2_seat.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDp3S)):
				self.p3_seat.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDp4S)):
				self.p4_seat.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDp1B)):
				self.p1_backrest.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDp2B)):
				self.p2_backrest.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDp3B)):
				self.p3_backrest.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDp4B)):
				self.p4_backrest.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDp5B)):
				self.p5_backrest.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDemfiS)):
				self.emfi_seat.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDemfiB)):
				self.emfi_backrest.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDtemp)):
				self.temp.append(self.reconstruct())
				self.i += 3
			elif(self.indentifierBelongsTo(self.IDhum)):
				self.hum.append(self.reconstruct())
				self.i += 3
			elif(self.dataFromDB[self.i]  == self.IDspO2Hr ):
				self.spO2_hr.append(self.reconstruct())
				self.i += 3
			elif(self.dataFromDB[self.i]  == self.IDspO2Sat and self.reconstruct() <= 100):  # Oxigen Sat. value always is less than 100
				self.spO2_sat.append(self.reconstruct())
				self.i += 3
			else:
				self.i += 1
				
		deltaLenX = len(self.x) - deltaLenX 
		deltaLenY = len(self.y) - deltaLenY
		deltaLenZ = len(self.z) - deltaLenZ
		
		deltaLenp1S = len(self.p1_seat) - deltaLenp1S 
		deltaLenp2S = len(self.p2_seat) - deltaLenp2S
		deltaLenp3S = len(self.p3_seat) - deltaLenp3S
		deltaLenp4S = len(self.p4_seat) - deltaLenp4S
		
		deltaLenEmfiB = len(self.emfi_backrest) - deltaLenEmfiB
		deltaLenEmfiS = len(self.emfi_seat) - deltaLenEmfiS
		deltaLenp1B = len(self.p1_backrest) - deltaLenp1B
		deltaLenp2B = len(self.p2_backrest) - deltaLenp2B
		deltaLenp3B = len(self.p3_backrest) - deltaLenp3B
		deltaLenp4B = len(self.p4_backrest) - deltaLenp4B
		deltaLenp5B = len(self.p5_backrest) - deltaLenp5B
		deltaLenTemp = len(self.temp) - deltaLenTemp
		deltaLenHum = len(self.hum) - deltaLenHum
		deltaLenSpO2Sat = len(self.spO2_sat) - deltaLenSpO2Sat 
		deltaLenSpO2HR = len(self.spO2_hr) - deltaLenSpO2HR 
	
		return {'LenEmfiB':deltaLenEmfiB, 'LenEmfiS':deltaLenEmfiS ,
		'Len1B':deltaLenp1B,'Len2B':deltaLenp2B , 'Len3B':deltaLenp3B ,'Len4B':deltaLenp4B,'Len5B':deltaLenp5B, 
		'LenTemp':deltaLenTemp, 'LenHum':deltaLenHum, 
		'LenSpO2':deltaLenSpO2Sat, 'LenSpO2HR':deltaLenSpO2HR ,
		'Lenp1S':deltaLenp1S, 'Lenp2S':deltaLenp2S, 'Lenp3S':deltaLenp3S, 'Lenp4S':deltaLenp4S,
		'LenX':deltaLenX, 'LenY':deltaLenY, 'LenZ':deltaLenZ}
		
	def EraseBufferData(self):
		self.x = []
		self.y = []
		self.z = []
		self.temp = []
		self.hum = []        
		self.p1_seat = []
		self.p2_seat = []
		self.p3_seat = []
		self.p4_seat = []
		self.p1_backrest = []
		self.p2_backrest = []
		self.p3_backrest = []
		self.p4_backrest = []
		self.p5_backrest = []
		self.emfi_seat = []
		self.emfi_backrest = []
		self.spO2_sat = []
		self.spO2_hr = []
		
	def getEmfiSeat(self):
		return self.emfi_seat 
	def getEmfiBackrest(self):
		return self.emfi_backrest
		
	def getTemp(self):	
		d1 = -39.7
		d2 = 0.04
		self.temp = np.array(self.temp)
		return np.round((d1 + d2*self.temp), 2)
	def getHum(self):
		c1 = -2.0468
		c2 = 0.5872
		c3 = -4.0845e-4        
		self.hum = np.array(self.hum)
		return np.round((c1+c2*self.hum+c3*(self.hum**2)), 2)
		
	def getSpO2HR(self):
		return self.spO2_hr
	def getSpO2Sat(self):
		return self.spO2_sat
		
	def getp1Backrest(self):
		return self.p1_backrest
	def getp2Backrest(self):
		return self.p2_backrest
	def getp3Backrest(self):
		return self.p3_backrest
	def getp4Backrest(self):
		return self.p4_backrest
	def getp5Backrest(self):
		return self.p5_backrest
	
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def getZ(self):
		return self.z
	
	def getp1Seat(self):
		return self.p1_seat
	def getp2Seat(self):
		return self.p2_seat
	def getp3Seat(self):
		return self.p3_seat
	def getp4Seat(self):
		return self.p4_seat
		
class AnalysisData:
	def spec(self, signal, fs):    
		n = len(signal)              # length of the signal
		k = sp.arange(n)
		T = n/fs
		frq = k/T                   # two sides frequency range
		frq = frq[range(n/2)]       # one side frequency range
		y = sp.fft(signal)/n        # fft computing and normalization
		y[0] = 0                    # DC component = 0
		y = abs(y[range(n/2)])
		return {'spec':y, 'freq':frq}
		