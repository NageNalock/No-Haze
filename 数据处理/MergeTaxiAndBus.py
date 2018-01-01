#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/26 21:57
# @Author  : Daisy
# @Site    : 
# @File    : MergeTaxiAndBus.py
# @Software: PyCharm Community Edition

'''
融合公交和出租数据
取并的关系
出租数据比较全,所以以出租为主
空掉的公交数据补0
'''

import csv
from datetime import datetime
from TaxiCount import writeData

# def isBusComplete(area):
#     busDataPath = '公交车数量' + area + '区域数据.csv'
#     with open(busDataPath, 'r', encoding='utf-8') as f:
#         data_csv = csv.DictReader(f)
#         for

def mergeData():
    taxiDataPath = '出租车数量总表.csv'
    taxiFile = open(taxiDataPath, 'r', encoding='utf-8')

    mergedList = []
    taxi_csv = csv.DictReader(taxiFile)
    for taxiRow in taxi_csv:
        # 正常存入时间 区域 出租车数量
        mergedDictTemp = {}
        areaTemp = taxiRow['区域']
        # print(taxiRow['时间'] + ':00')

        timeTemp = datetime.strptime(taxiRow['时间']+':00', '%Y/%m/%d %H:%M:%S')  # 转化为datatime格式
        mergedDictTemp['时间'] = timeTemp
        mergedDictTemp['区域'] = areaTemp
        mergedDictTemp['出租车数量'] = taxiRow['数量']
        # 根据区域检查公交车数量是否齐全
        busDataPath = '公交车数量数据/公交车数量' + areaTemp + '区域数据.csv'
        # print('此时的公交车区域为:::', areaTemp)
        if areaTemp != 'B':
            with open(busDataPath, 'r', encoding='utf-8') as busFile:
                bus_csv = csv.DictReader(busFile)
                busFlag = 0
                for busRow in bus_csv:
                    # 时间转化为datatime格式
                    if busRow['时间'] != '0' and busRow['时间'] != '时间':
                        busTime = datetime.strptime(busRow['时间'], '%Y-%m-%d %H:%M:%S')
                        if timeTemp == busTime:
                            mergedDictTemp['公交车数量'] = busRow['数量']
                            busFlag = 1
                if busFlag == 0:
                    print('公交车数据不全,现在的数据状态为:::', mergedDictTemp)
                    mergedDictTemp['公交车数量'] = 0
                    print('之后的状态', mergedDictTemp)
        mergedList.append(mergedDictTemp)
    dataHeaders = ['时间', '区域', '出租车数量', '公交车数量']
    fileName = '公交与出租'
    writeData(mergedList, dataHeaders, fileName)

def deleteDateOfB():
    '''
    除掉表中的B区数据
    :return:
    '''
    cleanedList = []
    busDataPath = '公交与出租.csv'
    with open(busDataPath, 'r', encoding='utf-8') as f:
        data_csv = csv.DictReader(f)
        for row in data_csv:
            if row['区域'] != 'B':
                cleanedList.append(row)
    dataHeaders = ['时间', '区域', '出租车数量', '公交车数量']
    fileName = '公交出租总表'
    writeData(cleanedList, dataHeaders, fileName)

if __name__ == '__main__':
    # mergeData()
    deleteDateOfB()