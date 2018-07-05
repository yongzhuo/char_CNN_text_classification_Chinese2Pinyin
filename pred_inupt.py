# -*- coding: UTF-8 -*-
#!/usr/bin/python
import xpinyin
import time
from pred_model import char_CNN

pin = xpinyin.Pinyin()


#在控制台输入用
while True:
    print("input_Chinese:")
    text = input()
    timestr = time.time()
    textpinyin = pin.get_pinyin(text, ' ')
    char_CNN.rec(text, textpinyin)
    timeend = time.time()
    print('耗时： ', timeend - timestr)



#做成server服务用
# class intent(object):
#     def __init__(self, sentence):
#         # self.sentence = sentence
#         self.result = intent.intnetget(self, sentence)
#
#
#     def intnetget(self, sentence):
#         # print("input_Chinese:")
#         # text = input()
#         timestr = time.time()
#         textpinyin = pin.get_pinyin(sentence, ' ')
#         domain = char_CNN.rec(sentence, textpinyin)
#         timeend = time.time()
#         print('耗时： ', timeend - timestr)
#         return  domain