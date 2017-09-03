# -*- coding: utf-8 -*-\
import pandas as pd
import numpy as np
import Tom_tools as tt
import math


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
    
'''
array = [1,1,3,3,3,3,2,6,1,7,3,2,4,9,3,3,6,4,2,5,7,4,3,6,7,5]
getTopIndex(array)
getBottomIndex(array)

hIndex=getTopIndex(high)
lIndex=getBottomIndex(low)
'''
'''
step2
合并hl索引
'''
#def connectHIndexAndLIndex(hIndex, lIndex):

    
'''
初始化起始值
'''
hIndexs=[]
lIndexs=[]
highs=[]
lows=[]



'''
包含数据跳过
'''
def skipInvolveDataNextIndex(index):
    global hIndexs,lIndexs,highs,lows
    h=highs[index]
    l=lows[index]
    index+=1
    if len(highs)-1 == index or len(lows)-1 == index:
        return None
    while highs[index]<h and lows[index]>l:
        if len(highs)-1 == index or len(lows)-1 == index:
            return None
        index+=1
    return index

'''
跳过x个包含数据
'''
def skipInvolveDataXIndex(index, x):
    while x > 0:
        index=skipInvolveDataNextIndex(index)
        if index == None:
            return None
        x-=1
    return index

'''
得到第一的索引及顶底标记
'''
#hl, index = getFirstIndex()

'''
获取下一个索引及顶底标记
'''

def findNextLowIndex(index):
    global lIndexs
    index+=1
    if len(lIndexs)-1 >= index:
        return lIndexs[index]
    else:
        return None
def findNextHighIndex(index):
    global hIndexs
    index+=1
    if len(hIndexs)-1 >= index:
        return hIndexs[index]
    else:
        return None
    
def compareBottomOrTopWithBefore(startIndex, endIndex, hl):
    if hl == 'h':
        x=0
        #至少大于第四个不包含的数据的索引列表的索引
        
        while lIndexs[x]< endIndex:
            x+=1
            if len(lIndexs)-1<x:
                return None, None
        endIndex=lIndexs[x]
        #循环检查数据
        #step1检查在找到的索引期间是否存在更高的顶点
        for i in range(startIndex,endIndex+1):
            #print(i)
            if highs[startIndex] < highs[i]:
                return 'h',i
        #step2检查在找到的索引期间是否存在比目标索引小的值，有的话跳下一个底索引进行比较
        for i in range(startIndex-1,endIndex+1):
            if i<0:
                continue
            if lows[endIndex]>lows[i]:
                endIndex=findNextLowIndex(x)
                if endIndex==None:
                    return None,None
                return compareBottomOrTopWithBefore(startIndex, endIndex, hl)
        return 'l', endIndex
    elif hl == 'l':
        x=0
        while hIndexs[x]<endIndex:
            x+=1
            if len(hIndexs)-1<x:
                return None,None
            
        
        endIndex=hIndexs[x]
        for i in range(startIndex, endIndex+1):
            if lows[startIndex] > lows[i]:
                return 'l',i
        for i in range(startIndex-1, endIndex+1):
            if i < 0:
                continue
            if highs[endIndex]<highs[i]:
                endIndex=findNextHighIndex(x)
                if endIndex==None:
                    return None, None
                return compareBottomOrTopWithBefore(startIndex,endIndex,hl)
        return 'h', endIndex
    
    
'''
df根据时间升序排列
'''
def getRightIndexDF(df):
    df=df.sort_values(by=['time'])
    df=df.reset_index(drop=True)
    return df
'''
0.1步找到笔的数据
'''
def getFirstPen(df):
    global hIndexs,lIndexs,highs,lows
    highs=df.high
    lows=df.low
    hIndexs=getTopIndex(highs)
    lIndexs=getBottomIndex(lows)
    #i=len(hIndexs)
    #j=len(lIndexs)
    #x = max(i,j)
    i=0
    while hIndexs[i]==lIndexs[i]:
        i+=1
    if hIndexs[i]>lIndexs[i]:
            return 'l',i
    elif lIndexs[i]>hIndexs[i]:
            return 'h',i
        
def getNextPen(hl,index):
    global hIndex,lIndex,high,low
    FdayInvolveIndex=skipInvolveDataXIndex(index, 4)
    if FdayInvolveIndex == None:
        return None,None
    startIndex=index
    return compareBottomOrTopWithBefore(startIndex, FdayInvolveIndex, hl)

def findAllPen(df):
    df0 = pd.DataFrame()
    hl, index = getFirstPen(df)
    i=0
    while index <= max(lIndexs[-1],hIndexs[-1]):
        df0.loc[i,'hl']=hl
        df0.loc[i,'index']=index
        hl,index=getNextPen(hl,index)
        if hl==None or index==None:
            return df0
        i+=1
    return df0

