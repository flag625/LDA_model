# -*- coding: utf-8 -*-

import pandas as pd
import json
import os
import string
from collections import Counter
import nltk
import logging.config
import configparser

conf = configparser.ConfigParser()
conf.read("../CommonAPI/comm.conf")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler(conf.get('logging','log_path'), mode='a')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
print('这里是测试内容：{}'.format(conf.get('data_source','path')))

class Excel2pd(object):

    # 获取数据源地址
    def __init__(self):
        self.data_path = conf.get('data_source','path')

    # 将Excel文件转化为dataframe,并返回
    def excel2pd(self):
        try:
            df = pd.read_excel(self.data_path)
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

        return df

class Segement(object):
    def __init__(self, regEx, article):
        self.regEx = regEx
        self.article = article



if __name__ == '__main__':
    test_pd = Excel2pd().excel2pd()
    print(test_pd)