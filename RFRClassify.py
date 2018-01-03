#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/2 16:55
# @Author  : Daisy
# @Site    : Soochow
# @File    : RFRClassify.py
# @Software: PyCharm Community Edition


from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from StratifiedShuffleSplit import getAttributeAndLabel, setSplit
from sklearn.datasets import load_iris
import math
from sklearn.model_selection import cross_val_score, ShuffleSplit

'''
随机森林分类器
'''


# def guessWhat()

def classfier(train_X, train_y, test_X, test_y, leapCount):
    # rf = RandomForestRegressor(n_estimators=1000, max_features=None, max_depth=None, bootstrap=True,
    # min_samples_leaf=leapCount)
    # print(train_X)
    rf = RandomForestRegressor()

    scores = []
    for i in range(train_X.shape[1]):
        score = cross_val_score(rf, train_X[:, i:i + 1], train_y, scoring="r2", cv=ShuffleSplit(len(train_X), 3, .3))
        scores.append((round(np.mean(score), 3)+1, str(i)))
    print(sorted(scores,reverse=True))

    # 训练训练器
    # rf.fit(train_X, train_y)



    # 测试集测试
    # correctCount = 0
    # for testNum in range(len(test_X)):
    #     testTemp = np.array(test_X[testNum]).reshape((1, -1))
    #     preResut = rf.predict(testTemp)
    #     # print(preResut)
    #     # print('标签结果', test_y[testNum])
    #     if round(preResut[0]) == test_y[testNum]:
    #         correctCount += 1

    # for testNum in range(len(train_X)):
    #     testTemp = np.array(train_X[testNum]).reshape((1, -1))
    #     preResut = rf.predict(testTemp)
    #     # print(preResut)
    #     # print('标签结果', train_y[testNum])
    #     if round(preResut[0]) == train_y[testNum]:
    #         correctCount += 1

    # print('正确的结果数', correctCount)
    # print('正确率', correctCount / len(test_X))
    # return correctCount / len(train_X)
    return 0


if __name__ == '__main__':
    data, target = getAttributeAndLabel()
    areaADataSet = setSplit(data, target, 'H')
    # { 'TrainX':[],'TestX':[],'TainY':[],'TestY':[] }

    for leapCount in range(10, 110, 10):
        accuaryList = []
        for randomData in areaADataSet:
            accuaryList.append(
                classfier(randomData['TrainX'], randomData['TrainY'], randomData['TestX'], randomData['TestY'],
                          30))  # 最佳为30-40
        sum = 0
        for accuary in accuaryList:
            sum += accuary
            # print(accuary)
        print(sum / 10)
        break


        # print('叶子节点数为', leapCount, '下的总正确率', sum / 10)
        # print('^^^^^^^')
