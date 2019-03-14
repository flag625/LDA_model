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

    def doc_chunking(self, grammer, document):
        listOfsents = self.preprocess(document)
        for sent in listOfsents:
            self.sent_chunking(grammer, sent)

    def preprocess(self, document):
        listOfsents = comm.PosTag().preprocess(document)
        return listOfsents

    def sent_chunking(self, grammer, sent):
        sentTree = comm.PosTag().chunking(grammer, sent)
        self.traverse(sentTree)

    def getNounPhrases(self):
        res = ', '.join(np for np in self.NounPhrases)
        return res

    def traverse(self, sentTree):
        try:
            sentTree.label()
        except AttributeError:
            return
        else:
            if sentTree.label() == 'NP':
                # print(sentTree)
                tmp = ' '.join(word  for word, tag in sentTree.leaves())
                self.NounPhrases.append(tmp)
            else:
                for child in sentTree:
                    self.traverse(child)

    # def extract_np(self, sentTree):
    #     for subtree in sentTree.subtrees():
    #         if subtree.label() == 'NP':
    #             yield ' '.join(word for word, tag in subtree.leaves())


# class UnigramChunker(nltk.ChunkinghunkParserI):



if __name__ == '__main__':
    doc = "The mobile IP burst flow rate remitting and regulating method is to " \
          "establish multiple label swap paths LSP's by " \
          "utilizing the bandwidth the links of all the reachable paths in local network provide between " \
          "the label edge router SLER for the mobile node MN to access to the local network " \
          "and each of the boundary gateway label swap router DLSR of local network " \
          "and to disperse the burst mobile IP data flows onto the LSP's so that the burst mobile IP data flows shunt " \
          "in the local network can influx the boundary gateway label swap router DLSR. " \
          "The mobile IP burst flow rate remitting and regulating method includes two steps: " \
          "seeking and establishing several LSP's and distributing the available bandwidth among the mobile IP users. " \
          "The method can 'dilute' the concentrated burst flows to the wholelocal network to " \
          "eliminate jamming while maintaining the stable local flow rate characteristic. "

    doc2 = "ensuring reusability of protocol related layer furthest, avoiding rehandling development procedure for testing set. " \
           "The invention possesses high generality, reusability and extensibility. "

    grammer = r"""
    NP:{<DT|PP\$>?<JJ>*<NN|NNP>}
       {<NNP>+}
    """
    tech_term_grammer = r"""
        NP:{<NN>}
           {<JJ><NN|NNS>}
           {<VBG><NN>}
           {<NN><NN>}
           {<NN><NN><NN>}
           {<JJ><NN><NN>}
           {<JJ><JJ><NN>}
           {<JJ><VBG><NN>}
           {<JJR><NN><NN>}
           {<RB><NN><NN>}
           {<NN><VBG><NN>}
           {<VBN><NN><NN>}
           {<VBG><NN><NN>}
           {<JJ><JJ><NN><NN>}
           {<RB><JJ><NN><JJ><NN>}
           {<JJ><NN><NN><NN>}
           {<NN><JJ><VBG><NN>}        
        """

    tech_np_grammer = r"""
        NP:{<DT|CD|PRP\$>?<JJ|JJR|JJS>*<VBN>*<NN|NNS|NNP|NNPS>+}
           {<NN|NNS|NNP|NNPS>*<VBG>+<NN|NNS|NNP|NNPS>+}
           {<NN|NNS|NNP|NNPS>*<JJ|JJR|JJS>*<VBN>+<NN|NNS|NNP|NNPS>+}
           {<RB|RBR|RBS>+<JJ|JJR|JJS>*<NN|NNS|NNP|NNPS>*<JJ|JJR|JJS>*<NN|NNS|NNP|NNPS>+}
        """

    func_np_grammer = r"""
        NP:{<NN|NNP|NNS|NNPS>+<BEZ|BER><VBN>}
           {<VBG|VBZ>?<DT|CD>?<JJ|JJR|JJS|>*<NN|NNS|NNP|NNPS>+<RB|RBR|RBS>?<CC>?<NN|NNS|NNP|NNPS>?<VBG>?}
           {<TO><VB><DT|CD>?<NN|NNS|NNP|NNPS>+}
           {<VBN>?<RB|RBR|RBS>+<CC>?<RB|RBR|RBS>?}
           {<JJ|JJR|JJS>+}
        """



    # chunk1 = Chunking()
    # chunk1.doc_chunking(tech_term_grammer, doc)
    # res1 = chunk1.getNounPhrases()
    # print(res1)
    #
    # chunk2 = Chunking()
    # chunk2.doc_chunking(tech_np_grammer, doc)
    # res2 = chunk2.getNounPhrases()
    # print(res2)

    chunk3 = Chunking()
    chunk3.doc_chunking(func_np_grammer, doc2)
    res3 = chunk3.getNounPhrases()
    print(res3)

