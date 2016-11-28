#coding:utf-8
#全局变量


#亚超的cookie:     {'PHPSESSID':'t0baobm22gkocnk1399sc12ev4'},
#王垚的cookie      {'PHPSESSID':'blc4rij1p88p41ihsm531i8et2'},
#姜雪的cookie：    {'PHPSESSID':'hjf4pcq96oagajnbcoqu3emrm4'},
#冯璐的cookie：    {'PHPSESSID':'9r7gc052ptdlqai4sol3k5p793'},

#cookie
QICHACHA_COOKIE = [{'PHPSESSID': 't0baobm22gkocnk1399sc12ev4'}, {'PHPSESSID': 'blc4rij1p88p41ihsm531i8et2'},{'PHPSESSID': 'hjf4pcq96oagajnbcoqu3emrm4'},{'PHPSESSID': '9r7gc052ptdlqai4sol3k5p793'}]

#key_words路径
KEY_WORDS_PATH = ["./source_data/qichacha/key_words9.txt", "./source_data/qichacha/key_words10.txt", "./source_data/qichacha/key_words11.txt", "./source_data/qichacha/key_words12.txt"]

#公司基本信息的路径
BASIC_INFO_URL = "http://www.qichacha.com/company_getinfos?unique=[]&companyname={}&tab=base"

SEARCH_URL = "http://www.qichacha.com/search?key={}&index=0"

#URL and companyName路径
URL_AND_COMPANYNAME_PATH = ["./source_data/url_and_companyName/1.txt", "./source_data/url_and_companyName/2.txt", "./source_data/url_and_companyName/3.txt", "./source_data/url_and_companyName/4.txt"]

#存储爬取公司结果的路径
RESULT_PATH = ["./data/result1.txt", "./data/result2.txt", "./data/result3.txt", "./data/result4.txt"]
