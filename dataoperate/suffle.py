#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import random

def shuffle(lol, seed):
    for l in lol:
        random.seed(seed)
        random.shuffle(l)
    train_num = total * ratio[0]
    val_num = total * ratio[1]
    test_num = total * ratio[2]
    i = 0
    train = codecs.open(filename + ".train", "w", encoding="utf-8")
    val = codecs.open(filename + ".val", "w", encoding="utf-8")
    test = codecs.open(filename + ".test", "w", encoding="utf-8")

    samples=[]
    flag=0
    with codecs.open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            samples.append(line)
            flag = flag+1

    shuffle([samples], 3)

    for ch in samples:
        i += 1
        if i < train_num:
            cur_file = train
        elif i - train_num < val_num:
            cur_file = val
        elif i - train_num - val_num < test_num:
            cur_file = test

        cur_file.write(ch + '\n')

def char_nlu_split_train_val_test(filename, total, ratio=[1,0,0]):
    train_num = 120000 #total * ratio[0]
    val_num = 9600 #total * ratio[1]
    test_num = total - train_num - val_num #total * ratio[2]
    i = 0
    train = codecs.open(filename + ".train", "w", encoding="utf-8")
    val = codecs.open(filename + ".val", "w", encoding="utf-8")
    test = codecs.open(filename + ".test", "w", encoding="utf-8")

    samples=[]
    flag=0
    with codecs.open(filename, "r", encoding="utf-8") as f:
        for line in f:
            try:
                while line is None:
                    continue
                line = line.rstrip()
                lines = line.split('\t')
                # words = ' '.join(lines[0])
                samples.append(lines[0].strip() + '\t' + lines[1].strip())
                flag = flag+1
            except:
                you = 0

    shuffle([samples], 3)

    for ch in samples:
        i += 1
        if i < train_num:
            cur_file = train
        elif i - train_num < val_num:
            cur_file = val
        elif i - train_num - val_num < test_num:
            cur_file = test

        cur_file.write(ch + '\n')

if __name__ == "__main__":
    #将其混淆成120000:9600的训练、验算数据
    char_nlu_split_train_val_test("D:/DataSet/MachaneLearing/Classification/ner_5/train/ALL_10_5_pinyin.txt", 132296)