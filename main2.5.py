#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import random
import logging
import smtplib
import os
import json

from time import localtime,sleep
from datetime import datetime,date,timedelta
from selenium import webdriver
from email.mime.text import MIMEText
	
def check_file():
	if not os.path.exists('setup.ini'):
		print('	setup.ini file does not exist!!\n	Check file configure!!\n')
		return 0
	elif not os.path.exists('geckodriver.exe'):
		print('	geckodriver.exe file does not exist!!\n	Check file configure!!\n')
		return 0
	elif not os.path.exists('publicHoliday%s.json' %getYearString()):
		print('	publicHoliday.json file does not exist!! \n	Check file configure!! \n This file is using for holiday-pass.')
		return 0
	elif not os.path.exists('main2.3-test.exe'):
		print('	main2.3-test.exe file does not exist!! \n	This test_exe_file is using for mod checking, \n	please make sure the loop is ok.\n')
		return 1
	else:
		return 1


'''def Read_setup_file( bookname ):
	try:
		setupbook = xlrd.open_workbook( bookname )
		sheet1 = setupbook.sheet_by_index(0)
		sheet2 = setupbook.sheet_by_index(1)
		rows_num = sheet1.nrows
		cols_num = sheet1.ncols
		setup_col = sheet1.col_values(1)
		vacation_col = sheet2.col_values(1)
		return setup_col , vacation_col
	except:
		return 0'''


def CheckIn():
	x = os.system('ping -n 3 -w 200 %s' %CheckIp)
	if(x == 0):
		try:
			driver = webdriver.Firefox() #open firefox-webdriver drivers
			driver.get( CheckUrl )
			driver.find_element_by_xpath(".//input[@name='loginName']").send_keys(UserId)
			driver.find_element_by_xpath(".//input[@name='loginPass']").send_keys(UserPass)
			sleep(2)
			driver.find_element_by_xpath(".//input[@type='submit']").click() #find userid and password location
			sleep(10)
			driver.get( CheckApp ) #find bottom for checkin
			sleep(1)
			driver.find_element_by_id("inBox").click()
			sleep(5)
			driver.quit()
			x = 0
		except:
			x = 1

	return x


def CheckOut():
	y = os.system('ping -n 3 -w 200 %s' %CheckIp)
	if(y == 0):
		try:
			driver = webdriver.Firefox()
			driver.get( CheckUrl )
			driver.find_element_by_xpath(".//input[@name='loginName']").send_keys(UserId)
			driver.find_element_by_xpath(".//input[@name='loginPass']").send_keys(UserPass)
			sleep(2)
			driver.find_element_by_xpath(".//input[@type='submit']").click()
			sleep(10)
			driver.get( CheckApp )
			sleep(1)
			driver.find_element_by_id("outBox").click()
			sleep(5)
			driver.quit()
			y = 0
		except:
			y = 1

	return y


def ShutDownIt( shutdownchs , shutdown_delay):
	if( shutdownchs == 'SystemShutdown'):
		print(Systimer(),'Ur system will shutdown in %d seconds' %shutdown_delay)
		logging.log(logging.INFO,'Ur system will shutdown in %d seconds' %shutdown_delay)
		os.system('shutdown -s -t %d' %shutdown_delay)
	elif( shutdownchs == 'SystemSleep'):
		print(Systimer(),'Ur system will suspent to sleep in %d seconds' %shutdown_delay)
		logging.log(logging.INFO,'Ur system will suspent to sleep in %d seconds' %shutdown_delay)
		sleep( shutdown_delay )
		os.system('rundll32.exe powrProf.dll,SetSuspendState')
	else:
		return 0

# Sending Email if checkin/checkout succeed


# get current date
def getDate():
	x = datetime.today()
	return x

def getDateString():
	x = datetime.today()
	y = x.strftime("%Y-%m-%d")
	return y
	
def getYearString():
	x = datetime.today()
	y = x.strftime("%Y")
	return y

def Systimer():
	systimer = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	return systimer

