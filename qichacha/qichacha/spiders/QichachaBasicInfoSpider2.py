# -*- coding: UTF-8 -*-
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from qichacha.conf import BASIC_INFO_URL, QICHACHA_COOKIE, URL_AND_COMPANYNAME_PATH, RESULT_PATH
import re
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')


class QichachaBasicInfoSpider(BaseSpider):
    name = "QichachaBasicInfoSpider2"
    allowed_domains = ["qichacha.com"]

    url_set = set()

    def start_requests(self):
        self.read_company_url()
        for line in self.url_set:
            company_name = line.split("\t")[2]
            unique = line.split("\t")[3].replace("\n", "").replace("http://www.qichacha.com/firm_","").replace("http://www.qichacha.cn/firm_","").replace(".shtml", "")
            url = BASIC_INFO_URL.replace("[]", unique).replace("{}", company_name)
            yield Request(url, cookies = QICHACHA_COOKIE[1], callback = self.basic_info_parse, meta={"line":line})

    #读取公司对应的URL
    def read_company_url(self):
        file_input = open(URL_AND_COMPANYNAME_PATH[1], "r")
        for i in range(0, 4):
            if os.path.exists(RESULT_PATH[i]) is False:
                output = open(RESULT_PATH[i], "w")
                output.close()
        result_input = open(RESULT_PATH[1], "r")
        res_set = set()
        for i in range(0, 4):
            result_input = open(RESULT_PATH[i], "r")
            for line in result_input.readlines():
                url = line.split("\t")[3].replace("\n", "")
                res_set.add(url)
            result_input.close()

        for line in file_input.readlines():
            url = line.split("\t")[3].replace("\n", "")
            if url not in res_set:
                self.url_set.add(line)
        res_set.clear()
        file_input.close()

    #抽取公司页面对应的详细信息以及保存公司对应的html文件
    def basic_info_parse(self, response):
        line = response.meta["line"]

        if response.body.find('请先登录或者您没有这个权限！') != -1:
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!请您登录!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            os._exit(1)
            return

        s = "<script>window.location.href=\'http://www.qichacha.com/index_verify?type=companyview&back="
        if response.body.find(s) != -1 or response.body.find("您的操作过于频繁，验证后再操作") != -1:
            # self.key_set.add(key)
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!您的操作过于频繁，验证后再操作!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            os._exit(1)
            return

        basic_info = response.xpath('//div[@class="panel-body text-sm"]/ul/li').extract()
        content = {}
        address = ""
        salary = ""
        industry = ""
        company_type = ""

        for i in basic_info:
            data, number = re.subn("<[^<>]+>", "", i)
            data = data.replace(" ", "").replace("\n", "").replace("\t", "")
            sp = data.split("：")
            content[sp[0]] = sp[1]
            if data.find("企业地址：") != -1:
                address = data.replace("企业地址：", "")
            if data.find("注册资本：") != -1:
                salary = data.replace("注册资本：", "")
            if data.find("所属行业：") != -1:
                industry = data.replace("所属行业：", "")
            if data.find("公司类型：") != -1:
                company_type = data.replace("公司类型：", "")
        s = "{"
        for key in content.keys():
            s += '"' + key + '\":\"' + content[key] + '", '
        s = s[:-2]
        s += "}"

        if len(content) != 0:
            rop = open(RESULT_PATH[1], "a")
            if len(line.replace("\n", "").split("\t")) == 24:
                line = line.replace("\n", "") + "\tnull"
            rop.write(line.replace("\n", "") + "\t" + address.encode('utf-8') + "\t" + salary.encode('utf-8') + "\t" + industry.encode('utf-8') + "\t" + company_type.encode('utf-8') + "\t" + s + "\n")
            rop.close()

            html_output = open("./data/result_html/" + line.split("\t")[2] + ".html", "w")
            html_output.write(line.replace("\n", "") + "\t" + response.body)
            html_output.close()
        else:
            kop = open("./data/basic_info_error2.log", "a")
            kop.write(line.replace("\n", "") + "\n")
            kop.close()
