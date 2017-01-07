#!/use/bin/python
#coding:utf-8

'''
nanjing_currentday.py

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

city="'nanjing'"
#get url content
def get_html_content(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

#get url file
def down_file_content(url, filename):
    urllib.urlretrieve(imgurl,'/home/wln/python/pic/%s.jpg' % x)

'''
get current data info: (time, rengou, chengjiao, xinfangshangshi)
content like this:

'''
def get_current_data(content, fd):
	current_data_list = []
	reg = r'<marquee scrollDelay="150">([\s\S]*)</marquee>'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,content)
	if len(itemlist) < 1:
		logging.error('function get_current_data(), get aim string error')
		return
	item = re.split(r'(\d+)', itemlist[0].split('</span><span class="style1">')[-1])
	now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	current_data_list.append(now)
	for itm in item:
		if itm.isdigit() == True:
			current_data_list.append(itm)
		if len(current_data_list) == 4:
			break
	if len(current_data_list) != 4:
		logging.error('function get_current_data(), get data error')
	#write data to file
	fd.write(city + ",'" + str(current_data_list[0]) + "',"
			+ str(current_data_list[1]) + ',' 
			+ str(current_data_list[2]) + ',' 
			+ str(current_data_list[3])
			+ '\n')
    
	

url = "http://www.njhouse.com.cn/index_tongji.php"

def main():
	current_path = os.getcwd()
	current_year = datetime.datetime.now().strftime('%Y')
	dir = current_path + '/data/' + current_year
	current_day_data_f = dir + '/' + 'current_time.txt'
	log_record_f = dir + '/' + 'log_record.txt'
	if (os.path.exists(dir) == False):
		os.makedirs(dir)
	logging.basicConfig(level=logging.INFO,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %Y-%m-%d %H:%M:%S',
		filename=log_record_f,
		filemode='a')
	logging.info('*'*10 + '\t' + str(datetime.datetime.now()) +'\t'+ '*'*10)
	#get current data			
	fd = open(current_day_data_f, 'a')
	content = get_html_content(url)
	get_current_data(content, fd)	
	fd.close()
	
	#get disk_year_new.jpg
	urllib.urlretrieve('http://www.njhouse.com.cn/include/fdc_include/dataimg/dist_year_new.jpg',
		dir + '/' + 'disk_year_new'+ datetime.datetime.now().strftime('_%Y-%m-%d') + '.jpg')
	#get dist_day_new.jpg
	urllib.urlretrieve('http://www.njhouse.com.cn/include/fdc_include/dataimg/dist_day_new.jpg',
		dir + '/' + 'dist_day_new'+ datetime.datetime.now().strftime('_%Y-%m-%d') + '.jpg')
	urllib.urlretrieve('http://www.njhouse.com.cn/include/fdc_include/dataimg/2sf_day090703.jpg',
		dir + '/' + '2sf_lastmonth_day'+ datetime.datetime.now().strftime('_%Y-%m-%d') + '.jpg')
	
if __name__=='__main__':
	main()



