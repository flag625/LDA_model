# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
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
# print('这里是测试内容：{}'.format(conf.get('data_source','path')))

class Excel2pd(object):

    # 获取数据源地址
    def __init__(self, file_name):
        self.data_path = os.path.join(conf.get('data_source','path'),file_name+'.xlsx')

    # 将Excel文件转化为dataframe,并返回
    def excel2pd(self):
        try:
            df = pd.read_excel(self.data_path)
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

        return df

class Df2excel(object):
    # 获取目标dataframe
    def __init__(self, df):
        self.df = df

    def df2excel(self, file_name, pathChose='result',):
        '''
        dataframe转换为Excel, 保存在tmp文件夹
        :param file_name: 保存文件名
        :param pathChose: 保存路径选择，默认'result' Result文件夹，可选'tmp' tmp文件夹
        :return:
        '''
        file_path = os.path.join(conf.get(pathChose,'path'),file_name+'.xlsx')
        try:
            self.df.to_excel(file_path, encoding='utf-8', index=False)
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

# 分段，将技术词来源和功效词来源分开
class Segement(object):
    # 按照规则一分段，NOVELTY作为技术词来源，USE和ADVANTAGE作为功效词来源
    def __init__(self, text):
        '''
        :param text: 被分段的文本
        '''
        self.text = text

    def segement(self, regEx):
        '''
        分段
        :param regEx: 分段正则式
        :return: list
        '''
        try:
            self.regEx = re.compile(regEx)
            listOfTokens = self.regEx.split(self.text)
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

        return listOfTokens

    def find_tech(self, find_regEx, full=False):
        '''
         摘取技术词段落。
        :param find_regEx: 目标对象的正则式
        :param full: 判断摘要是否只有NOVELTY部分，默认为False
        :return: 目标段落
        '''
        self.regEx = re.compile(find_regEx)
        try:
            if full:
                self.regEx = re.compile(conf.get('grammer','find_tech_full_grammer'))
            listOfTokens = self.regEx.search(self.text)
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

        return listOfTokens.group(1)

    def find_func(self, find_regEx):
        '''
         摘取功效词段落。
        :param find_regEx: 目标对象的正则式
        :return: 目标段落
        '''
        self.regEx = re.compile(find_regEx)
        try:
            listOfTokens = self.regEx.search(self.text)
            if not listOfTokens:
                listOfTokens = re.search(conf.get('grammer','find_func_use_grammer'),self.text)
                if not listOfTokens:
                    listOfTokens = re.search(conf.get('grammer','find_func_adv_grammer'),self.text)
                res = listOfTokens.group(1)
            else:
                res = listOfTokens.group(1) + listOfTokens.group(2)
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

        return res


class PosTag(object):
    def preprocess(self, document):
        '''
        分句，分词，标记词性
        :param document: 被处理的一个文本
        :return: [list of sentance1:(tunple of word1(word1, postag), ...),list of sentance2,... ]
        '''
        try:
            sentences = nltk.sent_tokenize(document)
            sentences = [nltk.word_tokenize(sent) for sent in sentences]
            sentences = [nltk.pos_tag(sent) for sent in sentences]
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

        return sentences

    def chunking(self, grammar, sentence):
        '''
        获取目标分块
        :param grammar: 分块语法
        :param sentence: list of sentance:(tunple of word1(word1, postag), ...)
        :return: NLTK tree
        '''
        try:
            cp = nltk.RegexpParser(grammar)
            sentTree = cp.parse(sentence)
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

        return sentTree


