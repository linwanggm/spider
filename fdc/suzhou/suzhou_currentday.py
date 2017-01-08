#!/use/bin/python
#coding:utf-8

'''
suzhou_currentday.py

suzhou house data
URL: http://http://www.szfcweb.com/szfcweb/(S(0nfyxkjwmr13jrei5j0sk255))/DataSerach/XSFWINFO.aspx

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

city="'suzhou'"
#get url content
def get_html_content(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

#get url file
def down_file_content(url, filename):
    urllib.urlretrieve(imgurl,'/home/wln/python/pic/%s.jpg' % x)

'''
get current data info: (city, time, town, day_total_num, day_total_area, day_zhuzhai_num, day_zhuzhai_area, keshou_zhuzhai_num, keshou_feizhuzhai_num, keshou_total_num)
content like this:

'''
def get_current_data(content, fd):
	#print content
	current_data_list = []
	#town name list
	reg = r'rowspan="2">([\S][^<]*)</th>'
	imgre = re.compile(reg)
	namelist = re.findall(imgre,content)
	if len(namelist) < 1:
		logging.error('function get_current_data(), get aim string error')
		return
	#total num
	reg = r'</td><td>([\d]+)</td><td>'
	imgre = re.compile(reg)
	totalNumList = re.findall(imgre,content)
	#total_area
	reg = r'</td><td>([\d\.]+)</td>[^<]'
	imgre = re.compile(reg)
	totalAreaList = re.findall(imgre,content)	
	#zhuzhai num
	reg = r'</td><td class="alt">([\d]+)</td><td class="alt">'
	imgre = re.compile(reg)
	zhuzhaiNumList = re.findall(imgre,content)
	#zhuzhai area
	reg = r'</td><td class="alt">([\d\.]+)</td>[^<]'
	imgre = re.compile(reg)
	zhuzhaiAreaList = re.findall(imgre,content)
	len_namelist = len(namelist)
	#print len_namelist
	#print totalNumList
	#print totalAreaList
	#print zhuzhaiNumList
	#print zhuzhaiAreaList
	#get total num
	content = get_html_content(url_2)
	reg = r'</td><td width="150">([\d]+)[^\d]'
	imgre = re.compile(reg)
	keshou_total = re.findall(imgre,content)
	if len(totalNumList) != len_namelist or len(totalAreaList) != len_namelist or \
		len(zhuzhaiNumList) != len_namelist or len(zhuzhaiAreaList) != len_namelist \
		or len(keshou_total)/3 != len_namelist:
		logging.error('the len arrays are not the same')
		return
	
	now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	for i in range(0, len(namelist)):
		fd.write(city + ",'" + now + ",'" + str(namelist[i]) + "'," + str(totalNumList[i]) + "," \
		+ str(totalAreaList[i]) + "," + str(zhuzhaiNumList[i]) + "," + str(zhuzhaiAreaList[i]) + "," + \
		str(keshou_total[i*3]) + "," + str(keshou_total[i*3+1]) + "," + str(keshou_total[i*3+2])+'\n')
    
	

url = "http://www.szfcweb.com/szfcweb/(S(0nfyxkjwmr13jrei5j0sk255))/DataSerach/XSFWINFO.aspx"
url_2 = "http://www.szfcweb.com/szfcweb/(S(zujkokvkaefkfh45joaxcsja))/DataSerach/CanSaleHouseGroIndex.aspx"
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
	logging.info('*'*10 + '\t' + city + '  ' + str(datetime.datetime.now()) +'\t'+ '*'*10)
	#get current data			
	fd = open(current_day_data_f, 'a')
	content = get_html_content(url)
	get_current_data(content, fd)	
	fd.close()
	

	
if __name__=='__main__':
	main()



