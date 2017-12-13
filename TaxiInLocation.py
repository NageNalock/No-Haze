#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/12 17:56
# @Author  : Daisy
# @Site    : 
# @File    : TaxiInLocation.py
# @Software: PyCharm Community Edition
'''
以空气质量监测站为中心,半径1km画区域
统计区域内出租车的数量
'''

import math
import csv


def inLoaction(siteLon, siteLat, taxiLon, taxiLat):
    '''
    判断出租车是否在区域内
    :param siteLon: 站点经度
    :param siteLat: 站点纬度
    :param taxiLon: 出租车经度
    :param taxiLat: 出租车纬度
    :return: 是否在区域内
    '''
    LONDIS = 1 / 111  # 经度
    LATDIS = 1 / (111 * math.cos(math.pi / 6))  # 纬度

    lonMax = siteLon + LONDIS
    lonMin = siteLon - LONDIS
    latMax = siteLat + LATDIS
    latMin = siteLat - LATDIS

    if (lonMin < taxiLon < lonMax) and (latMin < taxiLat < latMax):
        return True
    else:
        return False


def whichLocation(taxiLon, taxiLat):
    '''
    找出出租车在哪个站点区域
    :param taxiLon: 出租车经度
    :param taxiLat: 出租车纬度
    :return: 站点编号,如果不在站点内则返回 'N'
    '''
    siteA = [121.471826, 31.298781, 'A']
    siteB = [121.406039, 31.236417, 'B']
    siteC = [121.538132, 31.264346, 'C']
    siteD = [121.481838, 31.204286, 'D']
    siteE = [121.429884, 31.224199, 'E']
    siteF = [121.416532, 31.161486, 'F']
    siteG = [121.707211, 31.188478, 'G']
    siteH = [121.538658, 31.226424, 'H']
    siteJ = [121.582075, 31.201593, 'J']
    sites = [siteA, siteB, siteC, siteD, siteE, siteF, siteG, siteH, siteJ]
    siteNum = 'N'
    for site in sites:
        isInLocation = inLoaction(site[0], site[1], taxiLon, taxiLat)
        if isInLocation == True:
            siteNum = site[2]
    return siteNum


def writeData(dataList, headers, filename):
    fileName = filename + '.csv'
    # print(dataList)
    with open(fileName, 'a+', encoding='utf-8', newline='') as f:  # newline去行之间的空行
        w_csv = csv.DictWriter(f, headers)
        w_csv.writeheader()
        w_csv.writerows(dataList)
    f.close()


def readData(i):
    '''
    读取文件并写入
    :param i: 读取第i号文件
    :return: 空
    '''
    dataPath = 'F:\\2015Soda上海数据\Taxi数据\\' + str(i) + '\\' + 'part-00000'
    print(dataPath)
    with open(dataPath, 'r', encoding="utf-8") as f:
        flag = 0
        dataList = []
        for ii in f:
            line = f.readline().strip()
            item = line.split(',')
            if flag < 1000:
                try:
                    dataDict = {}
                    dataDict['车ID'] = item[0]
                    dataDict['接收时间'] = item[6]
                    dataDict['经度'] = item[8]
                    dataDict['纬度'] = item[9]
                    dataDict['速度'] = item[10]
                    dataDict['所在区域'] = whichLocation(float(item[8]), float(item[9]))
                except IndexError:
                    continue
                if dataDict['所在区域'] != 'N':
                    dataList.append(dataDict)
                    # print(dataDict, ':', flag)
                    flag += 1
            else:
                dataHeaders = ['车ID', '接收时间', '经度', '纬度', '速度', '所在区域']
                fileName = '出租车整合第' + str(i) + '部分数据'
                writeData(dataList, dataHeaders, fileName)  # 每1000条数据进行一次写入
                print('flag已到1000,数据已写入,数组与flag已清空')
                dataList = []
                flag = 0

    f.close()


if __name__ == '__main__':
    # print(LATDIS)
    # print(LONDIS)
    for fileNum in range(26, 31):
        # print(fileNum)
        readData(fileNum)
        # print(math.cos(math.pi))
        # testSite = whichLocation(21.476663,31.306632)
