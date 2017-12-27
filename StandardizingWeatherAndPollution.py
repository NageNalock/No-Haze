#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/26 22:56
# @Author  : Daisy
# @Site    : 
# @File    : StandardizingWeatherAndPollution.py
# @Software: PyCharm Community Edition
'''
将天气/污染表标准化
坑爹的崔力辉
'''

import csv
from datetime import datetime
from TaxiCount import writeData


def standardizing():
    datapath = 'MergedDataSecond.csv'
    resultList = []
    with open(datapath, 'r', encoding='utf-8') as f:
        data_csv = csv.DictReader(f)
        for row in data_csv:
            dictTemp = {}

            timeUnStandard = (row['\ufeff年月日时分'])
            dataString = timeUnStandard[0:10]
            hourString = timeUnStandard[11:13]
            minuteString = timeUnStandard[13:]
            timeStandard = dataString + ' ' + hourString + ':' + minuteString + ':' + '00'
            dictTemp['时间'] = timeStandard
            timeDatetime = datetime.strptime(timeStandard, '%Y-%m-%d %H:%M:%S')

            area = row['area'].upper()
            if area != 'Y' and timeDatetime.month == 4:
                dictTemp['区域'] = area
                # dictTemp[]
                dictTemp['气温'] = row['气温']
                dictTemp['风向'] = row['风向']
                dictTemp['风速'] = row['风速']
                dictTemp['雨量'] = row['雨量']
                dictTemp['AQI'] = row['AQI']
                dictTemp['空气质量'] = row['AIRQUALITY']
                resultList.append(dictTemp)
                print(dictTemp)
                # print(dictTemp)
    hearders = ['时间', '区域', '气温', '风向', '风速', '雨量', 'AQI', '空气质量']
    filename = '清洗完毕天气与空气质量总表'
    writeData(resultList, headers=hearders, filename=filename)


if __name__ == '__main__':
    standardizing()
