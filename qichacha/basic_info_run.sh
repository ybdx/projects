#!/bin/bash
source ./.commonrc
scrapy crawl QichachaBasicInfoSpider1 &
scrapy crawl QichachaBasicInfoSpider2 &
scrapy crawl QichachaBasicInfoSpider3 &
scrapy crawl QichachaBasicInfoSpider4
