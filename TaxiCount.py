#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/19 16:38
# @Author  : Daisy
# @Site    : 
# @File    : TaxiCount.py
# @Software: PyCharm Community Edition

'''
读取出租车数据
统计这个时间内 这个时间段的出租车数量
'''

import xlrd, xlwt, csv
from datetime import datetime


def writeData(dataList, headers, filename):
    fileName = filename + '.csv'
    # print(dataList)
    with open(fileName, 'a+', encoding='utf-8', newline='') as f:  # newline去行之间的空行
        w_csv = csv.DictWriter(f, headers)
        w_csv.writeheader()
        w_csv.writerows(dataList)
    f.close()


def standardTime(test):
    '''
    把时间处理成标准时间(每三小时一次的抽样),部分时间会无法处理,返回None
    :param test: 一般时间,如2015-04-02 22:41:12(注意,这个时间在该函数中是无法标准化的
    :return: 标准化的时间,如2015-04-03 00:00:00
    '''
    # print('standardTime:::', test)
    if test.day == 1:
        delta1 = datetime(year=test.year, month=test.month - 1, day=31, hour=22, minute=30)
    else:
        delta1 = datetime(year=test.year, month=test.month, day=test.day - 1, hour=22, minute=30)
    # print(delta1)
    delta2 = datetime(year=test.year, month=test.month, day=test.day, hour=1, minute=30)
    delta3 = datetime(year=test.year, month=test.month, day=test.day, hour=4, minute=30)
    delta4 = datetime(year=test.year, month=test.month, day=test.day, hour=7, minute=30)
    delta5 = datetime(year=test.year, month=test.month, day=test.day, hour=10, minute=30)
    delta6 = datetime(year=test.year, month=test.month, day=test.day, hour=13, minute=30)
    delta7 = datetime(year=test.year, month=test.month, day=test.day, hour=16, minute=30)
    delta8 = datetime(year=test.year, month=test.month, day=test.day, hour=19, minute=30)
    delta9 = datetime(year=test.year, month=test.month, day=test.day, hour=22, minute=30)
    deltaList = [delta1, delta2, delta3, delta4, delta5, delta6, delta7, delta8, delta9]
    delta = delta2 - datetime(year=test.year, month=test.month, day=test.day)
    for deltaNum in range(len(deltaList)):
        # print(deltaNum)
        try:
            preDelta = deltaList[deltaNum]
            afterDelta = deltaList[deltaNum + 1]
        except IndexError:
            afterDelta = deltaList[0]

        if preDelta < test < afterDelta:
            resultTime = preDelta + delta
            # 可以在这直接return
            # print('&&&&&&')
            # print(resultTime)
            return resultTime


def getTaxiTimeAndArea(a=1):
    dataPath = '出租车数据/出租车整合第' + str(a) + '部分数据.csv'
    print('正在打开...', dataPath)
    i = 1

    taxiCountList = [{'时间': 0, '区域': 0, '数量': 0}]

    with open(dataPath, 'r', encoding='utf-8') as f:
        data_csv = csv.DictReader(f)
        for row in data_csv:
            if row['接收时间'] != '接收时间':
                i += 1
                taxiDict = {}
                # print(row, '**', i)
                taxiRealTime = datetime.strptime(row['接收时间'], '%Y-%m-%d %H:%M:%S')  # 真实时间
                taxiStandardTime = standardTime(taxiRealTime)  # 转换为标准时间,仍是datetime格式
                areaString = row['所在区域']
                taxiDict['时间'] = taxiStandardTime
                taxiDict['区域'] = areaString
                if taxiDict['时间'] is None:  # 无法正常处理的时间
                    if taxiRealTime.day == 30 and (taxiRealTime.month == 4 or 6 or 9 or 11):
                        taxiDict['时间'] = datetime(year=taxiRealTime.year, month=taxiRealTime.month + 1, day=1)
                    else:
                        taxiDict['时间'] = datetime(year=taxiRealTime.year, month=taxiRealTime.month,
                                                  day=taxiRealTime.day + 1)

                flag = 0  # 是否找到
                for taxiCount in taxiCountList:
                    if taxiCount['时间'] == taxiDict['时间'] and taxiCount['区域'] == taxiDict['区域']:
                        # print('区域与时间相等')
                        # print('本次循环的出租车信息(taxiDict):', taxiDict)
                        # print('List中对应的出租车信息(taxiCount):', taxiCount)
                        taxiCountTemp = taxiCount['数量']
                        taxiCount['数量'] = taxiCountTemp + 1
                        flag = 1

                        break
                if flag == 0:
                    taxiDict['数量'] = 1
                    taxiCountList.append(taxiDict)
            else:
                print('Error Row', row)

    f.close()
    dataHeaders = ['时间', '区域', '数量']
    fileName = '出租车数量第' + str(a) + '部分数据'
    writeData(taxiCountList, dataHeaders, fileName)


if __name__ == '__main__':
    # standardTime()
    # Test()
    # for num in range(2, 31):
    #     # print(num)
    #     getTaxiTimeAndArea(num)
    getTaxiTimeAndArea(30)
