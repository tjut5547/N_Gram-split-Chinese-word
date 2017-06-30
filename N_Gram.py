#-*- coding:utf-8 -*-
#!/usr/bin/env python

import re
import time
import pickle
import os, sys, copy
import numpy as np

class N_Gram(object):
    def __init__(self, file = None):
        self.dict_fd = open('dict.txt', 'r', encoding = 'utf-8')
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

if __name__ == '__main__':
    tang = N_Gram()
    for number in range(3000):
        print (number)
        string = "法制晚报讯（记者 唐宁 实习记者 金春妮）昨天凌晨，\
                        家住北京朝阳管庄新天地小区的王女士在网上爆料称，\
                        因快递丢失她投诉了申通快递一名快递员，结果被该快递员恶意报复，\
                        强行入室将自己打成重伤，并表示在6月24日事发后，申通快递公司一直对此事没有回应。\
                        昨天下午，北京申通快递官方微博表示，公司已经获悉此事，向客户致歉，尊重事实真相，\
                        不会逃避责任，更不会“容忍”任何侵害客户行为的存在，会就此事给公众一个交代。\
                        昨天晚间，北京警方发布消息称，涉事快递员已经被行政拘留."
        res = tang.cut("汤州林来自北京邮电大学")
    print (res)
