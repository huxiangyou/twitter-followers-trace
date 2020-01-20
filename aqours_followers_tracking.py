# -*- coding: utf-8 -*-
#!/usr/bin/python3
#python 3.7.3

"""
葫芦又写于2018年8月2日
葫芦又重制于2018年11月2日
葫芦又重制于2019年5月3日
葫芦又重制于2019年5月29日

Aqours声优Twitter关注者数跟踪

TWITTER is trademarks of Twitter, Inc. or its affiliates.
Twitter是美国Twitter Inc.或其附属公司的商标。
"""

import requests
import time
import sys

#常数
PLUS="＋"#加号
MINU="－"#减号
LENGTH_OF_SIGN=2#加减号的字符宽度(对齐用)

SLEEP_TIME=300#记录间隔时间(秒)
TIMEZONE=-32400#时区(秒)

file_path='./data/'#存储数据的文件夹

PROXIES=None#{'http':'127.0.0.1:1080','https':'127.0.0.1:1080'}#代理
accounts=('anju_inami','Rikako_Aida','suwananaka','box_komiyaarisa','Saito_Shuka','Aikyan_','Kanako_tktk','aina_suzuki723','furihata_ai')#跟踪的账号
accounts_num=len(accounts)

#初始数据
proxies=None
data_last=(0,)*accounts_num
time_last=time.time()-TIMEZONE
time_last_e=time.time()-TIMEZONE
time_last_c=time.time()-TIMEZONE
error_happened=False

def get_data(user:str,num_last:int)->int:
	"""获取关注者数数据，输出数据增量并返回数据；重试3次，全部失败则返回False"""
	# error=None
	global proxies
	for i in range(3):
		try:
			num_this=requests.get('https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names='+user,proxies=proxies,timeout=(10,30)).json()[0]['followers_count']
		# except requests.exceptions.ConnectTimeout:
		# 	error=requests.exceptions.ConnectTimeout
		# except requests.exceptions.ProxyError:
		# 	error=requests.exceptions.ProxyError
		# except requests.exceptions.ConnectionError:
		# 	error=requests.exceptions.ConnectionError
		except:
			# error=sys.exc_info()[0]
			continue
		else:
			print(num_this if num_last==0 else "      " if num_this==num_last else ((PLUS if num_this>num_last else MINU)+str(abs(num_this-num_last)).rjust(6-LENGTH_OF_SIGN)),end=" | ")
			return num_this
	print(" 错误 ",end=" | ")
	return False

def navigation_bar()->None:
	"""输出导航条"""
	print("--------------------|--------|--------|--------|--------|--------|--------|--------|--------|--------|----------|----------")
	print("记录时间(日本时间)  |  伊波  |  逢田  |  诹访  |  小宫  |  齐藤  |  小林  |  高槻  |  铃木  |  降幡  | 用时(秒) | 状态")

def sleep_to_SLEEP_TIME(sleep_time:float=SLEEP_TIME)->None:
	"""睡眠到下一个整5分钟"""
	time.sleep(sleep_time-time.time()%sleep_time)

def output_time(time_this:float=None,end:str=" | ")->float:
	"""输入unix时间戳，按格式输出时间。默认为当前时间"""
	if not time_this:
		time_this=time.time()-TIMEZONE
	print(time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time_this)),end=end)
	#
	return time_this

def pass_data(num_this:int)->int:
	"""输出数据增量并返回数据"""
	print("      ",end=" | ")
	return num_this

input("跟踪Aqours声优Twitter关注者数。葫芦又制作。按回车以开始。")#等待开始

navigation_bar()
while True:
	try:
		time_this=output_time()
		if not error_happened or time_this-time_last_e>SLEEP_TIME:#未出错 或上次全部出错 或上次部分出错已过5分钟 则重新开始
			data_this=tuple(get_data(accounts[i],data_last[i]) for i in range(accounts_num))
		else:#上次部分出错 则只重试出错部分
			data_this=tuple(get_data(accounts[i],data_last[i]) if not data_this[i] else pass_data(data_last[i]) for i in range(accounts_num))
		print(str(round(time.time()-TIMEZONE-time_this,1)).rjust(6),end="   | ")#time spent

		if not all(data_this):#出错
			if not any(data_this):#全部出错
				print("网络错误 重新配置网络")
				#
				sleep_to_SLEEP_TIME()
				error_happened=False#此次数据无效 假装没出错
				if proxies:
					proxies=None
				else:
					proxies=PROXIES#所谓重新配置网络就是把代理打开或者关掉 XD
			else:#个别未出错
				print("网络错误 重试")
				#
				error_happened=True
				time_last_e=time_this
		else:#未出错
			error_happened=False
			try:#写入文件
				f=open(file_path+time.strftime('%Y%m%d',time.gmtime(time_this))+'.txt','a',encoding='ANSI')
				f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time_this)))
				for i in range(accounts_num):
					f.write("\t"+str(data_this[i]))
				f.write("\n")
				f.close()
			except:
				print("文件记录失败",end="")

			if data_this!=data_last:
				print()
			else:
				print("无变化")
			time_last_c=time_this

		if time_this//7200!=time_last//7200:#新的整2小时
			navigation_bar()
			output_time(time_last_c)
			for i in range(accounts_num):
				print(str(data_this[i] if data_this[i] else data_last[i] if data_last[i] else "      ").rjust(6),end=" | ")
			print("        ",end=" | ")
			if time_this//86400!=time_last//86400:
				print("新的一天")
			else:
				print()

		if all(data_this):
			sleep_to_SLEEP_TIME()

		data_last=tuple(data_this[i] if data_this[i] else data_last[i] for i in range(9))
		time_last=time_this

	except:
		print()
		print("程序第"+str(sys.exc_info()[2].tb_lineno)+"行出错导致程序崩溃",end=" ")
		print(sys.exc_info()[0],sys.exc_info()[1])
		output_time()
		print(str(int(SLEEP_TIME-time.time()%SLEEP_TIME))+"秒后自动重启程序")
		del data_last,time_last
		data_last=(0,)*accounts_num
		time_last=time.time()-TIMEZONE
		sleep_to_SLEEP_TIME()
		navigation_bar()

print("葫芦又制作于2019年5月3日")
input()
