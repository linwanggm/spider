#!/use/bin/python
#coding:utf-8

'''
hangzhou_currentday.py

hangzhou house data
URL:http://www.hzfc.gov.cn/scxx/
get 8 pictures
1. current_keshou_num
2. new_build_yushou_num
3. leiji_lastmonth_num
4. leiji_currentday_num
5. leiji_lastmonth_detail_num
6. leiji_currentday_detail_num 
7. ershou_leiji_lastmonth_detail_num
8. ershou_leiji_currentday_detail_num 

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

city="'hangzhou'"
#get url content
def get_html_content(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

url = "http://www.hzfc.gov.cn/scxx"

def main():
        current_path = os.getcwd()
        current_year = datetime.datetime.now().strftime('%Y')
        dir = current_path + '/data/' + current_year
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
        content = get_html_content(url)
        reg = r'<img src=\'([\s\S][^\n]*)\'/>'
        imgre = re.compile(reg)
        itemlist = re.findall(imgre,content)
	if len(itemlist) != 8:
		logging.error('get data fail ,the pictures is ' + len(itemlist) + ' not equal 8')
	picNameArray = ['current_keshou_num', 'new_build_yushou_num', 'leiji_lastmonth_num', 'leiji_currentday_num',
			'leiji_lastmonth_detail_num', 'leiji_currentday_detail_num', 'ershou_leiji_lastmonth_detail_num', 
			'ershou_leiji_currentday_detail_num']
        #get last month time
        d = datetime.datetime.now()
        dayscount = datetime.timedelta(days=d.day)
        dayto = d - dayscount
        date_from = datetime.datetime(dayto.year, dayto.month, 1, 0, 0, 0)
	date_from = date_from.strftime('_%Y-%m')

	for i in range(0, len(picNameArray)): 
		if i!=0 and i%2 != 0:
			urllib.urlretrieve(url + '/' + itemlist[i],
                	dir + '/' + picNameArray[i]+ datetime.datetime.now().strftime('_%Y-%m-%d') + '.jpg')
		else:
			urllib.urlretrieve(url + '/' + itemlist[i],
			dir + '/' + picNameArray[i]+ date_from+ '.jpg')
	

if __name__=='__main__':
        main()

