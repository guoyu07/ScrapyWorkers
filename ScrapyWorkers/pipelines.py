# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from ScrapyWorkers.PipeLines.scrapy_mongodb import MongoDBPipeline

class ScrapyworkersPipeline(object):
    def process_item(self, item, spider):
        return item

MongoDBPipeline = MongoDBPipeline