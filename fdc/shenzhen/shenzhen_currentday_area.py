#!/use/bin/python
#coding:utf-8

'''
shenzhen_currentday.py
shenzhen house data
URL:http://ris.szpl.gov.cn/credit/showcjgs/ysfcjgs.aspx?cjType=0
(huxing, num, area, avg_price, keshou_num, keshou_area)
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

city="'shenzhen'"
#get url content
def get_html_content(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

'''
get current data info: (city, area, num, avg_price, total_price)
content like this:
'''
def get_current_data(content, fd):
	current_data_list = []
	aimstring = get_content_between_string("商品住房按面积统计成交信息", "</table>", content)
	reg = r'(>[\d]+)'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,aimstring)
	for i in range(0, len(itemlist)):
		if '>' in itemlist[i]:
			itemlist[i] = itemlist[i].split('>')[-1]
	if len(itemlist) != 19:
		logging.error('function get_current_data(), get len(itemlist) error, is ' + str(len(itemlist)) + ' not 19')
	del itemlist[10]
	del itemlist[5]
	del itemlist[0]
	colname=['90', '90_144', '144', '144_up']
	today = datetime.date.today()
	yesterday = str(today - datetime.timedelta(days=1))
	string = ''
	for i in range(0, len(itemlist)):
		if i%4 == 0:
			string = string + city + ',' + yesterday + ',\'' + colname[i/4] + '\',' + itemlist[i] + ','
		elif (i+1) %4 == 0:
			string = string + itemlist[i] + '\n'
		else:
			string = string + itemlist[i] + ','
	fd.write(string)
url = "http://ris.szpl.gov.cn/credit/showcjgs/ysfcjgs.aspx?cjType=0"

def main():
	current_path = os.getcwd()
	current_year = datetime.datetime.now().strftime('%Y')
	dir = current_path + '/data/' + current_year
	current_day_data = dir + '/' + 'current_time_area_data.txt'
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
	get_current_data(content, fd)	
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

