#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/26 20:12
# @Author  : Daisy
# @Site    : 
# @File    : CleanTaxiCount.py
# @Software: PyCharm Community Edition

'''
一只向List中添加数据
后一项与前一项相同,则相加,只添加一项
'''

import csv


def writeData(dataList, headers, filename):
    fileName = filename + '.csv'
    # print(dataList)
    with open(fileName, 'a+', encoding='utf-8', newline='') as f:  # newline去行之间的空行
        w_csv = csv.DictWriter(f, headers)
        w_csv.writeheader()
        w_csv.writerows(dataList)
    f.close()


def cleanTable():
    dataPath = 'all-groups.csv'
    print(dataPath)
    cleanedList = []
    with open(dataPath, 'r', encoding="utf-8") as f:
        data_csv = csv.DictReader(f)
        temp = list(data_csv)
        for csvNum in range(len(temp)):
            try:
                if temp[csvNum]['\ufeff时间'] == temp[csvNum + 1]['\ufeff时间'] and temp[csvNum]['区域'] == temp[csvNum + 1]['区域']:
                    # 若相等则将数值加到后一项上
                    preCount = int(temp[csvNum]['数量'])
                    afterCount = int(temp[csvNum + 1]['数量'])
                    temp[csvNum + 1]['数量'] = str(preCount + afterCount)
                    temp[csvNum]['数量'] = temp[csvNum + 1]['数量']
                    # print(temp[csvNum])
                else:
                    taxiDict = {}
                    taxiDict['时间'] = temp[csvNum]['\ufeff时间']
                    taxiDict['区域'] = temp[csvNum]['区域']
                    taxiDict['数量'] = temp[csvNum]['数量']
                    cleanedList.append(taxiDict)
                    print(temp[csvNum])
            except IndexError:
                print(temp[csvNum])
                continue

    dataHeaders = ['时间', '区域', '数量']
    fileName = '出租车数量总表'
    writeData(cleanedList, dataHeaders, fileName)

if __name__ == '__main__':
    cleanTable()
