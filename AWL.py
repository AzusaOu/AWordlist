# -*- coding: utf-8 -*-
# ================================
# AWordList
# Made by Azuya, BEPC
# Since I want to learn Japanese:)

# ver 1.0.0 : 2016.10.06
# update 1.0.1 : 2016.10.20 - Add process display and Any Key Continue.
# update 1.1.0 : 2016.10.28 - Combine two versions; Add forgetting record.
# update 1.1.3 : 2016.11.06 - Now it can speak the word! (MacOS only)
# update 1.1.4 : 2016.11.15 - Change the filelist() into default scripts in Python.
# update 1.2.0 : 2016.11.21 - Make sure that every normal test would contain new words.
# update 1.2.1 : 2016.12.12 - Bug fixed.
# ================================

from random import shuffle, randint
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

# 2016.11.15~Azuya: Use default scripts in Python.
# 2016.12.12_Azuya: Add type filter.
# ------------------------------------------
def filelist():
	fl = os.listdir(os.getcwd())
	print('===================')
	for i in fl:
		if '.wl' in i and '._st' not in i:
			print(i)
	print('===================')

def tts(content, cv):
	if 'Darwin' in platform.platform():
		os.system('say '+content+' -v '+cv)

def debuglist(dlist):
	for i in dlist:
		print(i[0])

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
	wList = []
	sTmp = ''
	iSta = 0
	f = open(f_List, 'r')
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

def randintlist(num, irangex, irangey):
	randlist = []
	if irangey <= 0:
		return randlist
	for i in range(num):
		rtmp = randint(irangex, irangey)
		while((rtmp in randlist) == True):
			rtmp = randint(irangex, irangey)
		randlist.append(rtmp)
	return randlist

# 2016.11.21~Azuya: Make sure that every normal test would contain new words.
# 2016.12.01~Azuya: Be avoid of that some words never been selected.
# 2016.12.12~Azuya: Word choosing method updated.
# ------------------------------------------
def listmaker(num, wList, command='normal', record=[]):
	word4test = []
	if command == 'normal':
		if num == 0:
			word4test = wList
			num = len(wList)
		elif num > len(wList):
			print('There are not so many words in the list.')
			return []
		else:
			lenList = len(wList)
			lenOld = len(record)
			lenNew = lenList - lenOld

			if(num < lenNew/0.6 and num < lenOld/0.4):
				nNew = int(0.6 * num)
			elif num < lenNew:
				nNew = int(num * lenNew / lenList)
			else:
				nNew = lenNew
				
			nOld = num - nNew
			if nOld > lenOld:
				nOld -= 1
				nNew += 1

			print('Total:\t%d\nUnseen:\t%d\nSeen:\t%d\nNew:\t%d\nOld:\t%d' % (lenList, lenNew, lenOld, nNew, nOld))

			lNew = []
			for i in wList:
				lNew.append(i)
			for i in record:
				if i[:2] in lNew:
					lNew.remove(i[:2])
					# print('[%s - %s] Removed.' % (i[0], i[1]))

			chooseNew = randintlist(nNew, 0, lenNew-1)
			chooseOld = randintlist(nOld, 0, lenOld-1)

			# print(chooseNew)
			# print(chooseOld)

			for i in chooseNew:
				word4test.append(lNew[i])
			for i in chooseOld:
				word4test.append(record[i][:2])
			shuffle(word4test)
			# for i in word4test:
			# 	for j in i:
			# 		print j
		

	elif command == 'r':
		rList = sorted(record, key = lambda record:record[-1], reverse = True)
		if num == 0:
			word4test = rList
			num = len(rList)
		elif num > len(rList):
			print('There are not so many words in the list.')
			return []
		else:
			for i in range(num):
				word4test.append(rList[i])
	return word4test

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
# 2016.11.06~Azuya: Now it can speak.
# ------------------------------------------
def selftest(num, wList, command='normal'):
	finished = 0
	word4test = []
	record = bin_in(name4inf)
	# record: [[foreign, local, count], ...]
	# word4test: [[foreign, local], ...]

	# ---> Build the wordlist for test
	word4test = listmaker(num, wList, command, record)
	if word4test == []:
		return 0

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
				print(('\n'+i[0]+' ({0}/{1})').format(finished, len(word4test)))
				# tts(i[0], 'Kyoko')
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
						if j[0] == i[0] and j[-1] < 11:
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
				print(('\n'+i[0]+' ({0}/{1})').format(finished, len(word4test)))
				print('(You have forgot this word for {0} times.)'.format(i[-1]))
				# tts(i[0], 'Kyoko')
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
						if j[0] == i[0] and j[-1] < 11:
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
if __name__ =="__main__":
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
				# file = 'kg.wl'	# Debug.
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
		except Exception, e:
			print('\nAn error has occurred. If this info appears continually, please try to restart.')
			print('### '+str(e))


