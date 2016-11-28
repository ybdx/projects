#!/bin/bash
CURRENT_FILE_DIR="$(cd "$(dirname "$0")";pwd)"
cd $CURRENT_FILE_DIR
source ./.commonrc
scrapy crawl QichachaSpider1 &
scrapy crawl QichachaSpider2 &
scrapy crawl QichachaSpider3 &
scrapy crawl QichachaSpider4
