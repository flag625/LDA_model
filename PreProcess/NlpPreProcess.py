# -*- coding: utf-8 -*-
'''
对筛选出来的技术词和功效词进行再处理，形成可以进行LDA分析的词袋，同时统计词频
'''

import codecs
import pandas as pd
import json
import os
import string
from collections import Counter
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet

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
# print('这里是测试内容：{}'.format(conf.get('data_source','path'))

class NlpPreProcess(object):
    def __init__(self, stopfile=None):
        super(NlpPreProcess, self).__init__()
        self.wml = WordNetLemmatizer() # 词形还原
        self.ps = PorterStemmer() # 词干提取
        with codecs.open(stopfile, 'r', 'utf-8') as f:
            self.stoplist = f.read().splitlines() #停用词表
        print("the num of stopwords is %s" %len(self.stoplist))
        self.Num = 0

    def preprocessFile(self, filePath):
        '''
        去标点，去数字，分割单词，词形还原
        :param filePath: 待处理的文本路径
        :return:
        '''
        print('begin process %s' %filePath)
        df = pd.read_excel(filePath)
        dictWord = {}
        freWord = Counter()
        saveFile = codecs.open(conf.get('result', 'path')+os.sep+'docwords.json', 'w', 'utf-8')
        freFile = os.path.join(conf.get('result', 'path'), 'frequence_clean.xlsx')
        num = 0
        for dic in df.ix[:, 'tech_func']:
            doc = str(dic).lower()
            for c in string.punctuation:
                doc = doc.replace(c, ' ')
            for c in string.digits:
                doc = doc.replace(c, '')
            doc = nltk.word_tokenize(doc)
            cleanDoc = []
            for word in doc:
                if wordnet.synsets(word) and word not in self.stoplist:
                    word = self.wml.lemmatize(word) # 词形还原
                    cleanDoc.append(word)
            freWord += Counter(cleanDoc)
            dictWord['content'] = ' '.join(cleanDoc) #保存为Json文件
            json.dump(dictWord, saveFile, ensure_ascii=False)
            saveFile.write('\n')
            num += 1
        pd.DataFrame.from_dict(dict(freFile), orient='index').to_excel(freFile)
        print('---'*20)