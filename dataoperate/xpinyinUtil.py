# -*- coding: UTF-8 -*-
#!/usr/bin/python
import xpinyin

p = xpinyin.Pinyin()
# default splitter is `-`
shang_hai = p.get_pinyin(u"上海")
# 'shang-hai'
# show tone marks
shàng_hǎi = p.get_pinyin(u"上海", show_tone_marks=True)
# 'shàng-hǎi'
# remove splitter
shanghai = p.get_pinyin(u"上海", '')
# 'shanghai'
# set splitter as whitespace
shang0hai = p.get_pinyin('上海自来水来着海上', ' ')
# 'shang hai'
S = p.get_initial(u"上")
# 'S'
S_H = p.get_initials(u"上海")
# 'S-H'
SH = p.get_initials(u"上海", u'')
# 'SH'
S0H = p.get_initials(u"上海", u' ')
# 'S H'
print(shang_hai)
print(shàng_hǎi)
print(shanghai)
print(shang0hai)
print(S)
print(S_H)
print(SH)
print(S0H)


class xpinyinUtil(object):
    p = xpinyin.Pinyin()
    def pingyinFile(filename, filewrite):
        file = open(filename, 'r', encoding='utf-8')
        # lineone = file.readline()
        sentences = []
        length = {}
        while True:
            line = file.readline()
            if not line:
                break
            sentence = line.strip()
            text = sentence.split('\t')
            try:
                shang0hai = p.get_pinyin(text[0].strip(), ' ')
                lenpinyin = len(shang0hai)
                if lenpinyin in length.keys():
                    length[lenpinyin] = length[lenpinyin] + 1
                elif lenpinyin not in length.keys():
                    length[lenpinyin] = 1
                sentences.append(text[1] + '\t' + shang0hai.lower().strip() + '\n')
            except:
                print('错误： ', line)
        print(length)
        filewrite = open(filewrite, 'w', encoding='utf-8')
        filewrite.writelines(sentences)
test_file = 'D:/DataSet/MachaneLearing/Classification/ner_5/train/ALL_10_5.txt'
pinyinfile = 'ALL_10_5_pinyin.txt'
xpinyinUtil.pingyinFile(test_file, pinyinfile)

# {2: 25, 3: 52, 4: 43, 5: 246, 6: 604, 7: 618, 8: 670, 9: 930, 10: 1018, 11: 1425, 12: 1634, 13: 2257, 14: 2650, 15: 3302, 16: 3873, 17: 3787, 18: 3713, 19: 4150, 20: 4612, 21: 5296, 22: 5127, 23: 4906, 24: 4952, 25: 5148, 26: 5664, 27: 6041, 28: 4595, 29: 4327, 30: 4054, 31: 3660, 32: 3521, 33: 3443, 34: 2967, 35: 2698, 36: 2675, 37: 2422, 38: 2184, 39: 2016, 40: 1870, 41: 1715, 42: 1466, 43: 1347, 44: 1274, 45: 1124, 46: 1131, 47: 935, 48: 864, 49: 795, 50: 725, 51: 697, 52: 594, 53: 611, 54: 521, 55: 452, 56: 422, 57: 437, 58: 361, 59: 374, 60: 295, 61: 321, 62: 246, 63: 244, 64: 202, 65: 204, 66: 167, 67: 171, 68: 130, 69: 132, 70: 128, 71: 108, 72: 93, 73: 88, 74: 81, 75: 86, 76: 66, 77: 60, 78: 42, 79: 40, 80: 43, 81: 35, 82: 32, 83: 24, 84: 27, 85: 27, 86: 14, 87: 24, 88: 12, 89: 16, 90: 19, 91: 8, 92: 19, 93: 7, 94: 9, 95: 13, 96: 2, 97: 1, 98: 5, 99: 5, 100: 6, 101: 1, 102: 1, 103: 1, 104: 2, 105: 2, 106: 1, 107: 4, 108: 1, 109: 2, 110: 1, 111: 1, 115: 1, 118: 1, 119: 1, 120: 2, 124: 1, 127: 1}