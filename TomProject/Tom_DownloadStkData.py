# -*- coding: utf-8 -*-


import os,sys
import numpy as np
import pandas as pd
import tushare as ts
import datetime as dt
#  zwQuant
import zwSys as zw  
import zwQTBox as zwx
import zwTools as zwt

import Tom_tools as tt
from time import ctime,sleep

'''
基础文件数据
'''
def downBase():
    '''
    下载时基本参数数据时，有时会出现错误提升：
          timeout: timed out
          属于正常现象，是因为网络问题，等几分钟，再次运行几次 
    '''  
    dat = ts.get_index()
    dat.to_csv(tt.stk_inx0,index=False,encoding='gbk',date_format='str');   
    
    dat = ts.get_stock_basics();
    dat.to_csv(tt.stk_base,encoding='gbk',date_format='str');
    
    c20=['code','name','industry','area'];
    d20=dat.loc[:,c20]
    d20['code']=d20.index;
    
    #d20=d20.sort(columns='code')
    d20=d20.sort_values(by='code')
    d20.to_csv(tt.stk_code,index=False,encoding='gbk',date_format='str');
    
    #sz50,上证50；hs300,沪深300；zz500，中证500
    dat=ts.get_sz50s();
    if len(dat)>3:
        dat.to_csv(tt.stk_sz50,index=False,encoding='gbk',date_format='str');

    dat=ts.get_hs300s();
    if len(dat)>3:
        dat.to_csv(tt.stk_hs300,index=False,encoding='gbk',date_format='str');
    
    dat=ts.get_zz500s();
    if len(dat)>3:
        dat.to_csv(tt.stk_zz500,index=False,encoding='gbk',date_format='str');


#downBase()




'''
指数数据
'''
#getInxFromFile(stk_inx0)
def getInxFromFile(filePath):
    #下载大盘指数文件，
    #filepath = 'data/inx_code.csv';
    qx=zw.zwDatX(zw._rdatCN);
    zwx.down_stk_inx(qx, filePath)

'''
个股数据指定日期至今的日结数据
'''

#日数据
#传入周期，和文件路径
#getStkFromFile(stk_code,'2017-05-01')
#getStkFromFile(select_stk_code, '2010-04-01')
def getStkFromFile(StkSourcePath,startTime): 
   #自动下载，追加数据
   #-------设置参数       
    #股票代码文件 
    #filePath='./data/stk_code.csv';
    #startTime = '1994-01-01'
    qx = zw.zwDatX(tt._rdatCN)
    zwx.down_stk_all(qx,StkSourcePath,startTime)
    


#当天tick数据数据并转换成分时数据
#getTodayTickAndCycle(stk_code, ['01','05','30'])
#getTodayTickAndCycle(select_stk_code,['01','05','30'])
def getTodayTickAndCycle(StkSourcePath, cycles):
    qx = zw.zwDatX(tt.realTickPath)
    #qx.ksgns=cycles
    zwx.xtick_real_down_all(qx,StkSourcePath,cycles)
    


        
'''
历史Tick数据
'''
def getPastTick(StkSourcePath,startDate,endDate):
    qx=zw.zwDatX(tt.hisTickPath)
    qx.xday0k=startDate
    qx.xday9k=endDate
    zwx.xtick_down8tim_all(qx, StkSourcePath)
    

#这个方法可以将任意tick数据转化成定制的
def transfToMinWithTick(tickSourceFile, outputMinDir, cycles):
    rsk=outputMinDir
    qx=zw.zwDatX()
    qx.code=tickSourceFile.split(os.path.sep)[-1].split('_')[1].split('.')[0]
    qx.min_ksgns=cycles
    zwx.xtick2tim100(qx,tickSourceFile)
    zwx.xtick2minWr(qx,rsk)
    


    
#def mergeTwoTick
    #print(df)
#print(outputMinDir)
#transToMinWithTickSourceDir(select_stk_code,tickSourceDir,outputMinDir,'2015-01-06','2015-01-12',['01','30'])

#xstr = 'xxxx_123123'
#xstr =xstr.split('_')[1]
    
