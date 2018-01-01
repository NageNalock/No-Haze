#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/1 22:08
# @Author  : Daisy
# @Site    : Soochow
# @File    : StratifiedShuffleSplit.py
# @Software: PyCharm Community Edition

import csv
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

'''
StratifiedShuffleSplit和ShuffleSplit的一个变体，返回分层划分，也就是在创建划分的时候要保证每一个划分中类的样本比例与整体数据集中的原始比例保持一致
1. 归一化 *
2. 增加参数 #
3. 增1 #
4. 数据向量化 *
'''


def airQualityVector(qualityStr):
    '''
    将污染参数向量化
    :param qualityStr: 字符串形式的污染
    :return: 整型形式的污染
    '''
    # print('222')
    str_vecDict = {'优': 0, '良': 1, '轻度污染': 2, '中度污染': 3, '重度污染': 4}
    if str_vecDict.get(qualityStr) == None:
        print(qualityStr)
    return str_vecDict.get(qualityStr)


def getAttributeAndLabel():
    '''
    获取特征与标签
    :return: 两个词典 { 区域1:[特征], 区域2:[特征] }  { 区域1:[标签], 区域2:[标签] }
    '''
    dataPath = '汇合的表格.csv'
    '''
    A E F G H
    '''
    attributeDict = {'A': [], 'E': [], 'F': [], 'G': [], 'H': []}
    labelDict = {'A': [], 'E': [], 'F': [], 'G': [], 'H': []}
    with open(dataPath, 'r', encoding="utf-8") as f:
        data_csv = csv.DictReader(f)
        for row in data_csv:
            if row['空气质量'] != '/':
                # 分开写,方便之后的数据处理
                area = row['区域']
                # 特征部分
                taxiCount = row['出租车数量']  # 可能需要与公交之间平衡数据
                busCount = row['公交车数量']
                airTemperature = row['气温']
                windSpeed = row['风速']
                # windDirection = row['风向']
                rainFall = row['雨量']
                attributeDict[area].append([taxiCount, busCount, airTemperature, windSpeed, rainFall])
                # 标签部分
                airQuality = airQualityVector(row['空气质量'])
                labelDict[area].append(airQuality)
    return attributeDict, labelDict

def setSplit(attribuleDict, labelDict, area):
    attribuleList = attribuleDict[area]
    labelList = labelDict[area]
    X = np.array(attribuleList)
    y = np.array(labelList)
    spliter = StratifiedShuffleSplit(n_splits=10,test_size=.1,train_size=.9,random_state=0)
    spliter.get_n_splits(X,y)
    count = 0
    for train_index, test_index in spliter.split(X,y):
        print('Train Index:')
        print(train_index)
        print('Test Index:')
        print(test_index)
        print('******')
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        print(X_train)
        print(X_test)
        print('------')
        print(y_train)
        print(y_test)
        print('######')
        count += 1
    print(count)
if __name__ == '__main__':
    # print(airQualityVector('良'))
    a, b = getAttributeAndLabel()
    setSplit(a,b,'A')
    # print(a)
    # print(b)
    # print(len(a['E']))
    # print(len(b['E']))
