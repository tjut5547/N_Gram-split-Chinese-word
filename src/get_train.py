#-*- coding:utf-8 -*-
#!/usr/bin/env python

import pickle

class App(object):
    def __init__(self, file):
        fd = open(file, 'r', encoding = 'utf-8')

        self.word_count, self.word_word_dict = {}, {}
        for line in fd:
            Line, length = line.split(), len(line.split())
            for index in range(length):
                if Line[index] in self.word_count:
                    self.word_count[Line[index]] += 1
                else:
                    self.word_count[Line[index]] = 1

                if index == length - 1: break
                if Line[index] in self.word_word_dict:
                    if Line[index + 1] in self.word_word_dict[Line[index]]:
                        self.word_word_dict[Line[index]][Line[index + 1]] += 1
                    else:
                        self.word_word_dict[Line[index]][Line[index + 1]] = 1
                else :
                    self.word_word_dict[Line[index]] = {Line[index + 1] : 1}

        print ("LEN :", len(self.word_count))
        print ("LEN :", len(self.word_word_dict))
        pickle.dump((self.word_count, self.word_word_dict), open("../data/data.pickle", 'wb'))

        # number = 1
        # for word, frequency in self.word_count.items():
        #     print (word, frequency, end = '    ')
        #     if number % 30 == 0:
        #         print ()


if __name__ == '__main__':
    app = App('../data/train_utf_8.txt')