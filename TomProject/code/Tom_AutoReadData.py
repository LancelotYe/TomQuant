# -*- coding: utf-8 -*-
import os,sys
import Tom_DownloadStkData as td
import Tom_Draw as tda
import pandas as pd
import numpy as np
import datetime as dt



#DataStyle=Enum('dayData','hisTick','hisTickToMin','realTick')

'''
datastyle=['dayData','hisTick','hisTickToMin','realTick','realTickToMin','hisCodeMin']
'''
#def readStk(datastyle,date,cycle,code,hisCodeMinEndDate):
'''
def readStk(datastyle,date,cycle,code):
    selectDF=td.selectOneStkCode(code,datastyle,date,cycle)
    fromDate=''
    toDate=''
    delta=dt.timedelta(days=1)
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
            if(startDate-frD)>=7*delta or (startDate-frD)<=-7*delta or toD-endDate>delta:
                os.remove(readPath)
                td.getStkFromFile(td.select_stk_code,date)
    elif datastyle=='hisTick':
        readPath=td.hisTickPath
        #date='1992-01-03'
        Ddate=dt.datetime.strptime(date,'%Y-%m-%d')
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
        readPath=td.hisTickToMinPath
        readPath=os.path.join(readPath,date,'M'+cycle,code+'.csv')
        if os.path.exists(readPath)==False:
            XreadPath=td.hisTickPath
        #date='1992-01-03'
            Ddate=dt.datetime.strptime(date,'%Y-%m-%d')
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
       
    elif datastyle=='hisCodeMin':
        readPath=td.hisCodeMinPath
        readPath=os.path.join(readPath,'M'+cycle,code+'.csv')
        if os.path.exists(readPath)==False:
            sd=dt.datetime.strptime(date,'%Y-%m-%d')
            ed=dt.datetime.strptime(hisCodeMinEndDate,'%Y-%m-%d')
            while(sd<=ed):
                sdstr=dt.datetime.strftime(sd,'%Y-%m-%d')
                xReadPath=td.hisTickPath
                #date='1992-01-03'
                Ddate=dt.datetime.strptime(date,'%Y-%m-%d')
                Tdate=Ddate+delta
                tdate=dt.datetime.strftime(Tdate,'%Y-%m-%d')
                getYM=dt.datetime.strftime(Ddate,'%Y-%m')
                xReadPath=os.path.join(xReadPath,getYM,date+'_'+code+'.csv')
                if os.path.exists(xReadPath)==False:
                    td.getPastTick(td.select_stk_code,date,tdate)
                    tdf=pd.read_csv(xReadPath, encoding='gbk')
                    #fromDate=date+' '+tdf.tail(1)['time'].values[0]
                    #toDate=date+' '+tdf.head(1)['time'].values[0]
                sd+=delta
                
            td.transToMinWithTickSourceDir(td.select_stk_code,td.his_tick_sourceDir,td.outputMinDir,date,hisCodeMinEndDate,[cycle])
        df=pd.read_csv(readPath,encoding='gbk')
        fromDate=df.loc[df.index.size-1,'time']
        toDate=df.loc[0,'time']
      
    else:
        print('No such type')
        return
    #print(readPath)
    df=pd.read_csv(readPath, encoding='gbk')
    #print(df)
    #print(readPath)
    #print(fromDate)
    #print(toDate)
    return readPath,df,fromDate,toDate,selectDF, datastyle
'''
#rP,df,fromDate,toDate=readStk('hisTick','2015-02-25','01','000001')
def readNextStk():
    selectDF=td.selectNextCodeInStkCode()
    code=selectDF.loc[0,'code']
    code="%06d" %code
    datastyle=selectDF.loc[0,'datastyle']
    date=selectDF.loc[0,'date']
    cycle=selectDF.loc[0,'cycle']
    cycle="%02d" %cycle
    #hisCodeMinEndDate=selectDF.loc[0,'hisCodeMinEndDate']
    return readStk(datastyle,date,cycle,code)

def readAfterXDay(xday):
    selectDF=td.selectCodeAddDate(xday)
    code=selectDF.loc[0,'code']
    code="%06d" %code
    datastyle=selectDF.loc[0,'datastyle']
    date=selectDF.loc[0,'date']
    cycle=selectDF.loc[0,'cycle']
    cycle="%02d" %cycle
    #hisCodeMinEndDate=selectDF.loc[0,'hisCodeMinEndDate']
    return readStk(datastyle,date,cycle,code)

def readNextDatastyleStk():
    selectDF=td.selectCodeNextDatastyle()
    code=selectDF.loc[0,'code']
    code="%06d" %code
    datastyle=selectDF.loc[0,'datastyle']
    date=selectDF.loc[0,'date']
    cycle=selectDF.loc[0,'cycle']
    cycle="%02d" %cycle
    #hisCodeMinEndDate=selectDF.loc[0,'hisCodeMinEndDate']
    return readStk(datastyle,date,cycle,code)

def readOtherCycleData(cycle):
    selectDF=td.selectCodeOtherCycle(cycle)
    code=selectDF.loc[0,'code']
    code="%06d" %code
    datastyle=selectDF.loc[0,'datastyle']
    date=selectDF.loc[0,'date']
    cycle=selectDF.loc[0,'cycle']
    cycle="%02d" %cycle
    #hisCodeMinEndDate=selectDF.loc[0,'hisCodeMinEndDate']
    return readStk(datastyle,date,cycle,code)
'''
def readOtherHisCodeMinEndDate(hisCodeMinEndDate):
    selectDF=td.selectCodeOtherHisCodeMinEndDate(hisCodeMinEndDate)
    code=selectDF.loc[0,'code']
    code="%06d" %code
    datastyle=selectDF.loc[0,'datastyle']
    date=selectDF.loc[0,'date']
    cycle=selectDF.loc[0,'cycle']
    cycle="%02d" %cycle
    hisCodeMinEndDate=selectDF.loc[0,'hisCodeMinEndDate']
    return readStk(datastyle,date,cycle,code,hisCodeMinEndDate)
'''

def readStk(datastyle,date,cycle,code):
    if datastyle=='dayData':
        return td.getStkCodeDayDate(code,date)
    elif datastyle=='realTick':
        return td.getStkCodeTodayTickData(code)
    elif datastyle=='realTickToMin':
        return td.getStkCodeTodayMinData(code,cycle)
    elif datastyle=='hisTick':
        return td.getStkCodeHisTickData(code,date)
    elif datastyle=='hisTickToMin':
        return td.getStkCodeHisTickToMinData(code,date,cycle)
'''
readPath,tdf,fromDate,toDate,selecDF,datastyle=readStk('realTickToMin','2017-05-11','05','600111')
print(readPath)
print(tdf)
print(fromDate,toDate)
print(selecDF)
print(datastyle)
'''