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

class Segements(object):
    def __init__(self):
        self.df = pd.DataFrame()

    def excel2pd(self, filename):
        self.df = comm.Excel2pd(filename).excel2pd()

    def pd2excel(self, filename):
        comm.Df2excel(self.df).df2excel(filename)

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
    seg = Segements()
    # seg.excel2pd('patents_1134')
    seg.excel2pd('test')
    # print(seg.df)
    seg.add_col('tech')
    seg.add_col('func')
    # print(seg.df)
    num = 0
    for abstract in seg.df.ix[:,'AB']:
        if not re.search(conf.get('grammer','rejudge'), abstract):
            seg.df['tech'][num] = seg.find(abstract,conf.get('grammer','find_tech_grammer'),1,True)
        else:
            seg.df['tech'][num] = seg.find(abstract,conf.get('grammer','find_tech_grammer'),1)
            seg.df['func'][num] = seg.find(abstract,conf.get('grammer','find_func_grammer'),0)
        print('完成 ： %d' % (num+1))
        num += 1
    # print('---'*20)
    # print(seg.df['func'])
    # seg.pd2excel('test_1')