#获取code从starttime起的日数据
def getStkCodeDayDate(code,startTime):
    selectDF,datastyle=tt.initDatDateSelectFileWithCode(code,startTime)
    readPath=tt.joinPath(tt.dayDataDir,code+'.csv')
    if os.path.exists(readPath)==False:
        getStkFromFile(tt.select_stk_code,startTime)
    else:
        tdf=tt.readDf(readPath)
        sd=tt.str2dateYmd(startTime)
        ed=tt.str2dateYmd(tt.dateYmd2str(tt.today_Date))
        fd=tt.str2dateYmd(tdf.tail(1)['date'].values[0])
        td=tt.str2dateYmd(tdf.head(1)['date'].values[0])
        if abs((fd-sd)/tt.one_Day_Delta)>=3 or ed>td+tt.one_Day_Delta:
            tt.remove(readPath)
            fd,td=sd,ed
            getStkFromFile(tt.select_stk_code,startTime)
    tdf=tt.readDf(readPath)
    fromDate=tdf.tail(1)['date'].values[0]+' '+tt.endTradeTime
    toDate=tdf.head(1)['date'].values[0]+' '+tt.endTradeTime
    return readPath,tdf,fromDate,toDate,selectDF,datastyle

def getStkCodeTodayTickData(code):
    selectDF,datastyle=tt.initRealTickSelectFileWithCode(code)
    readPath=tt.realTickPath
    readPath=tt.joinPath(readPath,code+'.csv')
    cycleStr='%02d' %selectDF.loc[0,'cycle']
    getTodayTickAndCycle(tt.select_stk_code,[cycleStr])
    tdf=tt.readDf(readPath)
    fromDate=tt.today_Date_Ymd_Str+' '+tdf.tail(1)['time'].values[0]
    toDate=tt.today_Date_Ymd_Str+' '+tdf.head(1)['time'].values[0]
    return readPath,tdf,fromDate,toDate,selectDF,datastyle

def getStkCodeTodayMinData(code,cycle):
    selectDF,datastyle=tt.initRealTickToMinSelectFileWithCode(code,cycle)
    readPath=tt.realTickPath
    cycle='%02d' %int(cycle)
    readPath=tt.joinPath(readPath,'M'+cycle,code+'.csv')
    cycleStr='%02d' %selectDF.loc[0,'cycle']
    getTodayTickAndCycle(tt.select_stk_code,[cycleStr])
    tdf=tt.readDf(readPath)
    fromDate=tt.today_Date_Ymd_Str+' '+tdf.tail(1)['time'].values[0]
    toDate=tt.today_Date_Ymd_Str+' '+tdf.head(1)['time'].values[0]
    return readPath,tdf,fromDate,toDate,selectDF,datastyle


def getStkCodeHisTickData(code,date):
    selecDF,datastyle=tt.initHisTickSelectFileWithCode(code,date)
    readPath=tt.getHisTickCodePath(code,date)
    if not tt.isExist(readPath):
        print('Date:'+date+' Code:'+str(code)+' is saving...')
        getPastTick(tt.select_stk_code,date,date)
    try:
        tdf=tt.readDf(readPath)
        fromDate=date+' '+tdf.tail(1)['time'].values[0]
        toDate=date+' '+tdf.head(1)['time'].values[0]
        return readPath,tdf,fromDate,toDate,selecDF,datastyle
    except Exception as e:
        print(date+' has no data')
        return None,None,None,None,None,None


def getStkCodeHisTickToMinData(code,date,cycle):
    selecDF,datastyle=tt.initHisTickToMinSelectFileWithCode(code,date,cycle)
    readPath=tt.getHisTickToMinCodePath(code,date,cycle)
    if not tt.isExist(readPath):
        xReadPath,xtdf,xfromDate,xtoDate,xSelectDF,xDatastyle=getStkCodeHisTickData(code,date)
        if xReadPath==None:
            print(str(code)+'at:'+date+' No HisTick Data')
            return None,None,None,None,None,None
        if tt.isExist(xReadPath):
            selecDF,datastyle=tt.initHisTickToMinSelectFileWithCode(code,date,cycle)
            transfToMinWithTick(xReadPath,tt.joinPath(tt.outputMinDir,date),[cycle])
    if tt.isExist(readPath):
        tdf=tt.readDf(readPath)
        fromDate=date+' '+tdf.tail(1)['time'].values[0]
        toDate=date+' '+tdf.head(1)['time'].values[0]
        return readPath,tdf,fromDate,toDate,selecDF,datastyle
    else:
        print(date+' has no data')
    
    
    
