# -*- coding: utf-8 -*-\
import pandas as pd
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

#df0=getXdayMeanPrice(5,df)
def deleteMeanData(x,rP):
    df=tt.readDf(rP)
    df=df.drop('mean'+str(x),axis=1)
    tt.saveDFNoIndex(rP,df)
def initMeanData(x,rP,target):
    df=tt.readDf(rP)
    df=getXdayMeanPrice(x,df,target)
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