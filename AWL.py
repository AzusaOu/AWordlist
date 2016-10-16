# -*- coding: utf-8 -*-
# ================================
# AWordList
# Made by Azuya, BEPC
# Since I want to learn Japanese:)
# ver 1.0 : 2016.10.06
# ================================

from random import shuffle
import  os
import  sys
import  tty, termios

def loadWords(f_List):
	f = open(f_List, 'r')
	wList = []
	sTmp = ''
	iSta = 0
	sTitle = f.readline().replace('\n','')
	sTmp = f.readline().replace('\n','')
	while(sTmp!='###'):
		lTmp = sTmp.split(' - ')
		wList.append(lTmp)
		sTmp = f.readline().replace('\n','')
		iSta += 1
	f.close()
	return sTitle, wList, iSta

def getchar():
	# http://blog.csdn.net/marising/article/details/3173848
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try :
	    tty.setraw( fd )
	    ch = sys.stdin.read( 1 )
	    return ch
	finally :
	    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def welcome(f_List):
	sTitle, wList, iCount = loadWords(f_List)
	print('Title  :< ' +sTitle+ ' >')
	print('Amount :' +str(iCount))
	return sTitle, wList

def selftest(num, wList):
	shuffle(wList)
	word4test = []
	if num == 0:
		word4test = wList
	elif num > len(wList):
		print('There are not so many words in the list.')
		return 0
	else:
		for i in range(num):
			word4test.append(wList[i])
	sta = ''
	while True:
		for i in word4test:
			print('\n'+i[0])
			a = raw_input('↓')
			print(i[1] + '...(y/q?)')
			sta = getchar()
			if sta == 'y':
				word4test.remove(i)
				print('Deleted.')
			elif sta == 'q':
				return 1
		if len(word4test) == 0:
			print('You have finished the test.')
			break
		shuffle(word4test)
	return 1


# ----------------------------------------------------

cha = 'AWL~$ '
wList = []
while True:
	try:
		com = raw_input(cha)
		
		if 'ld' in com:
			ltmp = com.split(' ')
			file = ltmp[1]
			try:
				sTitle, wList = welcome(file)
				cha = sTitle +'~$ '
			except:
				print('File does not exist...')

		elif 'tt' in com:
			ltmp = com.split(' ') 
			selftest(int(ltmp[1]), wList)

		elif com == 'lt':
			for i in wList:
				print(i[0] + ' - ' + i[1])

		elif com == 'q':
			break

		elif com == '-h':
			print('\nld [file]\n- Load a wordlist file from your disk. This should be the first step.\n')
			print('lt\n- After your wordlist loaded, you can use this command to show all of your words.\n')
			print('tt [number]\n- Have a selftest. The [number] decide how many words are used for your examination. If it is set as 0, all of the words will appear.\n')
			print('q\n- Quit.')
			print('\nMore information about this APP, come here: https://github.com/AzusaOu/AWordlist\n')

		elif com == '':
			continue

		else:
			print('Invalid command. -h for help.')
	except:
		print('\nAn error has occurred. If this info appears continually, please try to restart.')


