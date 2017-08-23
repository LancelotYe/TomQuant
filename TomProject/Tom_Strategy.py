# -*- coding: utf-8 -*-\
import pandas as pd
import numpy as np
import Tom_tools as tt
import math

'''
rP='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/cn/day/603859.csv'
df=tt.readDf(rP)
df0=df.loc[0,'close']

df020=df.head(20)
closes=df.close


closes
x=getMean(closes)
'''
def getXdayMeanPrice(x,df,target):
    num=x
    numStr=str(num)
    #df=df.drop('mean5',axis=1)
    size=df.index.size
    while x<=size:
        df.at[size-x,'mean'+numStr]=getMean([df.loc[i,target] for i in range(size-x+num)[-num:]])
        x+=1
    return df

#df0=getXdayMeanPrice(5,df,'close')
def deleteMeanData(x,rP):
    df=tt.readDf(rP)
    df=df.drop('mean'+str(x),axis=1)
    df=df.drop('accelerated'+str(x),axis=1)
    tt.saveDFNoIndex(rP,df)
def initMeanAndAcceleratedData(x,rP,target):
    df=tt.readDf(rP)
    df=getXdayMeanPrice(x,df,target)
    df=getMeanAcceleratedSpeed(x,df)
    tt.saveDFNoIndex(rP,df)
    
    

def getStandardDeviation(prices):
    mean=getMean(prices)
    vals=[math.pow(abs(p-mean),2) for p in prices]
    return math.pow(sum(vals)/len(vals),0.5)
def getMean(prices):
    return sum(prices)/len(prices)

def bollChannel(prices):
    m=getMean(prices)
    sd=getStandardDeviation(prices)
    return m+2*sd, m-2*sd

def getMeanAcceleratedSpeed(x,df):
    for i in range(df.index.size-1):
        df.at[i,'accelerated'+str(x)]=df.loc[i,'mean'+str(x)]-df.loc[i+1,'mean'+str(x)]
    return df
#缠
'''
step1
找出顶点
'''
def getTopIndex(a):
    ax=list()
    for index in range(len(a)):
        if ifHigherThanLast(index, a) and ifHigherThanNext(index,a):
            ax.append(index)
    return ax
def ifHigherThanNext(index, array):
    if index==len(array)-1:
        return True
    if array[index]>array[index+1]:
        return True
    elif array[index]==array[index+1]:
        return ifHigherThanNext(index+1, array)
    else:
        return False
    
def ifHigherThanLast(index, array):
    if index==0:
        return True
    if array[index]>array[index-1]:
        return True
    else:
        return False
    
'''
找出底点
'''
def getBottomIndex(a):
    ax=list()
    for index in range(len(a)):
        if ifLowerThanLast(index,a) and ifLowerThanNext(index,a):
            ax.append(index)
    return ax

def ifLowerThanNext(index, array):
    if index==len(array)-1:
        return True
    if array[index]<array[index+1]:
        return True
    elif array[index]==array[index+1]:
        return ifLowerThanNext(index+1, array)
    else:
        return False
        
def ifLowerThanLast(index, array):
    if index==0:
        return True
    if array[index]<array[index-1]:
        return True
    else:
        return False
    
array = [1,1,3,3,3,3,2,6,1,7,3,2,4,9,3,3,6,4,2,5,7,4,3,6,7,5]
getTopIndex(array)
getBottomIndex(array)

hIndex=getTopIndex(high)
lIndex=getBottomIndex(low)

'''
step2
合并hl索引
'''
def connectHIndexAndLIndex(hIndex, lIndex):

    
'''
初始化起始值
'''
hIndex, lIndex, high, low
def getFirstIndex():
    global hIndex,lIndex,high,low
    high==df.high
    low=df.low
    hIndex=getTopIndex(high)
    lIndex=getBottomIndex(low)
    i=len(hIndex)
    j=len(lIndex)
    x = max(i,j)
    for i in range(x):
        if hIndex[i]==lIndex[i]:
            continue
        elif hIndex[i]>lIndex[i]:
            return 'l',i
        elif lIndex[i]>hIndex[i]:
            return 'h',i
        
hl, index = getFirstIndex()

def getNextIndex(hl,index):
    global hIndex,lIndex,high,low
    if hl == 'h':
        x=0
        while lIndex[x]>=index+4:
            x+=1
        for i in range(x)[-(x-index):]:
            if high[index] < high[i]:
                return 'h',i
            elif low[x]>low[i]:
                return getNextIndex('h', i)
            return 'l', x
    elif hl == 'l':
        x=0
        while lIndex[x]>=index+4:
            x+=1
        for i in range(x)[-(x-index):]:
            if low[index] > low[i]:
                return 'l',i
            elif high[x]<high[i]:
                return getNextIndex('l', i)
            return 'h', x
        
def skipInvolveDataNextIndex(index):
    global hIndex,lIndex,high,low
    h=high[index]
    l=low[index]
    index+=1
    while high[index]<h and low[index]>l:
        index+=1
    return index
    