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
print('这里是测试内容：{}'.format(conf.get('logging','log_path')))

class Excel2pd(object):
    def __init__(self):
        self.data_path = conf.get('data_source','path')

    def excel2pd(self):
        df = pd.read_excel(self.data_path)
        return df

if __name__ == '__main__':
    test_pd = Excel2pd.excel2pd()
    print(test_pd)