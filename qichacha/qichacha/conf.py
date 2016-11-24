#coding:utf-8
#全局变量

'''
qichacha_cookie = [{'PHPSESSID':'mj5i4l4n6d3ohbf3b3b617hvl4'},
                   {'PHPSESSID':'9se9vcj196svse34elpe300ln1'},
                   {'PHPSESSID':'jl0nvd61abkuqgokrdoqfoh4j4'},
                   {'PHPSESSID':'9ok1n0pttotjnft6cfnk3mefl7'},
                   {'PHPSESSID':'lt76srdq337c2roerrfivqe145'},
                   {'PHPSESSID':'t2gncinp9e8824bum5m8ga87m4'},
                   {'PHPSESSID':'irvqrlklcl2j28cv9v94k8a381'},
                   {'PHPSESSID':'bf9mof6mnb5le4g4t3t901hh70'},
                   {'PHPSESSID':'u5444sifg8vgvaefal9bvv0rk1'},
                   {'PHPSESSID':'gg33d3ckm85abbl6q3eqvr8rc0'}]
'''

#cookie
QICHACHA_COOKIE = [{'PHPSESSID': 'sa9cempc5jmckvdcvbcbi7gkj3'}, {'PHPSESSID': 'blc4rij1p88p41ihsm531i8et2'},{'PHPSESSID': '5olaq1lcbg1joau7au92kt65h0'},{'PHPSESSID': '9r7gc052ptdlqai4sol3k5p793'}]

#key_words路径
KEY_WORDS_PATH = ["./source_data/qichacha/key_words9.txt", "./source_data/qichacha/key_words10.txt", "./source_data/qichacha/key_words11.txt", "./source_data/qichacha/key_words12.txt"]

#公司基本信息的路径
BASIC_INFO_URL = "http://www.qichacha.com/company_getinfos?unique=[]&companyname={}&tab=base"

SEARCH_URL = "http://www.qichacha.com/search?key={}&index=0"

#URL and companyName路径
URL_AND_COMPANYNAME_PATH = ["./source_data/url_and_companyName/1.txt", "./source_data/url_and_companyName/2.txt", "./source_data/url_and_companyName/3.txt", "./source_data/url_and_companyName/4.txt"]

#存储爬取公司结果的路径
RESULT_PATH = ["./data/result1.txt", "./data/result2.txt", "./data/result3.txt", "./data/result4.txt"]