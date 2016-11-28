#!/bin/bash
source ./.commonrc
scrapy crawl QichachaSpider1 &
scrapy crawl QichachaSpider2 &
scrapy crawl QichachaSpider3 &
scrapy crawl QichachaSpider4
