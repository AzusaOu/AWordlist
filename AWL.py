# -*- coding: utf-8 -*-
# ================================
# AWordList
# Made by Azuya, BEPC
# Since I want to learn Japanese:)

# ver 1.0 : 2016.10.06
# update 1.0.1 : 2016.10.20 - Add process display and Any Key Continue.
# update 1.1.0 : 2016.10.28 - Combine two versions; Add forgetting record.
# ================================

from random import shuffle
import 	platform
import	os

# Core
# ============================================================

def getchar(s=''):
	if s != '':
		print(s)
	# http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
	# This function is designed for Win
	if 'Windows' in platform.platform():
		ch = msvcrt.getch()

	# http://blog.csdn.net/marising/article/details/3173848
	# This function is designed for Linux
	else:
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try :
		    tty.setraw( fd )
		    ch = sys.stdin.read( 1 )
		    return ch
		finally :
		    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def filelist():
	# This function is designed for Win
	if 'Windows' in platform.platform():
		os.system('dir')
	# This function is designed for Linux
	else:
		os.system('ls -hl') 

# Get from Koyume(140514)
# ------------------------------------------
import	pickle
def bin_in(s_Location):
    file = open(s_Location,'rb')
    content = pickle.load(file)
    file.close()
    return content
def bin_out(a_Object,s_Location):
    file = open(s_Location,'wb')
    pickle.dump(a_Object,file)
    file.close()

# 2016.10.25~Azuya: Add the function which can create a pickle file
# ------------------------------------------
def loadwords(f_List):
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
	global name4inf
	name4inf = f_List + '._st'
	if os.path.exists(name4inf) == False:
		bin_out([], name4inf)
	return sTitle, wList, iSta

# Application
# ============================================================
def welcome(f_List):
	sTitle, wList, iCount = loadwords(f_List)
	print('Title  :< ' +sTitle+ ' >')
	print('Amount :' +str(iCount))
	return sTitle, wList

# 2016.10.20~Azuya: Add the process display and any button can make it continue.
# 2016.10.25~Azuya: Add a function which can record how many times is a word forgetted.
# 2016.10.28~Azuya: Add 'tt r' mode.
# ------------------------------------------
def selftest(num, wList, command='normal'):
	finished = 0
	word4test = []
	record = bin_in(name4inf)
	# record: [[foreign, local, count], ...]
	# word4test: [[foreign, local], ...]

	# ---> Build the wordlist for test
	if command == 'normal':
		shuffle(wList)
		if num == 0:
			word4test = wList
			num = len(wList)
		elif num > len(wList):
			print('There are not so many words in the list.')
			return 0
		else:
			for i in range(num):
				word4test.append(wList[i])
	elif command == 'r':
		rList = sorted(record, key = lambda record:record[-1], reverse = True)
		if num == 0:
			word4test = rList
			num = len(rList)
		elif num > len(rList):
			print('There are not so many words in the list.')
			return 0
		else:
			for i in range(num):
				word4test.append(rList[i])
	# <---------------------------------
	# ---> Test start
	sta = ''
	if command == 'normal':
		while True:
			for i in word4test:
				# ---> Judge whether the word has been put into the record list.
				for j in record:
					if i[0] == j[0]:
						break
				else:
					record.append([i[0], i[1], 0])
				# <---------------------------------
				print(('\n'+i[0]+' ({0}/{1})').format(finished, num))
				print('|')
				sta = getchar()
				print(i[1] + '...[y/q?]')
				sta = getchar()
				if sta == 'y':
					word4test.remove(i)
					finished += 1
					for j in record:
						if j[0] == i[0] and j[-1] != 0:
							j[-1] -= 1					
					print('Deleted.')
				elif sta == 'q':
					return 1
				else:
					for j in record:
						if j[0] == i[0]:
							j[-1] += 1
					# print record	# Debug.
			if len(word4test) == 0:
				bin_out(record, name4inf)
				print('You have finished the test.')
				break
			shuffle(word4test)

	elif command == 'r':
		# word4test: [[foreign, local, count], ...]
		while True:
			# print(str(word4test))
			for i in word4test:
				print(('\n'+i[0]+' ({0}/{1})').format(finished, num))
				print('(You have forgot this word for {0} times.)'.format(i[-1]))
				print('|')
				sta = getchar()
				print(i[1] + '...[y/q?]')
				sta = getchar()
				if sta == 'y':
					word4test.remove(i)
					finished += 1
					# Forgetting record -1.
					for j in record:
						if j[0] == i[0] and j[-1] != 0:
							j[-1] -= 1					
					print('Deleted.')
					break
				elif sta == 'q':
					return 1				
				else:
					# Forget.
					for j in record:
						if j[0] == i[0]:
							j[-1] += 1
			if len(word4test) == 0:
				bin_out(record, name4inf)
				print('You have finished the test.')
				break
			word4test = sorted(word4test, key = lambda word4test:word4test[-1], reverse = True)
	# <---------------------------------
	return 1

def helplist(content):
	print('These are the available commands:')
	for i in content:
		print('\n'+i)
		print('- '+content[i])

# Main UI
# ============================================================
if 'Windows' in platform.platform():
	import  msvcrt
else:
	import  sys, tty, termios

cha = 'AWL~$ '
wList = []
while True:
	try:
		com = raw_input(cha)
		
		if 'ld' in com:
			ltmp = com.split(' ')
			file = ltmp[1]
			# file = 'kn.wl'	# Debug.
			try:
				sTitle, wList = welcome(file)
				cha = sTitle +'~$ '
			except:
				print('File does not exist...')

		elif 'tt' in com:
			ltmp = com.split(' ') 
			if len(ltmp) == 2:
				selftest(int(ltmp[1]), wList)
			else:
				selftest(int(ltmp[2]), wList, ltmp[1])

		elif com == 'lt':
			for i in wList:
				print(i[0] + ' - ' + i[1])

		elif com == 'in':
			print('Title  :< ' +sTitle+ ' >')
			print('Amount :' +str(len(wList)))

		elif com == 'ft':
			filelist()

		elif com == 'q':
			break

		elif com == '-h':
			helpContent = {'ld [filePath]':'Load a wordlist file from your disk. This should be the first step.',
			'lt':'Load a wordlist file from your disk. This should be the first step.',
			'tt [number]':'Have a selftest. The [number] decides how many words are used for your examination. If it is set as 0, all of the words will appear.',
			'tt r [number]':'Review the words you have seen.',
			'in':'Show the information of current wordlist.',
			'ft':'Show the files in current dir.',
			'q':'Quit.'}
			helplist(helpContent)
			print('\nMore information about this APP, come here: https://github.com/AzusaOu/AWordlist\n')

		elif com == '':
			continue

		else:
			print('Invalid command. -h for help.')
	except:
		print('\nAn error has occurred. If this info appears continually, please try to restart.')


