#!/use/bin/python
#coding:utf-8

'''
beijing_currentday.py
nanjing house data
URL:http://www.bjjs.gov.cn/bjjs/fwgl/fdcjy/index.shtml
1. qiFangWangQian (num, area, zhuzhai_num, zhuzhai_area)
2. xianFangWangQian (num, area, zhuzhai_num, zhuzhai_area)
3. CunLiangFangWangQian (num, area, zhuzhai_num, zhuzhai_area)
4. keshou_fangzi(keshouqifang_num, keshouqifang_zhuzhai_num, weiqianyuexianfang_num, weiqianyuxianfang_zhuzhai_num, keshoucunliangfang_num, keshoucunliangfang_zhuzhai_num)
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

city="'beijing'"
#get url content
def get_html_content(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

'''
get current data info: (time, rengou, chengjiao, xinfangshangshi)
content like this:
'''
def get_current_data(content, url_2, fd):
	current_data_list = []
	aimstring = get_content_between_string('<div class="fdcsjtj_content">', '</html>', content)
	reg = r'([^A-Za-z>][\d-]+)'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,aimstring)
	if len(itemlist) < 1:
		logging.error('function get_current_data(), get aim string error')
		return
	for itm in itemlist:
		item = itm.split('(')[0]
		current_data_list.append(item)
	if len(current_data_list) != 15:
		logging.error('function get_current_data(), get data error')
		return
	#write data to file
	string = city + ','
	for i in range(0, len(current_data_list)-1):
		if i % 5 == 0 and i != 0:
			continue
		else:
			string = string + current_data_list[i] + ','
	string = string + current_data_list[-1]
	#get the keshouqifang, weiqianyue, cunliangfang data
	content = get_html_content(url_2)
	aimstring = get_content_between_string("可售房屋套数", "</td></tr>", content)
	reg = r'(?<=>)\d+'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,aimstring)
	keshouqifang_total = itemlist[-1]
	aimstring = get_content_between_string("住宅套数", "</td></tr>", content)
	reg = r'(?<=>)\d+'
	imgre = re.compile(reg)
	itemlist_zhuzhai = re.findall(imgre,aimstring)
	keshouqifang_zhuzhai = itemlist_zhuzhai[0]
	string = string + ',' + keshouqifang_total + ',' + keshouqifang_zhuzhai
	#weiqianyue
	aimstring = get_content_between_string("未签约套数", "</td></tr>", content)
	reg = r'(?<=>)\d+'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,aimstring)
	weiqianyue_total = itemlist[-1]	
	weiqianyue_zhuzhai = itemlist_zhuzhai[4]
	string = string + ',' + weiqianyue_total + ',' + weiqianyue_zhuzhai
	#cunliangfang
	aimstring = get_content_between_string("可售房源套数", "</tr>", content)
	reg = r'\s\d+'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,aimstring)
	cunliangfang_total = itemlist[-1]	
	aimstring = get_content_between_string("可售住宅套数", "</tr>", content)
	reg = r'\s\d+'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,aimstring)
	cunliangfang_zhuzhai = itemlist[-1]	
	string = string + ',' + cunliangfang_total + ',' + cunliangfang_zhuzhai
	fd.write(string+'\n')

url = "http://www.bjjs.gov.cn/bjjs/fwgl/fdcjy/index.shtml"
url_2 = "http://www.bjjs.gov.cn/bjjs/fwgl/fdcjy/fwjy/index.shtml"

def main():
	current_path = os.getcwd()
	current_year = datetime.datetime.now().strftime('%Y')
	dir = current_path + '/data/' + current_year
	current_day_data = dir + '/' + 'current_time_data.txt'
	log_record_f = dir + '/' + 'log_record.txt'
	if (os.path.exists(dir) == False):
		os.makedirs(dir)
	logging.basicConfig(level=logging.INFO,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %Y-%m-%d %H:%M:%S',
		filename=log_record_f,
		filemode='a')
	logging.info('*'*10 + '\t' + city + ' ' + str(datetime.datetime.now()) +'\t'+ '*'*10)
	#get current data			
	fd = open(current_day_data, 'a')
	content = get_html_content(url)
	get_current_data(content, url_2, fd)	
	fd.close()

def get_content_between_string(str1, str2, content):
	contentArray = content.split('\n')
	returnStr = ''
	begin = False
	for item in contentArray:
		if str1 in item:
			begin = True
		if begin == True and str2 in item:
			returnStr = returnStr + str(item) + '\n'
			begin = False
		if begin == True:
			returnStr = returnStr + str(item) + '\n'
	return returnStr

if __name__=='__main__':
	main()