if __name__ == '__main__':
    test_pd = Excel2pd('test').excel2pd()
    # print(test_pd)
    # print(test_pd.ix[:,['AB ']])
    # tmp = Df2excel(test_pd)
    # res = tmp.add_col("tech")
    # tmp.df2excel("tmp")
    # print(res)

    # 分段语法，以USE为界将文本分成两部分
    seg_grammer_1 = r'USE - '

    # 判断摘要是否只要NOVELTY部分
    # search_pattern = r"USE - |ADVANTAGE - |DETAILED DESCRIPTION - |DESCRIPTION OF DRAWING(S) -"
    search = r'USE - |ADVANTAGE - |Advantages are: |DETAILED DESCRIPTION - |DESCRIPTION OF DRAWING(S) -'
    num = 1
    for doc in test_pd.ix[:,1]:
        test = re.search(search, doc)
        print(num)
        print(test)
        num += 1

    # 技术词的分段语法，有一条记录有“Advantages are: ”，手工处理
    find_nov_grammer = r'NOVELTY - (.*?)\s\s\s[A-Z][A-Z][A-Z][A-Z]*\s-\s(.*)'

    # 功效词的分段语法
    find_fun_grammer = r'USE - (.*?)ADVANTAGE - (.*?)\s\s\s[A-Z]*\s[A-Z]*\s-\s(.*)'

    # 功效词-USE部分的分段语法
    find_use_grammer = r'USE - (.*?)\s\s\s[A-Z][A-Z][A-Z][A-Z]*\s-\s(.*)'

    # 功效词-ADVANTAGE部分的分段语法
    find_adv_grammer = r'ADVANTAGE - (.*?)\s\s\s[A-Z]*\s[A-Z]*\s-\s(.*)'

    text_1 = u"   NOVELTY - The method involves sending a maximum distributable bandwidth by a node to acquire data. " \
           u"Use status of a network resource is confirmed based on a comparison result with a threshold value. " \
           u"The bandwidth to send data is confirmed based on the status. " \
           u"The data is sent to another node by the former node based on the bandwidth. " \
           u"A request time used by the former node to acquire a data sending right is compared with an average time of the former node. " \
           u"Maximum and minimum distributable bandwidths are distributed to the former node, " \
           u"if time rate is more than and less than respective threshold values.    " \
           u"USE - Method for sending data in a distributed non-cooperative network grid.    " \
           u"ADVANTAGE - The method utilizes the resource in a reasonable manner, and prevents the nodes from occupying a channel, " \
           u"so that other nodes do not acquire the bandwidth, thus prolonging the delay.    " \
           u"DETAILED DESCRIPTION - INDEPENDENT CLAIMS are also included for the following:    " \
           u"(1) a data sending system in distributed non-cooperative network grid    " \
           u"(2) a data sending node in distributed non-cooperative network grid.    " \
           u"DESCRIPTION OF DRAWING(S) - The drawing shows a flow diagram of a data sending method. `(Drawing includes non-English language text)` "

    text_2 = "   NOVELTY - Core of the invention is that based on condition of protocol test, levels of units not related to protocol, " \
             "and units related to protocol are divided. " \
             "The units not related to protocol executes operation processes, " \
             "which are not related to specific content of protocol and are suitable to test any protocol. " \
             "The units related to protocol is in charge of operation processes for specific testing protocol. " \
             "Further, the invention marks off corresponding general procedure module for protocol test from units related to " \
             "protocol as a common part in use for testing each protocol repeatedly. " \
             "Advantages are: ensuring reusability of protocol related layer furthest, " \
             "avoiding rehandling development procedure for testing set. " \
             "The invention possesses high generality, reusability and extensibility. "

    text_3 = "   NOVELTY - The disclosed forming method for broadband waveform comprises: " \
             "determining the sub-band signal opposite to the microphone signal, " \
             "as well as the signal frequency-domain correlation matrix; " \
             "according to 3D space transmission vector of signal source and former matrix, determining the weight vector for every sub-band signal; " \
             "then deciding the output signal. " \
             "This invention combines frequency and spacedomain for speech process, and improves SNR for wide application. "

    # seg_test_1 = Segement(text_1).segement(seg_grammer_1)
    # seg_test_2 = Segement(text_2).segement(seg_grammer_1)

    # use = re.search(conf.get('grammer','find_tech_grammer'), text_1)
    # print(use.group(1))
    # print(use.group(2))

    # func_test = Segement(text_1).find_func(find_fun_grammer)
    # print(func_test)

    # adv = re.search(find_adv_grammer, text_1)
    # print(adv.group(1))

    # find_test = Segement(text_3).findall(find_nov_grammer)
    # print(seg_test_1)
    # print(seg_test_2)
    # print(find_test)

    # use_list = Segement(text_1).findall(find_use_grammer, tech=0)
    # print(use_list)

    # doc = u" Therefore, the invention considers the chain circuit attenuation and the effects of interference and descending load of region. " \
    #       u"Compared with traditional method based on chain circuit rate attenuation, " \
    #       u"the invention approaches to mobile station distribution method of the real WCDMA (wideband code division multiple access) system. "
    # pos_test = PosTag(doc)
    # sentence = pos_test.preprocess()
    # print(sentence)