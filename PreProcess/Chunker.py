# -*- coding: utf-8 -*-
# 分块器评估测试

import nltk
from nltk.corpus import conll2000

# print(conll2000.chunked_sents('train.txt')[99])
# print(conll2000.chunked_sents('train.txt', chunk_types=['NP'])[99])

# test_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])

# tags = nltk.chunk.tree2conlltags(test_sents[0])
# print(tags)

# 简单的评估和基准
cp = nltk.RegexpParser("")
test_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
print(cp.evaluate(test_sents))

grammer = r"NP: {<[CDJNP].*>+}"
cp = nltk.RegexpParser(grammer)
print(cp.evaluate(test_sents))