'''
tickSourceDir指定需要转换的历史tick数据父路径../TomQuantData/min/tick
outputMinDir转换完成以后传出到该文件目录，无需添加日期标记文件夹
date传入需要转换的日期data='yyyy-mm-dd'
cycle指定修改的周期列表
'''
def transToMinWithTickSourceDir(baseCodefile,tickSourceDir,outputMinDir,startDate,endDate,cycles):
    #date='2015-01-01'
    #sdf=pd.read_csv(selectCodefile,encoding='gbk')
    sdf=tt.readDf(baseCodefile)
    selectCodes=sdf['code']
    #print[selectCodes]
    os.chdir(tickSourceDir)
    os.listdir()
    sd=tt.str2dateYmd(startDate)
    ed=tt.str2dateYmd(endDate)
    while(sd<=ed):
        getYM=tt.dateYm2str(sd)
        for d in os.listdir():
            if d == getYM:
                mouthDir=tt.joinPath(tickSourceDir,getYM)
                datestr=tt.dateYmd2str(sd)
                for f in os.listdir(mouthDir):
                    if f.startswith(datestr):
                        for code in selectCodes:
                            if f.split('_')[1].split('.')[0]=='%06d'%int(code):
                                f=tt.joinPath(mouthDir,f)
                                outD=tt.joinPath(outputMinDir,datestr)
                                if not tt.isExist(outD):
                                    os.makedirs(outD)
                                transfToMinWithTick(f,outD,cycles)
        sd+=tt.one_Day_Delta
   
#批量下载才允许合并
def mergeMinData(startDate,endDate,cycle,code):
    df=pd.DataFrame()
    #cycle=1
    #cycle='M'+'%02d' %int(cycle)
    code='%06d' %int(code)
    dl=tt.getNoWeekendDateList(startDate,endDate)
    dl=dl[::-1]
    for date in dl:
        #hisMinFilePath=os.path.join(tt.hisTickToMinPath,date,cycle,code+'.csv')
        hisMinFilePath=tt.getHisTickToMinCodePath(code,date,cycle)
        if tt.isExist(hisMinFilePath):
            df0=tt.readDf(hisMinFilePath)
            for i in range(df0.index.size):
                df0.loc[i,'time']=date+''+str(df0.loc[i,'time'])
            if df.size<10:
                df=df0
            else:
                df=pd.concat([df,df0],ignore_index=True)
    if df.size == 0:
        print('[-]Error:No Data????Code:'+code+'startDate:'+startDate+'endDate:'+endDate+'cycle:'+cycle+' date:'+date)
        return None,None
    #outputPath=os.path.join(tt.hisCodeMinPath,cycle,code+'.csv')
    outputDir=tt.joinPath(tt.hisCodeMinPath,cycle)
    readPath=tt.joinPath(outputDir,code+'.csv')
    #tt.saveFileToDir(startDate+'-'+endDate+'-'+code+'.csv',outputDir,df)
    tt.saveDFNoIndex(readPath,df)
    return df,readPath


#批量下载才允许合并
def mergeMinDataX(startDate,endDate,cycle,code):
    df=pd.DataFrame()
    code='%06d' %int(code)
    readPath=tt.getHisTickToMinMergeCodePath(code,cycle)
    dl=tt.getNoWeekendDateList(startDate,endDate)
    dl=dl[::-1]
    if tt.isExist(readPath):
        #获取原来文件存在的日期
        existDates=[]
        df=tt.readDf(readPath)
        times=df.time
        for time in times:
            time=(tt.str2dateYmdHMS(time))
            time=tt.dateYmd2str(time)
            if len(existDates)==0:
                existDates.append(time)
            else:
                if not existDates[-1]==time:
                    existDates.append(time)
        existDates.sort(reverse=True)
        
        #先判断merge数据中存在date日期否
        for date in dl:
            if date in existDates:
                continue
            else:
                hisMinFilePath=tt.getHisTickToMinCodePath(code,date,cycle)
                #hisMinFilePath=tt.getHisTickToMinMergeCodePath(code,cycle)
                if tt.isExist(hisMinFilePath):
                    df0=tt.readDf(hisMinFilePath)
                    for i in range(df0.index.size):
                        df0.loc[i,'time']=date+''+str(df0.loc[i,'time'])
                    if df.size<10:
                        df=df0
                    else:
                        df=pd.concat([df,df0],ignore_index=True)
        df=df.sort_values(by='time',ascending=False)
        df=df.reset_index(drop=True)
        
    else:
        for date in dl:
            hisMinFilePath=tt.getHisTickToMinCodePath(code,date,cycle)
            if tt.isExist(hisMinFilePath):
                df0=tt.readDf(hisMinFilePath)
                for i in range(df0.index.size):
                    df0.loc[i,'time']=date+''+str(df0.loc[i,'time'])
                if df.size<10:
                    df=df0
                else:
                    df=pd.concat([df,df0],ignore_index=True)
        if df.size == 0:
            print('[-]Error:No Data????Code:'+code+'startDate:'+startDate+'endDate:'+endDate+'cycle:'+cycle+' date:'+date)
            return None,None
    #readPath=tt.getHisTickToMinMergeCodePath(code,cycle)
    #tt.saveFileToDir(startDate+'-'+endDate+'-'+code+'.csv',outputDir,df)
    tt.saveDFNoIndex(readPath,df)
    return df,readPath
    
