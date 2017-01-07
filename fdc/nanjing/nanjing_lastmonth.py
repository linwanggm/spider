#!/use/bin/python
#coding:utf-8

'''

nanjing_lastmonth.py

nanjing house data
URL:http://www.njhouse.com.cn/index_tongji.php
1. get current data (time, rengou, chengjiao, xinfangshangshi), is current data
2. get current year data of city, get yerstoday and today data (rengou, chengjiao, mianji), is a picture
3. get the data (zhuzhai, bangong, shangye) all towns of city (chengjiaotaoshu, chengjiaomianji), for last month
4. the price of houses of all towns, for last month (chengjiaoqujian, chengjiaotaoshu, chengjiaomianji, bili)
5. the data of ershoufang of current year, last month, last day (town, chengjiaotaoshu, chengjiaomiji), is a picture

all data split by ','
'''
import os,sys
import urllib
import re
import datetime
import sys
import re
import logging
reload(sys)
sys.setdefaultencoding('utf8')

city = "'nanjing'"
#get url content
def get_html_content(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

#get url file
def down_file_content(url, filename):
    urllib.urlretrieve(imgurl,'/home/wln/python/pic/%s.jpg' % x)

'''
get the data (zhuzhai, bangong, shangye) all towns of city (chengjiaotaoshu, chengjiaomianji), for last month

'''
def get_lastmonth_data_townnum(content, fd):
	global date_from;
	townlist=['quanshi', 'xuanwu', 'qinhuai','jianye', 'gulou',
			  'xixia','yuhuatai', 'jiangning', 'liuhe', 'pukou',
			  'tanshui','gaochun']
	reg = r'bgcolor="#FFFFFF">(\d+|'')</td>'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,content)
	if len(itemlist) < 1:
		logging.error('function get_lastmonth_data(), get aim string list error')
		return
	i = 0
	for item in itemlist:
		i = i + 1
		if i%6 == 1:
			fd.write(city + ",")
			fd.write("'" + str(date_from) + "',")
			fd.write("'" + townlist[(i-1)/6] + "'")
		if item.isdigit() == True:
			fd.write("," + item)
		if item == '':
			fd.write("," + '0')
		if i%6 == 0:
			fd.write('\n')
	if i%6 != 0:
		fd.write('\n')
		
	if len(townlist)*6 != len(itemlist):
		logging.error('function get_lastmonth_data(), get data error, town num is ' + len(townlist)+ ', data num is ' + len(itemlist) )
	
#the price of houses of all towns, for last month (chengjiaoqujian, chengjiaotaoshu, chengjiaomianji, bili)

def get_lastmonth_data_hourse_size_rate(content, fd):
	global date_from;
	list_c1name = []
	reg = r'<td height="20">([\s\S]*)</font></td><td>'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,content)	
	#get first column name list
	str_c1 = itemlist[0].split('align="center" cellpadding="0" cellspacing="1"')[0]
	list_c1 = str_c1.split('</font>')
	reg1 = r'(\d+.*\d+)'
	imgre1 = re.compile(reg1)
	for item in list_c1:
		if '<font color=#003399>' not in item:
			continue
		aim = item.split('<font color=#003399>')[1]
		ilist = re.findall(imgre1,aim)
		if len(ilist) == 0:
			ilist.append('total')
		list_c1name.append(ilist[0])
	reg2 = r'<td>([0-9\.%]*)</td>'
	imgre2 = re.compile(reg2)
	ilist = re.findall(imgre2,str_c1)
	i = 0
	for item in ilist:
		i=i+1
		if(i%3==1):
			fd.write(city + ",")
			fd.write("'"+str(date_from)+"',")
			fd.write("'" + list_c1name[(i-1)/3] + "'")
		fd.write(',' + item.split('%')[0])
		if (i%3==0):
			fd.write('\n')
	if (i%3 != 0):
		fd.write('\n')
		logging.error('function get_lastmonth_data_hourse_size_rate(), len(list_c1name) is ' + str(len(list_c1name))+ 'len(ilist) is ' + str(len(ilist)))

#the price of houses of all towns, for last month (chengjiaoqujian, chengjiaotaoshu, chengjiaomianji, bili)
def get_lastmonth_data_hourse_price_rate(content, fd):
	global date_from;
	list_c1name = []
	reg = r'<td height="20">([\s\S]*)</font></td><td>'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,content)	
	#get first column name list
	str_c1 = itemlist[0].split('align="center" cellpadding="0" cellspacing="1"')[1]
	list_c1 = str_c1.split('</font>')
	reg1 = r'(\d+.*\d+)'
	imgre1 = re.compile(reg1)
	for item in list_c1:
		if '<font color=#003399>' not in item:
			continue
		aim = item.split('<font color=#003399>')[1]
		ilist = re.findall(imgre1,aim)
		if len(ilist) == 0:
			ilist.append('total')
		list_c1name.append(ilist[0])
	str_c2 = content.split('align="center" cellpadding="0" cellspacing="1"')[-1]
	reg2 = r'<td>([0-9\.%]*)</td>'
	imgre2 = re.compile(reg2)
	ilist = re.findall(imgre2,str_c2)
	i = 0
	for item in ilist:
		i=i+1
		if(i%3==1):
			fd.write(city + ",")
			fd.write("'"+str(date_from)+"',")
			fd.write("'" + list_c1name[(i-1)/3] + "'")
		fd.write(',' + item.split('%')[0])
		if (i%3==0):
			fd.write('\n')
	if (i%3 != 0):
		fd.write('\n')	
		logging.error('function get_lastmonth_data_hourse_price_rate(), len(list_c1name) is ' + str(len(list_c1name))+ 'len(ilist) is ' + str(len(ilist)))
url = "http://www.njhouse.com.cn/index_tongji.php"

def main():
	global date_from;
	current_path = os.getcwd()
	current_year = datetime.datetime.now().strftime('%Y')
	dir = current_path + '/data/' + current_year
	last_month_data_townnum_f = dir + '/' + 'month_statistics_town_num.txt'
	last_month_data_townsize_f = dir + '/' + 'month_statistics_town_size_rate.txt'
	last_month_data_townprice_f = dir + '/' + 'month_statistics_town_price_rate.txt'
	log_record_f = dir + '/' + 'log_record.txt'
	if (os.path.exists(dir) == False):
		os.makedirs(dir)
	#get last month time
	d = datetime.datetime.now()
	dayscount = datetime.timedelta(days=d.day)
	dayto = d - dayscount
	date_from = datetime.datetime(dayto.year, dayto.month, 1, 0, 0, 0)
	
	logging.basicConfig(level=logging.INFO,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %Y-%m-%d %H:%M:%S',
		filename=log_record_f,
		filemode='a')
	logging.info('*'*10 + '\t' + str(datetime.datetime.now())+'\t'+ '*'*10)
	#get current data			
	fd_num = open(last_month_data_townnum_f, 'a')
	content = get_html_content(url)
	get_lastmonth_data_townnum(content, fd_num)	
	fd_num.close()
	fd_size = open(last_month_data_townsize_f, 'a')
	get_lastmonth_data_hourse_size_rate(content, fd_size)
	fd_size.close()
	fd_price = open(last_month_data_townprice_f, 'a')
	get_lastmonth_data_hourse_price_rate(content, fd_price)
	fd_price.close()	
	
if __name__=='__main__':
	main()




