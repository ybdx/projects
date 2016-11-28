# -*- coding: utf-8 -*-
import re
import sys
import os
import random
reload(sys)
sys.setdefaultencoding('utf-8')

'''
功能：将大文件切分成各个小文件
'''

'''
test_sent = "青岛四方城市发展有限公司"
words = jieba.cut(test_sent)
for w in words:
    print w
result = pseg.cut(test_sent)
for w in result:
    if len(w.word) == 1 or w.flag == "ns" or w.word =="有限公司" or w.word == "公司" or w.word == "有限责任":
        continue
    print w.word, "/", w.flag,

'''

def file_split(inputPath, outputPathDir):
    count = 0
    companyNameSet = set()
    keySet = set()
    fileinput = open(inputPath, "r")
    if os.path.isfile(inputPath) is False:
        print inputPath + " is not a valid path"
        os._exit(1)
    if os.path.exists(outputPathDir) is False:
        os.mkdir(outputPathDir)
    elif os.path.isdir(outputPathDir) is False:
        print outputPathDir + " is not a directory"
        os._exit(1)
    print inputPath, outputPathDir

    while True:
        line = fileinput.readline()
        if line:
            companyNameSet.add(line)
        else:
            break
    avg = len(companyNameSet) / 4
    for i in companyNameSet:
        keySet.add(i)
        if len(keySet) == avg:
            count += 1
            fo = open(outputPathDir + "/%d.txt" % count, "w")
            for key in keySet:
                fo.write(key)
            fo.close()
            keySet.clear()
    
    fo = open(outputPathDir + "/%d.txt" % count, "a")

    for key in keySet:
        fo.write(key)
    fo.close()
    keySet.clear()
    companyNameSet.clear()
    fileinput.close()

if __name__ == "__main__":
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]
    file_split(inputPath, outputPath)





