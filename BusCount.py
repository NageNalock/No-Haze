#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/26 20:48
# @Author  : Daisy
# @Site    : 
# @File    : BusCount.py
# @Software: PyCharm Community Edition

import csv
from datetime import datetime
from TaxiCount import writeData

'''
统计公交车在某段时间某个区域内的数量
'''


def testTable(area):
    '''
    用来看表头的,坑爹的崔力辉
    :param area: 区域
    :return: 没啥用,只是让函数返回一行罢了
    '''
    dataPath = '公交数据/' + area + '.csv'
    print('正在打开...', dataPath)
    with open(dataPath, 'r', encoding='utf-8') as f:
        data_csv = csv.DictReader(f)
        for row in data_csv:
            print(row)
            return 0


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


def getBusTimeAndCount(area, timeHeader):
    dataPath = '公交数据/' + area + '.csv'
    print('正在打开...', dataPath)
    busCountList = [{'时间': 0, '区域': 0, '数量': 0}]
    with open(dataPath, 'r', encoding='utf-8') as f:
        data_csv = csv.DictReader(f)
        for row in data_csv:
            # print(row['2015-01-01 07:00:53'])
            busRealTime = datetime.strptime(row[timeHeader], '%Y-%m-%d %H:%M:%S')  # 真实时间
            if busRealTime.month == 4:  # 只计算四月的
                busDict = {}
                busStandardTime = standardTime(busRealTime)
                busDict['区域'] = area
                busDict['时间'] = busStandardTime
                if busDict['时间'] is None:
                    if busRealTime.day == 30 and (busRealTime.month == 4 or 6 or 9 or 11):
                        busDict['时间'] = datetime(year=busRealTime.year, month=busRealTime.month + 1, day=1)
                    else:
                        busDict['时间'] = datetime(year=busRealTime.year, month=busRealTime.month,
                                                 day=busRealTime.day + 1)
                # print(busDict)

                flag = 0  # 是否找到
                for busCount in busCountList:
                    if busCount['时间'] == busDict['时间'] and busCount['区域'] == busDict['区域']:
                        print('区域与时间相等')
                        print('本次循环的出租车信息(taxiDict):', busDict)
                        print('List中对应的出租车信息(taxiCount):', busCount)
                        busCountTemp = busCount['数量']
                        busCount['数量'] = busCountTemp + 1
                        flag = 1

                        break
                if flag == 0:
                    busDict['数量'] = 1
                    busCountList.append(busDict)

    f.close()
    dataHeaders = ['时间', '区域', '数量']
    fileName = '公交车数量' + area + '区域数据'
    writeData(busCountList, dataHeaders, fileName)



if __name__ == '__main__':
    testTable('J')
    getBusTimeAndCount('J', '2015-01-01 09:14:38')
