import json
import re
from datetime import datetime,date,timedelta
import requests

def getYearString():
	x = datetime.today()
	y = x.strftime("%Y")
	return y

'''with open('date-holidays.txt','r') as f: 
		date = f.readlines()

dataform = re.compile(r'"date":"[0-9]{4}-[0-9]{2}-[0-9]{2}","year":[0-9]{4},"month":[0-9]{1,2},"day":[0-9]{1,2},"status":[0-9]{1}', re.I)
datelist =[]

for t in date:
	datelist += dataform.findall(t)
print(datelist)'''

year = str(input('输入需要获取节假日的年份: '))
r = requests.get('http://api.haoshenqi.top/holiday?date=%s' %year)
with open('ordinry-holidaydate%s.json'%year,'w') as f:
     f.write(r.content.decode('utf-8'))
     f.close


'''with open('date-holidays.json', 'r') as openfile:
	publicHolidayList = json.load(openfile)
with open('ordinry-holidaydate%s.json'%year,'r') as fi:
     publicHolidayList = json.load(fi)
     fi.close'''

publicHolidayList = eval(r.content.decode('utf-8'))
print(publicHolidayList)
print(type(publicHolidayList))

    
publicHoliday =[]
for item in publicHolidayList:
	print(item)
	if item['status'] >= 2:
		#print(type(item['status']))
		publicHoliday.append(item)

print('\n\n')

for item in  publicHoliday:
	#print(type(item['status']))
	print(item)

with open('publicHoliday%s.json'%year, 'w') as fj:
	json.dump(publicHoliday , fj)
	fj.close

	
