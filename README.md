# nxmy-checkin-python
a chenkin code using webdriver mod
本软件使用webdriver库geckodriver的来实现部分爬虫功能，请注意目前仅支持火狐浏览器，
对配置文件进行修改，配置文件的基本内容包含如下：

UserId: 10000000          #用户名；登录的工
UserPass: xxxxxxxxx@!#    #密码；文本
CheckInHour: 8            #签入小时；
CheckInMin: 30            #签入分钟；
CheckOutHour: 18          #签出小时；
CheckOutMin: 30           #签出分钟；
CheckRandom: 10           #随机区间(分钟)；此设置包含了尝试每次任务的间隔，亦作为随机时间的区间，可以减少同一时间点击导致所有时间相同
CheckIp: 10.186.130.118   #服务地址
CheckUrl: http://10.186.130.118:8888/TM3/main/        #服务应用地址
CheckApp: http://10.186.130.118:8888/TM3/kqsz/attendance/qd/index.jsp?panelId=w_10723       #服务子程序地址
LoopType: SystemSleep     #三种工作模式： SystemShutdown每日任务完成后关机, SystemSleep每日任务完成后休眠, LoopContinue一直运行
vacation_start_time: 2020-07-10 06:00                 #节假日开始时间，暂停任务的开始，格式YYYY-MM-DD"
vacation_end_time: 2020-08-05 23:00                   #节假日结束时间，暂停任务的结束，格式YYYY-MM-DD"
receivers: xecotykew@gmail.com                        #设置通知邮箱


version 2.3：
1. 解决了随机时间区间的bug，现在可以设置长于30分钟的间隔时间了。
2. 解决了2.0版本中大量库的应用，现在程序占用减少了50%
3. 升级了geckodriver
4. 增加了新的时间处置方式，目前程序的稳定性更好

version 2.4:
1. 修正了部分bug

version 2.5:
1. 添加了公共节假日的策略，现在可以正常跳过假节日并正常执行调休日的签到问题，节假日数据保存在publicHoliday{年份}.json
2. 节假日api地址：http://api.haoshenqi.top/holiday?date=2023 ，内置了一个获取节假日数据的自动脚本findall.py
3. 增加了签到后邮件通知的功能，设置receivers参数，运行main2.5-EmailNotify.exe
4. 修正了loopcontinue模式的bug