#df0=findTopsAndBottoms(df)

def filterUsefulPen(df):
    df0 = findAllPen(df)
    df1 = pd.DataFrame()
    x = 0
    while x <= df0.index.size-1:
        if x==0:
            df1=df0.loc[[0]]
        else:
            hl = df1.tail(1)['hl'].values[0]
            index = df1.tail(1).index.values[0]
            if hl == df0.loc[x, 'hl']:
                df1.loc[index] = df0.loc[x]
            else:
                df1=pd.concat([df1,df0.loc[[x]]],ignore_index=True)
        x+=1
    return df1


def findPen(df):
    #dataframe先根据时间排序
    df=getRightIndexDF(df)
    df0=filterUsefulPen(df)
    for i in range(df0.index.size):
        hl = df0.loc[i,'hl']
        index = int(df0.loc[i,'index'])
        df0.loc[i,'time']=df.loc[index,'time']
        if hl=='h':
            df0.loc[i,'price']=df.loc[index,'high']
        elif hl=='l':
            df0.loc[i,'price']=df.loc[index,'low']
    return df0
#



'''
找到线段数据
'''
    
def getLineHighDF(df):
    df=df.reset_index(drop=True)
    df0=pd.DataFrame()
    for i in range(df.index.size):
        if 0<i<df.index.size-1:
            if df.loc[i-1,'price']<=df.loc[i,'price'] and df.loc[i+1, 'price']<=df.loc[i,'price']:
                df0=pd.concat([df0,df.loc[[i]]], ignore_index=True)
        elif i==0:
            if df.loc[i+1, 'price']<=df.loc[i,'price']:
                df0=pd.concat([df0,df.loc[[i]]], ignore_index=True)
        elif i==df.index.size-1:
            if df.loc[i-1,'price']<=df.loc[i,'price']:
                df0=pd.concat([df0,df.loc[[i]]], ignore_index=True)
    return df0

def getLineLowDF(df):
    df=df.reset_index(drop=True)
    df0=pd.DataFrame()
    for i in range(df.index.size):
        if 0<i<df.index.size-1:
            if df.loc[i-1,'price']>=df.loc[i,'price'] and df.loc[i+1, 'price']>=df.loc[i,'price']:
                df0=pd.concat([df0,df.loc[[i]]], ignore_index=True)
        elif i==0:
            if df.loc[i+1, 'price']>=df.loc[i,'price']:
                df0=pd.concat([df0,df.loc[[i]]], ignore_index=True)
        elif i==df.index.size-1:
            if df.loc[i-1,'price']>=df.loc[i,'price']:
                df0=pd.concat([df0,df.loc[[i]]], ignore_index=True)
    return df0
    
def getNextLine(index, df,targetDf):
    if index==0:
        return df.loc[[index]]
    else:
        tailDf=targetDf.tail(1)
        tailDf=tailDf.reset_index(drop=True)
        prePrice=tailDf.loc[0,'price']
        preHL=tailDf.loc[0,'hl']
        price=df.loc[index,'price']
        hl=df.loc[index,'hl']
        if preHL=='h' and hl=='h':
            if prePrice>=price:
                return targetDf
            elif prePrice<price:
                targetDf=targetDf.head(targetDf.index.size-1)
                targetDf=pd.concat([targetDf,df.loc[[index]]],ignore_index=True)
                return targetDf
        elif preHL=='h' and hl=='l':
            targetDf=pd.concat([targetDf,df.loc[[index]]],ignore_index=True)
            return targetDf
        elif preHL=='l' and hl=='l':
            if prePrice<=price:
                return targetDf
            elif prePrice>price:
                targetDf=targetDf.head(targetDf.index.size-1)
                targetDf=pd.concat([targetDf,df.loc[[index]]],ignore_index=True)
                return targetDf
        elif preHL=='l' and hl=='h':
            targetDf=pd.concat([targetDf,df.loc[[index]]],ignore_index=True)
            return targetDf

def fliterUsefulLine(df):
    df1=pd.DataFrame()
    index=0
    while index<df.index.size:
        df1=getNextLine(index,df,df1)
        index+=1
    return df1

def findLine(df0):
    hDf=getHDF(df0)
    hDf=getLineHighDF(hDf)
    lDf=getLDF(df0)
    lDf=getLineLowDF(lDf)
    df0=pd.concat([hDf,lDf],ignore_index=True)
    df0=df0.sort_values(by='index')
    df0=df0.reset_index(drop=True)
    LINE_DF=fliterUsefulLine(df0)
    return LINE_DF


