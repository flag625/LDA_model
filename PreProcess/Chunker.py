# -*- coding: utf-8 -*-
# 分块器评估测试

import nltk
from nltk.corpus import conll2000

# print(conll2000.chunked_sents('train.txt')[99])
# print(conll2000.chunked_sents('train.txt', chunk_types=['NP'])[99])

# test_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])

# tags = nltk.chunk.tree2conlltags(test_sents[0])
# print(tags)

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

func_term_grammer = r"""
    NP:{<VBZ><DT><NN>}
       {<JJ><NN><NN>}
       {<NN><BEZ><VBN>}
       {<VBG><DT><NN>}
       {<VBZ><NN><CC><NN>}
       {<VBG><JJ><NN|NNS>}
       {<JJ><NN>}
       {<NN><NN><RB>}
       {<RB><CC><RB>}
       {<VBG><NN><VBG>}
       {<VBZ><JJ><NN>}
       {<TO><VB><DT><NN>}
       {<VBZ><NN><VBG>}
       {<VBG><JJ><NN>}
       {<VBN><RB>}
       {<VBG><DT><NN><RB>}
       {<NN><RB>}
       {<NN><BER><VBN>}
       {<NN><BEZ><VBN>}
       {<JJR><JJ>}
    """

# tech_term_grammer = r"""
#     NP:{<NN>}
#        {<JJ><NN|NNS>}
#        {<VBG><NN>}
#        {<NN><NN>}
#        {<NN><NN><NN>}
#        {<JJ><NN><NN>}
#        {<JJ><JJ><NN>}
#        {<JJ><VBG><NN>}
#        {<JJR><NN><NN>}
#        {<RB><NN><NN>}
#        {<NN><VBG><NN>}
#        {<VBN><NN><NN>}
#        {<VBG><NN><NN>}
#        {<JJ><JJ><NN><NN>}
#        {<RB><JJ><NN><JJ><NN>}
#        {<JJ><NN><NN><NN>}
#        {<NN><JJ><VBG><NN>}
#     """

# 简单的评估和基准
cp = nltk.RegexpParser(r"""
    NP: {<DT|PRP\$>?<JJ>*<NN>}
        {<NNP|NN>+}
""")
test_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
print(cp.evaluate(test_sents))

# grammer = r"NP: {<[CDJNP].*>+}"
grammer = tech_np_grammer
cp = nltk.RegexpParser(grammer)
print(cp.evaluate(test_sents))