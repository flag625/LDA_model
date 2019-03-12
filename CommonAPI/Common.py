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

class Df2excel(object):
    # 获取目标dataframe
    def __init__(self, df):
        self.df = df

    def add_col(self, new_col):
        '''
        增加一个新的空数据列
        :param new_col: 新列的名称
        :return: df
        '''
        try:
            self.df[new_col] = np.empty((len(self.df),0)).tolist()
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

        return self.df


class Segement(object):
    # 按照规则一分段，NOVELTY作为技术词来源，USE和ADVANTAGE作为功效词来源
    def __init__(self, text):
        '''
        :param text: 被分段的文本
        '''
        self.text = text
        self.search_pattern = r"USE - |ADVANTAGE - |DETAILED DESCRIPTION - |DESCRIPTION OF DRAWING(S) -"

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

    def findall(self, find_regEx, tech=1):
        '''
         摘要是规范时，摘取目标段落。
        :param find_regEx: 目标对象的正则式
        :param tech: 判断，tech=1 摘取技术词段落，tech=0 摘取功效词段落
        :return:
        '''
        if tech == 1:
            try:
                self.regEx = re.compile(find_regEx)
                if not re.search(self.search_pattern, self.text):
                    self.regEx = re.compile(r"NOVELTY - (.*)")
                listOfTokens = self.regEx.search(self.text)
            except Exception as e:
                logger.info(u"失败原因：")
                logger.info(e)
                raise e

            return listOfTokens.group(1)


class PosTag(object):
    def __init__(self, doc):
        self.doc = doc

    def preprocess(self):
        '''
        词性标记
        :return: list
        '''
        sentences = nltk.sent_tokenize(self.doc)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences

    def chunking(self, grammar, sentence):
        '''
        按照语法分块
        :param grammar:  名词短语的语法规则
        :return:
        '''
        cp = nltk.RegexpParser(grammar)
        res = cp.parse(sentence)
        return res


if __name__ == '__main__':
    test_pd = Excel2pd().excel2pd()
    res = Df2excel(test_pd).add_col("tech")
    print(res)

    # 整体分段语法
    # seg_grammer_1 = r"   NOVELTY - |   USE - |   ADVANTAGE - |Advantages are: |   DETAILED DESCRIPTION - |   DESCRIPTION OF DRAWING(S) -"

    # 技术词的分段语法，有一条记录有“Advantages are: ”，手工处理
    find_nov_grammer = r"NOVELTY - (.*?)\s\s\s[A-Z][A-Z][A-Z][A-Z]*\s\-\s(.*)"

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

    # find_test = Segement(text_3).findall(find_nov_grammer)
    # print(seg_test_1)
    # print(seg_test_2)
    # print(find_test)

    # doc = u" Therefore, the invention considers the chain circuit attenuation and the effects of interference and descending load of region. " \
    #       u"Compared with traditional method based on chain circuit rate attenuation, " \
    #       u"the invention approaches to mobile station distribution method of the real WCDMA (wideband code division multiple access) system. "
    # pos_test = PosTag(doc)
    # sentence = pos_test.preprocess()
    # print(sentence)