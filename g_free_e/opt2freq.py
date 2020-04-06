#copy the log file from the running core
import os
import sys
import numpy as np
import math
import numpy.linalg as LA
import pickle
from shutil import copyfile
from operator import itemgetter

def Print_Word(data,file):
	for item in data:
		for word in item:
			print>>file, word,
		print>>file,"\n",

newpath = r'frequency' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

data1 = []
data2 = []
data3 = []
data4 = []
data5 = []

tot = 17
fix = 4

f = open(sys.argv[1],"r")


for i, line in enumerate(f):
				if i>=4:
					if not line.strip():
								break
					data1.append(line.split())
				  

f.close()



g = open("opt.gjf","r")

for i, line in enumerate(g):
			    
			     if i<6:
			                data2.append(line.split())

		             if i>=6 and i<=6+tot:
					data3.append(line.split())

			     if i>7+tot and i<=7+tot+fix :
					data4.append(line.split())

			     if i>8+tot+fix :
					data5.append(line.split())

		





g.close

data2[2][1] = 'freq'



for i in range(tot-fix+1,tot+1):
		data1[i][0] = data1[i][0] + '(Iso=100000000)' 

h = open("./frequency/freq.gjf","w")

Print_Word(data2,h)

Print_Word(data1,h)
print>>h,"\n",

Print_Word(data5,h)


h.close









#for item in data2:
#	for word in item:
#			print>>h, word,
#	print>>h,"\n",

#for item in data1:
#	for word in item:
#			print>>h, word,
#	print>>h,"\n",


#print>>h,"\n",

#for item in data5:
#	for word in item:
#			print>>h, word,
#	print>>h,"\n",


#copyfile('./freq.gjf', './frequency/freq.gjf')



#O1 = np.array([10.451166,6.291920,31.227011])
#O2 = np.array([8.252566,7.921773,30.385517])

#O3= (O1+O2)/2

#data = []

#for i,line in enumerate(f):
#		if i>=2 and i<=244:
#			 data.append(line.split())


# print data


#data2 = sorted(data,key=itemgetter(0))

#print data2

#print len(data2)


#data3 = []
#data4 = []
#j = 0

#print LA.norm(O1 - O2)

#O3 = np.array(data2[1])
#data2[1].pop(0)
#print data[1]



#print len(data)
#print data[0]
#print data[1]
#print data[len(data)-1]



#for i in range(0,5):
#			print i

#for i in range(0,len(data)):
#				if data2[i][0] == 'Si':
#						        data2[i].pop(0)
#							data4.append(data2[i])
 #                                                       dist = LA.norm(np.asarray(map(float,data2[i])) - O1)
#							if dist <= 3	:
#		          			  			        print i
#	
#	
#							
#						        j = j+1
#

#print data3
#
#	print data4



#line, next(f)
#for line in f:
#if "Dipole Moment" in line:
#break
