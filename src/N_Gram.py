#-*- coding:utf-8 -*-
#!/usr/bin/env python

import re
import time
import pickle
import os, sys, copy
import numpy as np

class one_Gram(object):
    def __init__(self, file = None):
        self.dict_fd = open('data/dict.txt', 'r', encoding = 'utf-8')
        self.dict = {}
        self.length = 0
        for line in self.dict_fd:
            Line = line.split()
            word, frequency = Line[0], Line[1]
            self.dict[word] = int(frequency)
            self.length += int(frequency)

    def only_chinese(self, string):
        if len(string) == 0:
            return False
        for character in string:
            if character >= u"\u4e00" and character <= u"\u9fa6":
                continue
            else:
                return False
        return True

    def _all_situation(self, context, start = 0, result = []):
        length = len(context)
        if start == length:
            self.all_situation.append(copy.deepcopy(result))
        else:
            flag = False
            if start + 6 <= length and context[start : start + 6] in self.dict:
                flag = True
                result.append(context[start : start + 6])
                self._all_situation(context, start + 6, result)
                result.pop()
                return

            if start + 5 <= length and context[start : start + 5] in self.dict:
                flag = True
                result.append(context[start : start + 5])
                self._all_situation(context, start + 5, result)
                result.pop()
                return

            if start + 4 <= length and context[start : start + 4] in self.dict:
                flag = True
                result.append(context[start : start + 4])
                self._all_situation(context, start + 4, result)
                result.pop()
                return
                
            if start + 3 <= length and context[start : start + 3] in self.dict:
                flag = True
                result.append(context[start : start + 3])
                self._all_situation(context, start + 3, result)
                result.pop()

            if start + 2 <= length and context[start : start + 2] in self.dict:
                flag = True
                result.append(context[start : start + 2])
                self._all_situation(context, start + 2, result)
                result.pop()

            if context[start] in self.dict:
                flag = True
                result.append(context[start : start + 1])
                self._all_situation(context, start + 1, result)
                result.pop()

            if flag == False:
                result.append(context[start : start + 1])
                self._all_situation(context, start + 1, result)
                result.pop()

    def _get_possibility(self, result):
        possibility = 1
        for word in result:
            if word in self.dict:
                possibility = possibility * self.dict[word]
        return possibility / pow(self.length, len(result))

    def _cut(self, context):
        self._all_situation(context); Max = 0
        for result in self.all_situation:
            p = self._get_possibility(result)
            if p > Max:
                Max = p
                Max_result = result
        self.all_situation.clear()
        return Max_result

    def _pretreatment (self, context):
        tmp = []
        for line in context:
            if len(line) != 0:
                tmp.append(line)
        return tmp

    def cut(self, context):
        self.result = []
        self.all_situation = []
        context = re.split('：|-|/|【|？|】|\?|。|，|\.|、|《|》| |（|）|”|“|；|\n', context)
        context = self._pretreatment(context);
        for line in context:
            self.result = self.result + self._cut(line)
        return self.result

class BiGram(object):
    def __init__ (self):
        data = pickle.load(open("../data/data.pickle", 'rb'))
       
        self.word_count = data[0] # 单独word的词频
        self.word_next_word_count = data[1] # 每个word的后继词以及出现概率
        
        # 统计文档当中的次数
        self.length = 0
        for word in self.word_count:
            self.length = self.length + self.word_count[word]
        self.length += len(self.word_count) #加1平滑

        # 用来统计每个词后继词的总个数,后面可以用来计算条件概率
        self.word_next_word_num = {}
        for word in self.word_next_word_count:
            self.word_next_word_num[word] = 0
            for word_in in self.word_next_word_count[word]:
                self.word_next_word_num[word] += self.word_next_word_count[word][word_in]

    def _all_situation(self, context, start = 0, result = []):
        length = len(context)
        if start == length:
            self.all_situation.append(copy.deepcopy(result))
        else:
            flag = False
            if start + 6 <= length and context[start : start + 6] in self.word_count:
                flag = True
                result.append(context[start : start + 6])
                self._all_situation(context, start + 6, result)
                result.pop()
                return

            if start + 5 <= length and context[start : start + 5] in self.word_count:
                flag = True
                result.append(context[start : start + 5])
                self._all_situation(context, start + 5, result)
                result.pop()
                return

            if start + 4 <= length and context[start : start + 4] in self.word_count:
                flag = True
                result.append(context[start : start + 4])
                self._all_situation(context, start + 4, result)
                result.pop()
                
            if start + 3 <= length and context[start : start + 3] in self.word_count:
                flag = True
                result.append(context[start : start + 3])
                self._all_situation(context, start + 3, result)
                result.pop()

            if start + 2 <= length and context[start : start + 2] in self.word_count:
                flag = True
                result.append(context[start : start + 2])
                self._all_situation(context, start + 2, result)
                result.pop()

            if context[start] in self.word_count:
                flag = True
                result.append(context[start : start + 1])
                self._all_situation(context, start + 1, result)
                result.pop()

            if flag == False:
                result.append(context[start : start + 1])
                self._all_situation(context, start + 1, result)
                result.pop()

    def _pretreatment (self, context):
        tmp = []
        for line in context:
            if len(line) != 0:
                tmp.append(line)
        return tmp

    def _get_possibility(self, result):
        p = 1.0
        length = len(result)
        for index in range(length):
            if index == 0:
                if result[index] in self.word_count:
                    p = p * ((self.word_count[result[index]] + 1) / self.length)
                else:
                    p = p * (1 / self.length)
            else:
                if result[index - 1] in self.word_next_word_count and \
                   result[index] in self.word_next_word_count[result[index - 1]]:
                    p = p * ((self.word_next_word_count[result[index - 1]][result[index]] + 1) /
                             self.word_next_word_num[result[index - 1]])
                elif result[index - 1] in self.word_next_word_count:
                    p = p * (1 / self.word_next_word_num[result[index - 1]])
                else:
                    p = p * pow(0.1, 10)
        return p

    def _cut(self, context):
        self._all_situation(context); Max = 0
        for result in self.all_situation:
            p = self._get_possibility(result)
            if p > Max:
                Max = p
                Max_result = result
        self.all_situation.clear()
        return Max_result

    def cut(self, context):
        self.result = []
        self.all_situation = []
        context = re.split('：|-|/|【|？|】|\?|。|，|\.|、|《|》| |（|）|”|“|；|\n', context)
        context = self._pretreatment(context);
        for line in context:
            self.result = self.result + self._cut(line)
        return self.result

if __name__ == '__main__':
    tang = BiGram()
    for number in range(1000):
        print (number)
        string = "本报北京１２月３１日讯新华社记者陈雁、\
                  本报记者何加正报道：在度过了非凡而辉煌的１９９７年，\
                  迈向充满希望的１９９８年之际，’９８北京新年音乐会今晚在人民大会堂举行。\
                  党和国家领导人江泽民、李鹏、乔石、朱镕基、李瑞环、刘华清、尉健行、李岚清与万名首都各界群众和劳动模范代表一起，\
                  在激昂奋进的音乐声中辞旧迎新。"
        res = tang.cut(string)
    print (res)
