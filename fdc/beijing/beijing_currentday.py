#!/use/bin/python
#coding:utf-8

'''
beijing_currentday.py
beijing house data
URL:http://www.bjjs.gov.cn/tabid/2207/Default.aspx
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

#get url file
def down_file_content(url, filename):
    urllib.urlretrieve(imgurl,'/home/wln/python/pic/%s.jpg' % x)

'''
get current data info: (time, rengou, chengjiao, xinfangshangshi)
content like this:
'''
def get_current_data(content, url_2, fd):
	current_data_list = []
	reg = r'class="fontfamily">([\d\S]*)</span>'
	imgre = re.compile(reg)
	itemlist = re.findall(imgre,content)
	if len(itemlist) < 1:
		logging.error('function get_current_data(), get aim string error')
		return
	now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
	keshouqifang_str='HouseTransactionStatist_totalCount" class="fontfamily">'
	keshouqifang_zhuzhai_str = 'HouseTransactionStatist_residenceCount" class="fontfamily">'
	weiqianyue_str = 'HouseTransactionStatist_totalCount5" class="fontfamily">'
	weiqianyue_zhuzhai_str = 'HouseTransactionStatist_residenceCount5" class="fontfamily">'
	cunliangfang_str = 'SignOnlineStatistics_totalCount" class="fontfamily">'
	cunliangfang_zhuzhai_str = 'SignOnlineStatistics_residenceCount" class="fontfamily">'
	spliteArray = [keshouqifang_str, keshouqifang_zhuzhai_str, weiqianyue_str, weiqianyue_zhuzhai_str, cunliangfang_str, cunliangfang_zhuzhai_str]	
	
	for item in spliteArray:
		reg = item + '([\d]*)</span>'
		imgre = re.compile(reg)
		itemlist = re.findall(imgre,content)
		if len(itemlist) < 1:
			logging.error('function get_current_data(), ' + item)
			string = string + ',0'
		else:
			string = string + ',' + str(itemlist[0])
	fd.write(string+'\n')

url = "http://www.bjjs.gov.cn/tabid/2207/Default.aspx"
url_2 = "http://www.bjjs.gov.cn/tabid/2167/default.aspx"

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

if __name__=='__main__':
	main()

