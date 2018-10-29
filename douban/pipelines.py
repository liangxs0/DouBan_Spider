# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import codecs

class DoubanPipeline(object):
    def __init__(self):
        self.file = codecs.open('mian.txt','a+',encoding='utf-8')
    def process_item(self, item, spider):
        # 获取当前工作目录
        self.file.write(item['comment'])
        print('数据写入')
        return item
    def spider_closed(self):
        self.file.close()
