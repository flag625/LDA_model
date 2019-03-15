# -*- coding: utf-8 -*-

import nltk
import pandas as pd
from CommonAPI import Common as comm
from PreProcess import Segement as seg
from PreProcess import Chunking as chu
from PreProcess import NlpPreProcess as nlp

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
        '''
        预处理主要步骤
        :param segTmpFile: 分段处理后保存的过渡文件名
        :return:
        '''
        # 分段
        Seg = seg.Segement()
        print("开始技术词和功效词分段：")
        Seg.Segemnt(self.inputFile, segTmpFile)
        print("----"*20)
        self.df = Seg.getDF()
        # 分块
        print("开始技术词分块：")
        self.chunk()
        print("----"*20)
        print("开始功效词分块：")
        self.chunk(0)
        print("----" * 20)
        self.mergeTechFunc()
        nlp.NlpPreProcess().preprocessFile(dataframe=self.df)
        self.pd2excel('chunk_test')

    def chunk(self, tech=1):
        '''
        技术词和功效词分块
        :param tech: 默认1，选择技术词分块；0，选择功效词分块
        :return:
        '''
        num = 0
        grammer = 'tech'
        if not tech:
            grammer = 'func'
        self.add_col(grammer + '_chunk')
        for doc in self.df.ix[:, grammer]:
            if doc:
                chunk = chu.Chunking(num+1)
                chunk.doc_chunking(conf.get('grammer', grammer+'_np_grammer'), doc)
                res = chunk.getNounPhrases()
                self.df[grammer+'_chunk'][num] = res
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

    def mergeTechFunc(self):
        try:
            self.add_col('tech_func')
            for num in range(len(self.df)):
                if self.df['func'][num]:
                    self.df['tech_func'][num] = self.df['tech'][num] + ' ' + self.df['func'][num]
                else:
                    self.df['tech_func'][num] = self.df['tech'][num]
        except Exception as e:
            logger.info(u"失败原因：")
            logger.info(e)
            raise e


if __name__ == '__main__':
    proprocess = PrePrecess('test')
    proprocess.main('seg_test')
    # print(proprocess.getDF().head(5))