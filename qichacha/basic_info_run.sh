#!/bin/bash
CURRENT_FILE_DIR="$(cd "$(dirname "$0")";pwd)"
cd $CURRENT_FILE_DIR
source ./.commonrc
scrapy crawl QichachaBasicInfoSpider1 &
scrapy crawl QichachaBasicInfoSpider2 &
scrapy crawl QichachaBasicInfoSpider3 &
scrapy crawl QichachaBasicInfoSpider4
