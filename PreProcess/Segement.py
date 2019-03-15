# -*- coding: utf-8 -*-

import CommonAPI.Common as comm
import pandas as pd
import re
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

class Segement(object):
    def __init__(self):
        self.df = pd.DataFrame()

    def getDF(self):
        return self.df

    def Segemnt(self, inputFile, outputFile=None):
        self.excel2pd(inputFile)
        self.add_col('tech')
        self.add_col('func')
        num = 0
        for abstract in self.df.ix[:, 'AB']:
            if not re.search(conf.get('grammer', 'rejudge'), abstract):
                self.df['tech'][num] = self.find(abstract, conf.get('grammer', 'find_tech_grammer'), 1, True)
            else:
                self.df['tech'][num] = self.find(abstract, conf.get('grammer', 'find_tech_grammer'), 1)
                self.df['func'][num] = self.find(abstract, conf.get('grammer', 'find_func_grammer'), 0)
            print('完成 ： %d' % (num + 1))
            num += 1
        if outputFile:
            self.pd2excel(outputFile)

    def excel2pd(self, filename):
        self.df = comm.Excel2pd(filename).excel2pd()

    def pd2excel(self, filename):
        comm.Df2excel(self.df).df2excel(filename, 'tmp')

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

    def find(self, text, regEx, tech, full=False):
        if tech == 1:
            res = comm.Segement(text).find_tech(regEx, full)
        elif tech == 0:
            res = comm.Segement(text).find_func(regEx)
        return res


if __name__ == '__main__':
    seg = Segement()
    seg.Segemnt('patents_1134')

