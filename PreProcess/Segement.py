# -*- coding: utf-8 -*-

import CommonAPI.Common as comm

class Segements(object):

    def segement(self, text, regEx):
        listOfTokens = comm.Segement(text).segement(regEx)
        return listOfTokens

    def find(self, text, regEx, tech):
        if tech == 1:
            res = comm.Segement(text).find_tech(regEx)
        elif tech == 0:
            res = comm.Segement(text).find_func(regEx)
        return res


if __name__ == '__main__':
    text_1 = u"   NOVELTY - The method involves confirming number L of a reversible sub-matrix " \
             u"which is needed to generate a parity check matrix according to preconcerted given encoding frequency of a communication system, " \
             u"where L is a natural number. The reversible sub-matrix is generated according to the code length of a low-density parity check " \
             u"(LDPC) code and the number L of the sub-matrix. " \
             u"The generating matrix of LDPC code is deduced according to the generated sub-matrix, " \
             u"and the LDPC encoding is executed about the information to be sent according to the generating matrix. " \
             u"The bit sequence to be sent is obtained.    " \
             u"USE - Method for encoding low-density parity check in a low-density parity check encoding device (claimed).    " \
             u"ADVANTAGE - The method provides low-density parity check encoding with high speed, " \
             u"high efficiency and low encoding complex degree, and the performance of low-density parity check code is assured.    " \
             u"DETAILED DESCRIPTION - INDEPENDENT CLAIMS are also included for the following:    " \
             u"(1) a generating method of a low-density parity check matrix.    " \
             u"DESCRIPTION OF DRAWING(S) - The drawing shows a flow diagram of a low-density parity check encoding method. " \
             u"`(Drawing includes non-English language text)` "
    seg_re = r'USE - '
    find_re = r'ADVANTAGE - (.*?)\s\s\s[A-Z]*\s[A-Z]*\s-\s(.*)'
    seg_test = Segements()
    listOfseg = seg_test.segement(text_1,seg_re)
    # print(listOfseg[1])
    res = seg_test.find(listOfseg[1], find_re, 0)
    print(res)