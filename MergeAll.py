#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/27 11:17
# @Author  : Daisy
# @Site    : Soochow
# @File    : MergeAll.py
# @Software: PyCharm Community Edition

import csv
from datetime import datetime
from TaxiCount import writeData

'''
合并交通数据与天气/空气数据
与的关系
'''


def merge():
    trafficDataPath = '公交出租总表.csv'
    AirAndPollutionDataPath = '清洗完毕天气与空气质量总表.csv'

    dataList = []
    trafficFile = open(trafficDataPath, 'r', encoding='utf-8')
    traffic_csv = csv.DictReader(trafficFile)
    for trafficDataRow in traffic_csv:
        # print(trafficDataRow)
        mergeDictTemp = {}
        trafficTimeTemp = datetime.strptime(trafficDataRow['时间'], '%Y-%m-%d %H:%M:%S')
        trafficArea = trafficDataRow['区域']
        mergeDictTemp['时间'] = trafficTimeTemp
        mergeDictTemp['区域'] = trafficArea
        mergeDictTemp['出租车数量'] = trafficDataRow['出租车数量']
        mergeDictTemp['公交车数量'] = trafficDataRow['公交车数量']
        with open(AirAndPollutionDataPath, 'r', encoding='utf-8') as AirFile:
            air_csv = csv.DictReader(AirFile)
            flag = 0
            for airDataRow in air_csv:
                # print(airDataRow)
                if airDataRow['时间'] != '时间':
                    airTimeTemp = datetime.strptime(airDataRow['时间'], '%Y-%m-%d %H:%M:%S')
                    airArea = airDataRow['区域']
                    # 相等 则存入数据
                    if trafficTimeTemp == airTimeTemp and trafficArea == airArea:
                        flag = 1
                        # print(airDataRow)
                        print(trafficDataRow)
                        mergeDictTemp['气温'] = airDataRow['气温']
                        mergeDictTemp['风向'] = airDataRow['风向']
                        mergeDictTemp['风速'] = airDataRow['风速']
                        mergeDictTemp['雨量'] = airDataRow['雨量']
                        mergeDictTemp['AQI'] = airDataRow['AQI']
                        mergeDictTemp['空气质量'] = airDataRow['空气质量']
                        print(mergeDictTemp)
                        dataList.append(mergeDictTemp)
                        # print('**')
                        break

            if flag == 0:
                # print(trafficDataRow)
                print()
        print('***')
    headers = ['时间', '区域', '出租车数量', '公交车数量', '气温', '风向', '风速', '雨量', 'AQI', '空气质量']
    fileName = '汇合的表格'
    writeData(dataList, headers, fileName)


if __name__ == '__main__':
    merge()