#智能判断下载股票代码并转化分时
def downCode(code,startDate,endDate,cycles):
    dl=tt.getNoWeekendDateList(startDate,endDate)
    for cycle in cycles:
        for date in dl:
            getStkCodeHisTickToMinData(code,date,cycle)
                
#在操作该方法之前先添加收藏的股票代码到收藏文件
def downAndMergeFavCodeMinData(startDate,endDate,cycles):
    codes = tt.readDf(tt.fav_stk_code).code.values
    for code in codes:
        downCode(code,startDate,endDate,cycles)
     #转换完成以后才能合并所以不能合在一起
    readPaths=list()
    for code in codes:
        code='%06d' %int(code)
        for cycle in cycles:
            df,readPath=mergeMinDataX(startDate,endDate,cycle,code)
            readPaths.append(readPath)
    return readPaths

def getFavLongTimeData(startDate,endDate,cycles):
    #tt.removeStkFromFav('ALL')
    #tt.addStkCodesToFav(codes)
    return downAndMergeFavCodeMinData(startDate,endDate,cycles)



'''
单个数据下载
'''
def downHisTickDate(code,dateStr):
    dtime=tt.str2dateYmd(dateStr)
    getYM=tt.dateYm2str(dtime)
    getYMD=dateStr
    readPath=tt.hisTickPath
    code='%06d'%int(code)
    readPath=os.path.join(readPath,getYM,getYMD+'_'+code+'.csv')
    if not tt.isExist(readPath):
        if tt.isWeekEnd(getYMD):
            print('[*] '+code+''+getYMD + ' is Weekend ')
            return
        df=downHisTickData(code,getYMD)
        if len(df)<10:
            print('[-] '+code+''+getYMD + ' have no Data ')
            return
        else:
            print('[+] '+code+''+getYMD+' is Saving... ')
            tt.saveDFNoIndex(readPath,df)
    else:
        print('[+] '+code+''+getYMD+ ' is Exist ')
'''
批量本地判断下载历史分时数据
'''
def downHisFavTickDatasJudgeLocal(startDate,endDate):
    sd=tt.str2dateYmd(startDate)
    ed=tt.str2dateYmd(endDate)
    codes=tt.getFavList().code
    while sd<=ed:
        dateStr=tt.dateYmd2str(sd)
        for code in codes:
            downHisTickDate(code,dateStr)
        sd+=tt.one_Day_Delta
        
downloadNum = 0
def downHisTickData(code,date):
    global downloadNum
    df,dn=pd.DataFrame(),0
    try:
        df = ts.get_tick_data(code,date=date)    #print(df.head())
    except IOError: 
        pass    #skip,error 
    if type(df)==type(None):
        df=pd.DataFrame()
    dn=len(df)
    # print('     n',dn,ftg) # 跳过无数据 日期
    #if zwt.xin(dn,0,9):print('n2',dn,ftg) 
    if dn>10:  
        df['type']=df['type'].str.replace(u'中性盘', 'norm');
        df['type']=df['type'].str.replace(u'买盘', 'buy');
        df['type']=df['type'].str.replace(u'卖盘', 'sell');
        downloadNum+=1
        if downloadNum>=5:
            downloadNum=0
            sleep(20)
    return df

#df=downHisTickData('000001', '2017-08-05')