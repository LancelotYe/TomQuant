# -*- coding: utf-8 -*-
import os,sys
import Tom_DownloadStkData as td
import Tom_Draw as tda
import pandas as pd
import numpy as np
import datetime as dt



#DataStyle=Enum('dayData','hisTick','hisTickToMin','realTick')

'''
datastyle=['dayData','hisTick','hisTickToMin','realTick','realTickToMin']
'''
def readStk(datastyle,date,cycle,code):
    selectDF,codename=td.selectStkCodeList([int(code)])
    fromDate=''
    toDate=''
    if datastyle=='dayData':
        fromDate=date+' 13:00:00'
        toD=dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d')
        toDate=toD+' 13:00:00'
        readPath=td.dayDataPath
        readPath=os.path.join(readPath,code+'.csv')
        if os.path.exists(readPath)==False:
            td.getStkFromFile(td.select_stk_code,date)
        else:
            tdf=pd.read_csv(readPath, encoding='gbk')
            #print((tdf.tail(1)['date']!=date).bool)
            #print(tdf.head(1)['date']!=dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d').bool)
            
            #if (tdf.tail(1)['date']!=toD).bool or(tdf.head(1)['date']!=dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d').bool):
            startDate=tdf.tail(1)['date'].values[0]
            endDate=tdf.head(1)['date'].values[0]
            startDate=dt.datetime.strptime(startDate,'%Y-%m-%d')
            endDate=dt.datetime.strptime(endDate,'%Y-%m-%d')
            frD=dt.datetime.strptime(date,'%Y-%m-%d')
            toD=dt.datetime.strptime(toD,'%Y-%m-%d')
            delta=dt.timedelta(days=1)
            if(startDate-frD)>=7*delta or (startDate-frD)<=-7*delta or toD-endDate>delta:
                os.remove(readPath)
                td.getStkFromFile(td.select_stk_code,date)
    elif datastyle=='hisTick':
        readPath=td.hisTickPath
        #date='1992-01-03'
        Ddate=dt.datetime.strptime(date,'%Y-%m-%d')
        delta=dt.timedelta(days=1)
        Tdate=Ddate+delta
        tdate=dt.datetime.strftime(Tdate,'%Y-%m-%d')
        getYM=dt.datetime.strftime(Ddate,'%Y-%m')
        readPath=os.path.join(readPath,getYM,date+'_'+code+'.csv')
        if os.path.exists(readPath)==False:
            td.getPastTick(td.select_stk_code,date,tdate)
        tdf=pd.read_csv(readPath, encoding='gbk')
        fromDate=date+' '+tdf.tail(1)['time'].values[0]
        toDate=date+' '+tdf.head(1)['time'].values[0]
    elif datastyle=='hisTickToMin':
        #cycle='01'
        readPath=td.hisTickToMinPath
        readPath=os.path.join(readPath,date,'M'+cycle,code+'.csv')
        if os.path.exists(readPath)==False:
            XreadPath=td.hisTickPath
        #date='1992-01-03'
            Ddate=dt.datetime.strptime(date,'%Y-%m-%d')
            delta=dt.timedelta(days=1)
            Tdate=Ddate+delta
            tdate=dt.datetime.strftime(Tdate,'%Y-%m-%d')
            getYM=dt.datetime.strftime(Ddate,'%Y-%m')
            XreadPath=os.path.join(XreadPath,getYM,date+'_'+code+'.csv')
            outputdir=os.path.join(td.outputMinDir,date)
            if os.path.exists(XreadPath)==False:
                td.getPastTick(td.select_stk_code,date,tdate)
            td.transfToMinWithTick(XreadPath,outputdir,[cycle])
        tdf=pd.read_csv(readPath, encoding='gbk')
        fromDate=date+' '+tdf.tail(1)['time'].values[0]
        toDate=date+' '+tdf.head(1)['time'].values[0]
    elif datastyle=='realTick':
        readPath=td.realTickPath
        readPath=os.path.join(readPath,code+'.csv')
        td.getTodayTickAndCycle(td.select_stk_code,[cycle])
        tdf=pd.read_csv(readPath, encoding='gbk')
        fromDate=dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d')+' '+tdf.tail(1)['time'].values[0]
        toDate=dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d')+' '+tdf.head(1)['time'].values[0]
    elif datastyle=='realTickToMin':
        readPath=td.realTickToMinPath
        readPath=os.path.join(readPath,'M'+cycle,code+'.csv')
        td.getTodayTickAndCycle(td.select_stk_code,[cycle])
        tdf=pd.read_csv(readPath, encoding='gbk')
        fromDate=dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d')+' '+tdf.tail(1)['time'].values[0]
        toDate=dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d')+' '+tdf.head(1)['time'].values[0]
    else:
        print('No such type')
        return
    #print(readPath)
    df=pd.read_csv(readPath, encoding='gbk')
    #print(df)
    #print(readPath)
    #print(fromDate)
    #print(toDate)
    return readPath,df,fromDate,toDate,selectDF,codename
    
#rP,df,fromDate,toDate=readStk('hisTick','2015-02-25','01','000001')