# Check Today is public holiday or work day
def checkWorkDay(publicHolidays, selfHolidays):
	formattedCurrentTime = getDateString()
	todays_date = getDate()
	day = todays_date.isoweekday()
	vacation_start = datetime.fromisoformat(selfHolidays[0])
	vacation_end = datetime.fromisoformat(selfHolidays[1])
	# Go Through the public holiday list
	if day >= 1 and day <= 5:
		#print("Week-Day: ", day)正常工作日,状态0
		status = 0
	else:
		#print("Weekend: ", day)正常周末,状态1
		status = 1				  
	for item in publicHolidays:
		if item["date"] == formattedCurrentTime and item["status"] == 3:
			status = 3
			#print("Public Holiday: ", isWorkDay)公共节日,按照json列表,状态3
			break
		elif item["date"] == formattedCurrentTime and item["status"] == 2:
			status = 2
			#print("Public Work-Day: ", isWorkDay)节日调休,按照json列表,状态2
			break
	if vacation_end >= todays_date >= vacation_start:
		#手动添加的休假日期，状态4
		status = 4
	return status



def main(argv):

	print('''\n\n
  Copyright 2019 Alexiar <Alexiar@101LAPTOP-B>

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  \n''')

	#  You should have received a copy of the GNU General Public License
	#  along with this program; if not, write to the Free Software
	#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
	#  MA 02110-1301, USA.


	global UserId
	global UserPass
	global CheckInHour
	global CheckInMin
	global CheckOutHour
	global CheckOutMin
	global CheckRandom
	global CheckIp
	global CheckUrl
	global CheckApp

	vacation = []
	day = getDateString() #标记日期戳
	LoopType = 'LoopContinue'#默认循环模式为一直循环不中断
	CheckInPos = 0 #签入状态，默认为未签到
	CheckOutPos = 0 #签出状态，默认为未迁出
	Tryin = 3 #签入尝试次数
	Tryout = 3 #签出尝试次数
	nothinglogging = 20 #无事非非记录倒计次数
	loopdelay = 31 #循环延迟时间，控制循环频率，数值越高系统占用越少，不宜设置整数分钟
	shutdown_delay = 50 #关机延时时间
	CheckinRange = 0 #签到deadline时间区间
	CheckoutRange = 0 #迁出deadline时间区间
	StatusBook = {0:'Status 0: Normal working days',
				  1:'Status 1: Normal weekend',
				  2:'Status 2: Adjusted working days',
				  3:'Status 3: Public holidays',
				  4:'Status 4: Self vacation'}

	file_exist = check_file()#检查文件存在
	if file_exist == 1:
		with open( 'setup.ini','r', encoding='utf-8' ) as fi:
			setupini = fi.readlines()
		with open('publicHoliday%s.json'%getYearString(), 'r') as openfile:
			publicHolidayList = json.load(openfile)
	#print(publicHolidayList)
	
	UserId = setupini[0][7::].strip()
	UserPass = setupini[1][9::].strip()
	CheckInHour = int(setupini[2][12::].strip())
	CheckInMin = int(setupini[3][11::].strip())
	CheckOutHour = int(setupini[4][13::].strip())
	CheckOutMin = int(setupini[5][12::].strip())
	CheckRandom = int(setupini[6][12::].strip())
	CheckIp = setupini[7][8::].strip()
	CheckUrl = setupini[8][9::].strip()
	CheckApp = setupini[9][9::].strip()
	LoopType = setupini[10][9::].strip()
	vacation_start = setupini[11][20::].strip()#节假日设置开始
	vacation_end = setupini[12][18::].strip()#节假日设置结束
	receivers = setupini[13][10::].strip()
	vacation += vacation_start, vacation_end 
	

	print (
		'',
		'','UserId: ',UserId,'\n',
		'','CheckInHour: ',CheckInHour,'\n',
		'','CheckInMin: ',CheckInMin,'\n',
		'','CheckOutHour: ',CheckOutHour,'\n',
		'','CheckOutMin: ',CheckOutMin,'\n',
		'','CheckRandom: ',CheckRandom,'\n',
		'','CheckIp: ',CheckIp,'\n',
		'','CheckUrl: ',CheckUrl,'\n',
		'','CheckApp: ',CheckApp,'\n',
		'','LoopType: ',LoopType,'\n',
		'','Vacation_setup: %s -- %s'%(vacation_start,vacation_end),'\n',
		'', 'Email Receiver: ', receivers, '\n',
		)

	LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
	logging.basicConfig(filename='CHECKIN_%s.log'%CheckIp, level=logging.DEBUG, format=LOG_FORMAT)#日志启动
	logging.log(logging.INFO, "Program init.")

	print(Systimer(),'Program init!')
	print(Systimer(),'Logging init!')
	
	status = checkWorkDay( publicHolidayList,vacation )# 判断今日状态,工作日0,周末1,节假日调整2,节假日3,休假4,默认None
	lesstime = localtime() #获取当前时间，用于以下时间戳的计算
	Checkintime = datetime( lesstime[0],lesstime[1],lesstime[2],CheckInHour,CheckInMin,0) #签到的时间
	Checkouttime = datetime( lesstime[0],lesstime[1],lesstime[2],CheckOutHour,CheckOutMin,0) #迁出的时间
	CheckinStart = Checkintime - timedelta(minutes=CheckRandom) #开始执行签到的时间戳
	CheckoutEnd = Checkouttime + timedelta(minutes=CheckRandom) #结束执行迁出的时间戳

	while file_exist == 1:

		now = datetime.now()
		
		if day != getDateString(): #若日期发生变化，重新载参数
			with open('publicHoliday%s.json'%getYearString(), 'r') as openfile:
				publicHolidayList = json.load(openfile)
			print(Systimer(),'Renew PublicHoliday data and Datetime.')
			logging.log(logging.INFO, 'Renew PublicHoliday data and Datetime.')
			#日期变化后更新日期，更新status状态，更新时间戳
			day = getDateString()
			status = checkWorkDay( publicHolidayList,vacation )
			lesstime = localtime() #获取当前时间，用于以下时间戳的计算
			Checkintime = datetime( lesstime[0],lesstime[1],lesstime[2],CheckInHour,CheckInMin,0) #签到的时间
			Checkouttime = datetime( lesstime[0],lesstime[1],lesstime[2],CheckOutHour,CheckOutMin,0) #迁出的时间
			CheckinStart = Checkintime - timedelta(minutes=CheckRandom) #开始执行签到的时间戳
			CheckoutEnd = Checkouttime + timedelta(minutes=CheckRandom) #结束执行迁出的时间戳

		
		#没啥可干的时候睡眠一个loopdelay周期，屏幕更新一下
		if( nothinglogging == 20 ) or ( nothinglogging == 10):
			print(Systimer(),'Wait for next process. %s' %StatusBook[status])
			nothinglogging = nothinglogging -1
		elif( nothinglogging > 0 ):
			nothinglogging = nothinglogging -1
		else:
			logging.log(logging.INFO, 'Wait for next process. %s' %StatusBook[status])
			nothinglogging = 20
		sleep( loopdelay )#延时睡眠时间，不宜为分钟整数
		
		#判断运行状态，节假日、周末、休假自动关机或休眠，如果是loopconinue模式则重复循环
		if status == 0:
			pass
		elif status == 1 and CheckinStart < now < Checkintime:
			if LoopType != 'LoopContinue':
				print(Systimer(),'Status 1, Normal weekend, Process your choice of LoopType: %s' %LoopType)
				logging.log(logging.INFO, 'Status 1, Normal weekend, Process your choice of LoopType')
				break
			else:
				continue
		elif status == 2:
			pass
		elif status == 3 and CheckinStart < now < Checkintime:
			if LoopType != 'LoopContinue':
				print(Systimer(),'Status 3, public holidays, Process your choice of LoopType: %s' %LoopType)
				logging.log(logging.INFO, 'Status 3, public holidays, Process your choice of LoopType')
				break
			else:
				continue
		elif status == 4 and CheckinStart < now < Checkintime:
			if LoopType != 'LoopContinue':
				print(Systimer(),'Status 4, Set for self vacation, Process your choice of LoopType: %s' %LoopType)
				logging.log(logging.INFO, 'Status 4, Set for self vacation, Process your choice of LoopType"')
				break
			else:
				continue
		else:
			continue
		

		if CheckinStart <= now < Checkintime  and CheckInPos < 1 and Tryin > 0:
			#签入检查，全部为与判断
			CheckinRange = (Checkintime - now).seconds
			crnSec = random.randint(0 , CheckinRange)
			logging.log(logging.INFO, "Program will run checkinng in T.minus %d seconds. Please wait." %crnSec)
			for xi in range(crnSec):
				print(Systimer(),'Program will run checkinng in T.minus %d seconds. Please wait.' %(crnSec-xi),'\r', end='')
				sleep(1)
			#random delay for defferent checkin
			print(Systimer(),'Checkin starts, This will take some minutes!!')
			logging.log(logging.INFO, "Checkin starts.")
			CheckInPos = 1 - CheckIn()
			if (CheckInPos == 1 ):
				print(Systimer(),'Checkin successed. Wait for Checkout process!!')
				#sendEmail(receivers, '上班打卡成功')
				logging.log(logging.INFO, "Checkin success.")
				continue
			elif (CheckInPos == 0) and (Tryin > 0):
				print(Systimer(),'Checkin failed. Wait for trying again later!!')
				logging.log(logging.WARNING, "Checkin failed, Start retrying.")
				Tryin = Tryin - 1
				continue
			elif (CheckInPos == 0) and (Tryin == 0):
				print(Systimer(),'Checkin failed. Please Check Connnection!!')
				logging.log(logging.ERROR, "Checkin failed. Please Check Connnection.")
				Tryin = Tryin - 1
				continue



		elif Checkouttime < now <= CheckoutEnd and CheckOutPos < 1 and Tryout > 0:
			CheckoutRange = (CheckoutEnd - now).seconds
			crmSec = random.randint(0 , CheckoutRange)
			logging.log(logging.INFO, "Program will run checkout in T.minus %d seconds. Please wait." %crmSec)
			for xi in range(crmSec):
				print(Systimer(),'Program will run checkout in T.minus %d seconds. Please wait.' %(crmSec-xi),'\r', end='')
				sleep(1)
			print(Systimer(),'Checkout starts, This will take some minutes!!')
			logging.log(logging.INFO, "Checkout starts.")
			CheckOutPos = 1 - CheckOut()
			if (CheckOutPos == 1 ):
				print(Systimer(),'Checkout successed. Wait for Checkin process nextday!!')
				#sendEmail(receivers, '下班打卡成功')
				logging.log(logging.INFO, "Checkout success.")
				continue
			elif (CheckOutPos == 0) and (Tryout > 0):
				print(Systimer(),'Checkout failed. Wait for trying again later!!')
				logging.log(logging.WARNING, "Checkout failed, Start retrying.")
				Tryout = Tryout - 1
				continue
			elif (CheckOutPos == 0) and (Tryout == 0):
				print(Systimer(),'Checkout failed. Please Check Connnection!!')
				logging.log(logging.ERROR, "Checkout failed. Please Check Connnection.")
				Tryout = Tryout - 1
				continue

		elif CheckoutEnd+timedelta(minutes=5) < now < CheckoutEnd+timedelta(minutes=15):
		#Checkin and Checkout status of today, log it, and suspent pc
			if(CheckInPos == 1) and (CheckOutPos == 1):
				logging.log(logging.INFO, "Checkin and Checkout all successed. SYSTEM will %s for tommrow" %LoopType)
				print(Systimer(),'Checkin and Checkout all successed. SYSTEM will %s for tommrow' %LoopType)
			else:
				logging.log(logging.WARNING, "Checkin or Checkout failed.")
				print(Systimer(),'Checkin or Checkout failed. Check connection and see log record.')
				print(Systimer(),'Checkin or Checkout failed. SYSTEM will %s for tommrow' %LoopType)
			#status reset
			CheckInPos = 0
			CheckOutPos = 0
			Tryin = 3
			Tryout = 3
			status = None
			#status reset
			if LoopType != 'LoopContinue' :
				break


	#正常关机否则程序停止
	ShutDownIt( LoopType , shutdown_delay )#suspent pc




if __name__ == '__main__':
	main(1)
	

