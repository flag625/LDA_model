# -*- coding: utf-8 -*-
# 分块器评估测试

import nltk
from nltk.corpus import conll2000

# print(conll2000.chunked_sents('train.txt')[99])
# print(conll2000.chunked_sents('train.txt', chunk_types=['NP'])[99])

# test_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])

# tags = nltk.chunk.tree2conlltags(test_sents[0])
# print(tags)

tech_np_grammer1 = r"""
    NP:{<DT|CD|PRP\$>?<JJ|JJR|JJS>*<VBN>*<NN|NNS|NNP|NNPS>+}
       {<NN|NNS|NNP|NNPS>*<VBG>+<NN|NNS|NNP|NNPS>+}
       {<NN|NNS|NNP|NNPS>*<JJ|JJR|JJS>*<VBN>+<NN|NNS|NNP|NNPS>+}
       {<RB|RBR|RBS>+<JJ|JJR|JJS>*<NN|NNS|NNP|NNPS>*<JJ|JJR|JJS>*<NN|NNS|NNP|NNPS>+}
    """

tech_np_grammer2 = r"""
    NP:{<DT|CD|PRP\$>?<NN|NNS|NNP|NNPS>+<POS>?<NN|NNS|NNP|NNPS>*}
       {<NN|NNS|NNP|NNPS>*<VBG><NN|NNS|NNP|NNPS>+}
       {<NN|NNS|NNP|NNPS>+<JJ|JJR|JJS>+<VBG><NN|NNS|NNP|NNPS>+}
       {<VBN><NN|NNS|NNP|NNPS>+}
       {<JJ|JJR|JJS>+<VBG>?<NN|NNS|NNP|NNPS>+}
       {<JJR|JJS>?<RB|RBR|RBS><NN|NNS|NNP|NNPS>+}
       {<RB|RBR|RBS><JJ|JJR|JJS>+<NN|NNS|NNP|NNPS>+<JJ|JJR|JJS>+<NN|NNS|NNP|NNPS>+}
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

# func_np_grammer2 = r"""
#             NP:{<VBZ|VBG><DT|CD>?<JJ|JJR|JJS>*<NN|NNS>}
#                {<VBZ|VBG><DT|CD>?<JJ|JJR|JJS>*<NN|NNS>+<CC><NN|NNS>}
#                {<JJ|JJR|JJS>+<NN|NNS>+}
#                {<JJ|JJR|JJS>*<CC>?<JJ|JJR|JJS>+}
#                {<VBZ|VBG><NN|NNS><VBG>}
#                {<VBN><JJR|JJS>?<RB|RBR|RBS>}
#                {<VBG><DT|CD>?<NN|NNS><JJR|JJS>?<RB|RBR|RBS>}
#                {<RB|RBR|RBS>*<CC>?<JJR|JJS>?<RB|RBR|RBS>+}
#                {<TO>?<VB><DT|CD>?<NN|NNS>}
#                {<NN|NNS>+<BEZ|BER><VBN>}
#                {<NN|NNS>*<JJR|JJS>?<RB|RBR|RBS>}
#                {<NN|NNS>+<IN><NN|NNS>+}
#             """

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
# cp = nltk.RegexpParser(r"""
#     NP: {<DT|PRP\$>?<JJ>*<NN>}
#         {<NNP|NN>+}
# """)
# test_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
# print(cp.evaluate(test_sents))

# grammer = r"NP: {<[CDJNP].*>+}"
# grammer = tech_np_grammer
# cp = nltk.RegexpParser(grammer)
# print(cp.evaluate(test_sents))

doc2 = "so that network load is equilibrated, and improves efficiency of the selecting node and stability of the network."
sent = nltk.word_tokenize(doc2)
sent = nltk.pos_tag(sent)
grammer = r"NP: {<NN|NNS>+<IN><CD|CC>?<NN|NNS>+}"
cp = nltk.RegexpParser(grammer)
sentTree = cp.parse(sent)
print(sentTree)
