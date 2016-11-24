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
    name = "QichachaBasicInfoSpider1"
    allowed_domains = ["qichacha.com"]

    url_set = set()

    def start_requests(self):
        self.read_company_url()
        for line in self.url_set:
            company_name = line.split("\t")[2]
            unique = line.split("\t")[3].replace("\n", "").replace("http://www.qichacha.com/firm_","").replace("http://www.qichacha.cn/firm_","").replace(".shtml", "")
            url = BASIC_INFO_URL.replace("[]", unique).replace("{}", company_name)
            yield Request(url, cookies = QICHACHA_COOKIE[0], callback = self.basic_info_parse, meta={"line":line})

    #读取公司对应的URL
    def read_company_url(self):
        file_input = open(URL_AND_COMPANYNAME_PATH[0], "r")

        if os.path.exists(RESULT_PATH[0]) is False:
            output = open(RESULT_PATH[0], "w")
            output.close()
        result_input = open(RESULT_PATH[0], "r")
        res_set = set()
        for line in result_input.readlines():
            url = line.split("\t")[2].replace("\n", "")
            res_set.add(url)

        for line in file_input.readlines():
            url = line.split("\t")[3].replace("\n", "")
            if url not in res_set:
                self.url_set.add(line)

    #抽取公司页面对应的详细信息以及保存公司对应的html文件
    def basic_info_parse(self, response):
        line = response.meta["line"]

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
            rop = open(RESULT_PATH[0], "a")
            if len(line.replace("\n", "").split("\t")) == 24:
                line = line.replace("\n", "") + "\tnull"
            rop.write(line.replace("\n", "") + "\t" + address.encode('utf-8') + "\t" + salary.encode('utf-8') + "\t" + industry.encode('utf-8') + "\t" + company_type.encode('utf-8') + "\t" + s + "\n")
            rop.close()

            html_output = open("./data/result_html/" + line.split("\t")[2] + ".html", "w")
            html_output.write(line.replace("\n", "") + "\t" + response.body)
            html_output.close()
        else:
            kop = open("./data/basic_info_error1.log", "a")
            kop.write(line.replace("\n", "") + "\n")
            kop.close()