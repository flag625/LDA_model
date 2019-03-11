# -*- coding: utf-8 -*-

import pandas as pd
import json
import os
import string
import re
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
    # 按照规则一分段，NOVELTY作为技术词来源，USE和ADVANTAGE作为功效词来源
    def __init__(self, regEx, text):
        '''
        :param regEx: 分段正则式
        :param text: 被分段的文本
        '''
        self.regEx = re.compile(regEx)
        self.text = text

    def segement(self):
        '''
        分段
        :return: list
        '''
        try:
            listOfTokens = self.regEx.split(self.text)
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

        return listOfTokens

class PosTag(object):
    def __init__(self, doc):
        self.doc = doc

    # 词性标记
    def preprocess(self):
        sentences = nltk.sent_tokenize(self.doc)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences

    # 按照语法分块
    def chunking(self, grammar, sentence):
        '''
        :param grammar:  名词短语的语法规则
        :return:
        '''
        cp = nltk.RegexpParser(grammar)
        res = cp.parse(sentence)
        return res


if __name__ == '__main__':
    #test_pd = Excel2pd().excel2pd()
    #print(test_pd)

    doc = u" Therefore, the invention considers the chain circuit attenuation and the effects of interference and descending load of region. " \
          u"Compared with traditional method based on chain circuit rate attenuation, " \
          u"the invention approaches to mobile station distribution method of the real WCDMA (wideband code division multiple access) system. "
    pos_test = PosTag(doc)
    sentence = pos_test.preprocess()
    print(sentence)