# -*- coding: utf-8 -*-

import nltk

from CommonAPI import Common as comm

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

# 提取目标短语块
class Chunking(object):
    def __init__(self):
        self.NounPhrases = []

    def preprocess(self, document):
        listOfsents = comm.PosTag().preprocess(document)
        return listOfsents

    def chunking(self, grammer, sent):
        sentTree = comm.PosTag().chunking(grammer, sent)
        self.traverse(sentTree)
        return self.NounPhrases

    def traverse(self, sentTree):
        try:
            sentTree.label()
        except AttributeError:
            return
        else:
            if sentTree.label() == 'NP':
                print(sentTree)
                tmp = ' '.join(word  for word, tag in sentTree.leaves())
                self.NounPhrases.append(tmp)
            else:
                for child in sentTree:
                    self.traverse(child)

    def extract_np(self, sentTree):
        for subtree in sentTree.subtrees():
            if subtree.label() == 'NP':
                yield ' '.join(word for word, tag in subtree.leaves())


# class UnigramChunker(nltk.ChunkinghunkParserI):



if __name__ == '__main__':
    doc = "The mobile IP burst flow rate remitting and regulating method is to " \
          "establish multiple label swap paths LSP's by " \
          "utilizing the bandwidth the links of all the reachable paths in local network provide between " \
          "the label edge router SLER for the mobile node MN to access to the local network " \
          "and each of the boundary gateway label swap router DLSR of local network " \
          "and to disperse the burst mobile IP data flows onto the LSP's so that the burst mobile IP data flows shunt " \
          "in the local network can influx the boundary gateway label swap router DLSR. " \
          "The mobile IP burst flow rate remitting and regulatingmethod includes two steps: " \
          "seeking and establishing several LSP's and distributing the available bandwidth among the mobile IP users. " \
          "The method can 'dilute' the concentrated burst flows to the wholelocal network to " \
          "eliminate jamming while maintaining the stable local flow rate characteristic. "

    grammer = r"""
    NP:{<DT|PP\$>?<JJ>*<NN|NNP>}
       {<NNP>+}
    """
    chunk = Chunking()
    sentences = chunk.preprocess(doc)
    # for sentence in sentences:
    #     print(sentence)

    res = chunk.chunking(grammer, sentences[1])
    print(res)
    # print(type(res))
    # res.draw()
