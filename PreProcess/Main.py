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
        Seg.Segemnt(self.inputFile, segTmpFile)
        self.df = Seg.getDF()


if __name__ == '__main__':
    proprocess = PrePrecess('test')
    proprocess.main('seg_test')
    print(proprocess.getDF().head(5))