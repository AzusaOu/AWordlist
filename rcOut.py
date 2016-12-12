# -*- coding: utf-8 -*-
# v1.0.0 : 2016.11.17
from AWL import bin_in
import os
import datetime

def getTime():
	now = datetime.datetime.now()
	return now.strftime("%Y-%m-%d %H:%M:%S")

	# f = raw_input('*._st: ')
fl = os.listdir(os.getcwd())
rwl = []
for i in fl:
	if i.split('.')[-1] == '_st':
		rwl.extend(bin_in(i))
rwl = sorted(rwl, key = lambda rwl:rwl[-1], reverse = True)
strRwl = ''
for i in rwl:
	if i[-1] <= 3:
		break
	strRwl += ('[%d] %s\n\t%s\n\n' % (i[-1], i[0], i[1]))

strRwl = 'AWL Report\n%s\n\n' % getTime() + strRwl
print(strRwl)
with open('AWLReport.txt', 'w') as fo:
	fo.write(strRwl)
