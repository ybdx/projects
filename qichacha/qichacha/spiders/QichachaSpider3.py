# -*- coding: utf-8 -*-
from scrapy.spiders import BaseSpider
from qichacha.items import QichachaItem
from qichacha.url_manager import UrlManager
from scrapy.http import Request
from qichacha.conf import QICHACHA_COOKIE, KEY_WORDS_PATH, SEARCH_URL
import re
import time
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class QichachaSpider(BaseSpider):
    name = "QichachaSpider3"
    allowed_domains = ["qichacha.com"]
    start_urls = []
    key_set = set()

    def start_requests(self):
        self.read_key()
        while len(self.key_set) != 0:
            key = self.key_set.pop()
            url = SEARCH_URL.replace("{}", key)
            yield Request(url, cookies=QICHACHA_COOKIE[2],
                          callback=self.parse_url, meta={'key': key})

    def read_key(self):
        #读取已经请求过的关键字
        already_request_key_set = set()
        for i in range(1, 5):
            already_request_file = open("./data/key_words_search" + str(i) + ".txt", "r")
            for line in already_request_file.readlines():
                key = line.split("\t")[6].replace("\n", "")
                already_request_key_set.add(key)
            already_request_file.close()

        error_key_set = set()
        error_file = open("./data/error.txt", "r")
        error_file1 = open("./data/error3.txt", "r")
        for key in error_file.readlines():
            error_key_set.add(key.replace("\n", ""))
        for key in error_file1.readlines():
            error_key_set.add(key.replace("\n", ""))

        input_file = open(KEY_WORDS_PATH[2], "r")

        for line in input_file.readlines():
            key = line.split("\t")[1].replace("\n", "")
            if key not in already_request_key_set and key not in error_key_set:
                self.key_set.add(key)

        print len(already_request_key_set), "=============================="
        print len(error_key_set), "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        print len(self.key_set), "++++++++++++++++++++++++++++++++++++++++++++++"
        error_file.close()
        input_file.close()

        error_key_set.clear()
        already_request_key_set.clear()
    '''
    def get_content_request(self, response):
        # print response.request.url
        # if (response.request.url.find("\.shtml") != -1):
        #            print "1==========================================1"
        #            url = str(response.request.url)
        #            yield Request(url, cookies = self.qichacha_cookie, callback = self.get_company_info)
        #        elif (response.request.url.find("&email=&ajaxflag=true&p=") != -1):
        #            print "2==========================================2"
        #            yield Request(response.request.url, cookies = self.qichacha_cookie, callback = self.get_company_url, dont_filter = True)
        #        elif response.request.url.find("&index=0") != -1:
        key = response.meta['key']

        s = "<script>window.location.href=\'http://www.qichacha.com/index_verify?type=companysearch&back="
        if response.body.find(s) != -1 or response.body.find("您的操作过于频繁，验证后再操作") != -1:
            # self.key_set.add(key)
            kop = open("./data/search_keyword2.log", "a")
            kop.write(key)
            kop.close()
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!您的操作过于频繁，验证后再操作!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            return

        if response.body.find("您的搜索词太宽泛，建议更换一下搜索词") != -1 or (
                response.body.find("小查还没找到数据") != -1 and response.body.find("我不甘心，还想试一试") != -1):
            erroroutput = open("./data/error2.txt", "a")
            erroroutput.write(key)
            erroroutput.close()
            return
        elif response.body.find('<div class="text-left m-t-lg m-b-lg"> <ul class="pagination pagination-md">') != -1:
            if response.xpath('//div[@class="text-left m-t-lg m-b-lg"]/ul').extract()[0].find("<li") == -1:
                i = 1
                print "++++++++++++++++++++++++++++++++++++++++++++++"
                url = response.request.url + "&statusCode=&registCapiBegin=&registCapiEnd=&sortField=&isSortAsc=&province=&startDateBegin=&startDateEnd=&cityCode=&industryCode=&subIndustryCode=&tel=&email=&ajaxflag=true&p=%s" % (
                i)
                kop = open("./data/key_words1.txt", "a")
                kop.write(url + "\t" + str(i) + "\t" + key)
                kop.close()
                # yield Request(url, cookies = self.qichacha_cookie[random.randint(0, len(self.qichacha_cookie) - 1)], callback = self.get_company_url)
            else:
                text = response.xpath('//div[@class="text-left m-t-lg m-b-lg"]/ul/li/a/text()').extract()
                pageNum = ""
                if len(text) >= 7:
                    pageNum = text[6].replace(" ...", "")
                else:
                    pageNum = text[len(text) - 2]
                print "=========================================="
                for i in range(int(pageNum)):
                    url = response.request.url + "&statusCode=&registCapiBegin=&registCapiEnd=&sortField=&isSortAsc=&province=&startDateBegin=&startDateEnd=&cityCode=&industryCode=&subIndustryCode=&tel=&email=&ajaxflag=true&p=%s" % (
                    i + 1)
                    #                    time.sleep(random.uniform(0.5, 1))
                    kop = open("./data/key_words1.txt", "a")
                    kop.write(url + "\t" + pageNum + "\t" + key)
                    kop.close()
                    #   yield Request(url, cookies = self.qichacha_cookie[random.randint(0, len(self.qichacha_cookie) - 1)], callback = self.get_company_url)
        else:
            kop = open("./data/logs1.txt", "a")
            kop.write(response.request.url + "\t" + response.body)
            kop.close()
            #            return

    def get_company_info(self, response):
        # print response.body
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        if response.status != 200 or response.body == "":
            return Request(response.request.url, callback=self.basic_info)
        item = QichachaItem()
        item['url'] = response.request.url
        item['name'] = response.xpath('//span[@class="text-big font-bold"]/text()').extract()[0]

        if response.body.find('<span class="label  label-success m-l-xs">') != -1:
            item['status'] = response.xpath('//span[@class="label  label-success m-l-xs"]/text()').extract()[0]
        elif response.body.find('<span class="label label-danger m-l-xs">') != -1:
            item['status'] = response.xpath('//span[@class="label label-danger m-l-xs"]/text()').extract()[0]
        else:
            item['status'] = ""

        unique = ""
        companyname = ""
        if response.body.find('<a class="text-primary text-lg m-l" href="/company_cert?companykey=') != -1:
            s = response.xpath('//a[@class="text-primary text-lg m-l"]/@href').extract()[0]
            unique = s.split("&")[0].replace("/company_cert?companykey=", "")
            companyname = s.split("&")[1].replace("companyname=", "")
        else:
            unique = response.xpath('//input[@id="unique"]/@value').extract()[0]
            companyname = response.xpath('//input[@id="companyname"]/@value').extract()[0]
        json_url = "http://www.qichacha.com/company_getinfos?unique=%s&companyname=%s&tab=base" % (unique, companyname)
        return Request(json_url, callback=self.basic_info, meta={"item": item})

    def get_company_url(self, response):
        print "*******************************************"
        kop = open("./data/already_request_get_url.txt", "a")
        #        if(response.body == "" or response.status == 403 or response.status == 503):
        #           yield Request(response.request.url, cookies = self.qichacha_cookie, callback = self.get_content_request)
        #        else:
        if response.body.find('class="tp2_tit clear"') != -1:
            urls = response.xpath('//span[@class="tp2_tit clear"]/a/@href').extract()
            kop.write(response.request.url + "\n")
            kop.close()
            for url in urls:
                rop = open("./data/url.txt", "a")
                rop.write('http://www.qichacha.com' + url.encode('utf-8') + '\n')
                rop.close()
                # time.sleep(random.uniform(0.1, 0.3))
                yield Request("http://www.qichacha.com" + url,
                              cookies=self.qichacha_cookie[random.randint(0, len(self.qichacha_cookie) - 1)],
                              callback=self.get_company_info)

    def basic_info(self, response):
        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        basicInfo = response.xpath('//div[@class="panel-body text-sm"]/ul/li').extract()
        content = ""
        item = response.meta['item']
        for i in basicInfo:
            data, number = re.subn("<[^<>]+>", "", i)
            content += data.replace(" ", "").replace("\n", "").replace("\t", "") + "\t"
        item["info"] = content

        if item["info"] != "":
            rop = open("./data/result.txt", "a")
            rop.write(item['name'].encode('utf-8') + "\t" + item['url'].encode('utf-8') + "\t" + item['status'].encode(
                'utf-8') + item["info"].encode('utf-8') + "\n")
            rop.close()
        else:
            print "----------------------------------------------------------"
            kop = open("./data/basic_info_error.log", "a")
            kop.write(response.url + "\t" + response.body + "\n")
            kop.close()
            # yield Request(response.request.url, callback = self.basic_info, meta={"item":item}, dont_filter = True)
            #    print "============" + item["url"] + "==================" + response.body + "=================================="
            #    return Request(response.request.url, callback = self.basic_info, meta={"item":item})
            # return item
    '''

    def parse_url(self, response):
        s = "<script>window.location.href=\'http://www.qichacha.com/index_verify?type=companysearch&back="
        key = response.meta['key']
        if response.body.find(s) != -1 or response.body.find("您的操作过于频繁，验证后再操作") != -1:
            # self.key_set.add(key)
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!您的操作过于频繁，验证后再操作!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            return

        if response.body.find("您的搜索词太宽泛，建议更换一下搜索词") != -1 or (
                response.body.find("小查还没找到数据") != -1 and response.body.find("我不甘心，还想试一试") != -1):
            erroroutput = open("./data/error3.txt", "a")
            erroroutput.write(key.replace("\n", "") + "\n")
            erroroutput.close()
            return
        elif response.body.find('<td class="tp1">') != -1:
            urls = response.xpath('//td[@class="tp1"]/a/@href').extract()
            contents = response.xpath('//tr[@class="table-search-list"]').extract()
            html = response.body
            source = open("./data/source_html/" + key + ".html", "w")
            source.write(key.replace("\n", "") + "\t" + html)
            source.close()
            rop = open("./data/key_words_search3.txt", "a")

            for i in range(0, len(urls)):
                url = urls[i]
                companyName = response.xpath('//tr[@class="table-search-list"]/td[@class="tp2"]/span/a').extract()[i]
                companyName = companyName.replace("<em>", "").replace("</em>","")
                companyName, number = re.subn("<[^<>]+>", "", companyName)
                companyName = companyName.replace(" ", "").replace("\n", "").replace("\t", "")

                data = response.xpath('//tr[@class="table-search-list"]/td[@class="tp2"]').extract()[i]
                sp = data.split("</small> <small")
                name = ""
                phone = ""
                email = ""
                address = ""
                if len(sp) == 3:
                    name = sp[0].split("</span> <small")[1]
                    name, number = re.subn("<[^<>]+>", "", name)
                    name, number = re.subn("[^<>]+>", "", name)
                    name = name.replace(" ", "").replace("\n", "").replace("\t", "").replace("企业法人", "")
                    e_p = sp[1].split("</span> <span")
                    if len(e_p) == 2:
                        phone, number = re.subn("<[^<>]+>", "", e_p[0])
                        phone, number = re.subn("[^<>]+>", "", phone)
                        phone = phone.replace(" ", "").replace("\n", "").replace("\t", "")

                        email, number = re.subn("<[^<>]+>", "", e_p[1])
                        email, number = re.subn("[^<>]+>", "", email)
                        email = email.replace(" ", "").replace("\n", "").replace("\t", "")
                    elif sp[1].find('<i class="i i-phone3"></i>') != -1:
                        phone, number = re.subn("<[^<>]+>", "", sp[1])
                        phone, number = re.subn("[^<>]+>", "", phone)
                        phone = phone.replace(" ", "").replace("\n", "").replace("\t", "")
                    elif sp[1].find('<i class="fa  fa-envelope-o">') != -1:
                        email, number = re.subn("<[^<>]+>", "", sp[1])
                        email, number = re.subn("[^<>]+>", "", email)
                        email = email.replace(" ", "").replace("\n", "").replace("\t", "")
                    address, number = re.subn("<[^<>]+>", "", sp[2])
                    address, number = re.subn("[^<>]+>", "", address)
                    address = address.replace(" ", "").replace("\n", "").replace("\t", "")
                elif len(sp) == 2:
                    if sp[0].split("</span> <small")[1].find("企业法人") != -1:
                        name = sp[0].split("</span> <small")[1]
                        name, number = re.subn("<[^<>]+>", "", name)
                        name, number = re.subn("[^<>]+>", "", name)
                        name = name.replace(" ", "").replace("\n", "").replace("\t", "").replace("企业法人", "")
                    else:
                        e_p = sp[0].split("</span> <small")[1].split("</span> <span")
                        if len(e_p) == 2:
                            phone, number = re.subn("<[^<>]+>", "", e_p[0])
                            phone, number = re.subn("[^<>]+>", "", phone)
                            phone = phone.replace(" ", "").replace("\n", "").replace("\t", "")

                            email, number = re.subn("<[^<>]+>", "", e_p[1])
                            email, number = re.subn("[^<>]+>", "", email)
                            email = email.replace(" ", "").replace("\n", "").replace("\t", "")
                        elif sp[1].find('<i class="i i-phone3"></i>') != -1:
                            phone, number = re.subn("<[^<>]+>", "", sp[1])
                            phone, number = re.subn("[^<>]+>", "", phone)
                            phone = phone.replace(" ", "").replace("\n", "").replace("\t", "")
                        elif sp[1].find('<i class="fa  fa-envelope-o">') != -1:
                            email, number = re.subn("<[^<>]+>", "", sp[1])
                            email, number = re.subn("[^<>]+>", "", email)
                            email = email.replace(" ", "").replace("\n", "").replace("\t", "")
                    address, number = re.subn("<[^<>]+>", "", sp[1])
                    address, number = re.subn("[^<>]+>", "", address)
                    address = address.replace(" ", "").replace("\n", "").replace("\t", "")

                rop.write('http://www.qichacha.com' + url.encode('utf-8') + "\t" + companyName + "\t" + address + "\t" + name + "\t" + phone + "\t" + email + "\t" + key.replace("\n", "") + "\n")
            rop.close()
        else:
            kop = open("./data/logs3.txt", "a")
            kop.write(response.request.url + "\t" + response.body + "\t" + key)
            kop.close()