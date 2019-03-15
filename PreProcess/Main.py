# -*- coding: utf-8 -*-

import nltk
import pandas as pd
from CommonAPI import Common as comm
from PreProcess import Segement as seg
from PreProcess import Chunking as chu

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

class PrePrecess(object):
    def __init__(self, inputFile, outputFile=None):
        self.df = pd.DataFrame()
        self.inputFile = inputFile
        self.outputFile = outputFile

    def getDF(self):
        return self.df

    def main(self,segTmpFile=None):
        Seg = seg.Segement()
        print("开始技术词和功效词分段：")
        Seg.Segemnt(self.inputFile, segTmpFile)
        print("----"*20)
        self.df = Seg.getDF()
        self.add_col('tech_chunk')
        print("开始技术词分块：")
        self.techChunk()
        self.pd2excel('techChunk_test')
        print("----"*20)

    def techChunk(self):
        num = 0
        for doc in self.df.ix[:, 'tech']:
            if doc:
                chunk = chu.Chunking(num+1)
                chunk.doc_chunking(conf.get('grammer', 'tech_np_grammer'), doc)
                res = chunk.getNounPhrases()
                self.df['tech_chunk'][num] = res
                del chunk
            num += 1

    def add_col(self, colname):
        '''
        增加一个新的空数据列
        :param new_col: 新列的名称
        '''
        try:
            self.df[colname] = None
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e

    def pd2excel(self, filename):
        comm.Df2excel(self.df).df2excel(filename, 'tmp')


if __name__ == '__main__':
    proprocess = PrePrecess('test')
    proprocess.main('seg_test')
    # print(proprocess.getDF().head(5))