'''
找到中枢数据
'''
def getSpan(df):
    hdf=getHDF(df)
    ldf=getLDF(df)
    lineNum = len(df.index)-1
    hIndex=0
    lIndex=0
    hl=whoseFirstIndexFront(hdf,ldf)
    df0=pd.DataFrame()
    df1=pd.DataFrame()
    while lineNum>0:
        spanH=hdf.loc[hIndex,'price']
        spanL=ldf.loc[lIndex,'price']
        span=spanH-spanL
        if hl=='h':
            #锁定跨度的x轴坐标
            spanIndex=ldf.loc[lIndex,'index']
            hIndex+=1
        else:
            spanIndex=hdf.loc[hIndex,'index']
            lIndex+=1
        
        df0.loc[0,'spanIndex']=spanIndex
        df0.loc[0,'span']=span
        df0.loc[0,'spanL']=spanL
        df0.loc[0,'spanH']=spanH
        df1=pd.concat([df1,df0],ignore_index=True)
        hl=switchHL(hl)
        lineNum-=1
    return df1
def compareSpan(originSpan,targetSpan):
    if originSpan.spanL>=targetSpan.spanL and originSpan.spanH<=targetSpan.spanH:
        return True
    else:
        return False
#判断一个span在spans中形成多少个连续的中枢,并返回这个中枢
def spanTakeRoundToCenter(spanIndex,spanDf):
    #先往后判断
    startSpan=spanDf.loc[spanIndex]
    startIndex=spanIndex
    endIndex=spanIndex
    toBackList=range(spanIndex,len(spanDf.index))
    toFrontList=range(spanIndex)[::-1]
    for index in toBackList:
        targetSpan=spanDf.loc[index]
        if not compareSpan(startSpan, targetSpan):
            break
        else:
            endIndex=index

    for index in toFrontList:
       
        targetSpan=spanDf.loc[index]
        if not compareSpan(startSpan, targetSpan):
            break
        else:
            startIndex=index
    df=spanDf.loc[range(startIndex,endIndex+1)]
    return df
        

def getMinSpanIndex(spandf):
    minSpanIndex=spandf[spandf.span==min(spandf.span)].index.values[0]
    return minSpanIndex

def getSpanBlocks(spandf):
    spandf0=spandf
    #符合组合条件的span链接快
    spanBlocks=[]
    while spandf0.index.size>0:
        minSpanIndex=getMinSpanIndex(spandf0)
        dfx=spanTakeRoundToCenter(minSpanIndex,spandf)
        indexs=dfx.index
        for index in indexs:
            if not index in spandf0.index:
                indexs=np.delete(indexs,np.where(indexs==index),axis=0)
        startIndex=min(indexs)
        endIndex=max(indexs)
        if len(range(startIndex,endIndex+1))>=3:
            #构成中枢
            dfx=dfx.loc[startIndex:endIndex]
            #print(dfx.span)
            dfx=dfx.reset_index(drop=True)
            spanBlocks.append(dfx)
        for i in range(startIndex,endIndex+1):
            spandf0=spandf0.drop(i)
    return spanBlocks
    
def findCenter(linedf):
    spandf=getSpan(linedf)
    spanBlocks=getSpanBlocks(spandf)
    #print(spanBlocks)
    centerDf=pd.DataFrame()
    for i in range(len(spanBlocks)):
        sd=spanBlocks[i]
        centerDf.loc[i,'startIndex']=sd.head(1).spanIndex.values[0]
        centerDf.loc[i,'endIndex']=sd.tail(1).spanIndex.values[0]
        centerDf.loc[i,'lowPrice']=max(sd.spanL)
        centerDf.loc[i,'highPrice']=min(sd.spanH)
    return centerDf




'''
创建类
'''
'''
画图数据日期截取
'''
def clipMergeDFWithDate(df,sd,ed):
    dates=tt.getNoWeekendDateList(sd,ed)
    sd=dates[0]
    ed=dates[-1]
    sIndex=0
    eIndex=0
    for time in df.time.values:
        if sd in time:
            sIndex=df[df.time==time].index.values[0]
                
    for time in df.time.values:
        if ed in time:
            eIndex=df[df.time==time].index.values[0]
            break
    df=df.loc[eIndex:sIndex]
    df=df.reset_index(drop=True)
    return df
    
class Chan:
    def __init__(self,rP,sd,ed):
        self.rP=rP
        df = tt.readDf(rP)
        df=clipMergeDFWithDate(df,sd,ed)
        self.pen_df=findPen(df)
        self.line_df=findLine(self.pen_df)
        self.center_df=findCenter(self.line_df)


'''
缠策略公用方法
'''
def switchHL(hl):
    if hl=='h':
        return 'l'
    else:
        return 'h'
def whoseFirstIndexFront(hdf,ldf):
    hindex=hdf.loc[0,'index']
    lindex=ldf.loc[0,'index']
    if hindex>lindex:
        return 'l'
    else:
        return 'h'
def getHDF(df):
    return df[df.hl=='h'].reset_index(drop=True)
def getLDF(df):
    return df[df.hl=='l'].reset_index(drop=True)

