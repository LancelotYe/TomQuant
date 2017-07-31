# -*- coding: utf-8 -*-


import os,sys
import numpy as np
import pandas as pd
import tushare as ts
import tushare as ts
import datetime as dt
#  zwQuant
import zwSys as zw  
import zwQTBox as zwx
import zwTools as zwt

import Tom_tools as tt


#import Tom_Prefix as tp

#下载基础文件
#
'''
base 文件路径
'''
base = zw.getBasePath()
stk_inx0 = os.path.join(base, 'stk_inx0.csv')
stk_base = os.path.join(base, 'stk_base.csv')
stk_code = os.path.join(base, 'stk_code.csv')
stk_sz50 = os.path.join(base, 'stk_sz50.csv')
stk_hs300 = os.path.join(base, 'stk_hs300.csv')
stk_zz500 = os.path.join(base, 'stk_zz500.csv')

select_stk_code = os.path.join(base,'select_stk_code.csv')
fav_stk_code = os.path.join(base,'fav_stk_code.csv')

TomQuantData = zw.getTomQuantDataPath()
his_tick_sourceDir = os.path.join(TomQuantData, 'min', 'tick')


tickSourceDir=os.path.join(zw._rdatMin,'tick')
outputMinDir=os.path.join(zw._rdatMin)
#sourcePath
dayDataPath=os.path.join(zw._rdatCN,'day')
hisTickPath=os.path.join(zw._rdatMin,'tick')
hisTickToMinPath=os.path.join(zw._rdatMin)
realTickPath=os.path.join(zw._rdatTickReal,'tick')
realTickToMinPath=os.path.join(realTickPath)
#单只股票一段时间的历史分时数据（包含多天的），有hisTickToMin组装而来
hisCodeMinPath=os.path.join(zw._rdatMin)
#
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
    dat.to_csv(stk_inx0,index=False,encoding='gbk',date_format='str');   
    
    dat = ts.get_stock_basics();
    dat.to_csv(stk_base,encoding='gbk',date_format='str');
    
    c20=['code','name','industry','area'];
    d20=dat.loc[:,c20]
    d20['code']=d20.index;
    
    #d20=d20.sort(columns='code')
    d20=d20.sort_values(by='code')
    d20.to_csv(stk_code,index=False,encoding='gbk',date_format='str');
    
    #sz50,上证50；hs300,沪深300；zz500，中证500
    dat=ts.get_sz50s();
    if len(dat)>3:
        dat.to_csv(stk_sz50,index=False,encoding='gbk',date_format='str');

    dat=ts.get_hs300s();
    if len(dat)>3:
        dat.to_csv(stk_hs300,index=False,encoding='gbk',date_format='str');
    
    dat=ts.get_zz500s();
    if len(dat)>3:
        dat.to_csv(stk_zz500,index=False,encoding='gbk',date_format='str');


#downBase()
'''
选取自定义股票
'''
data_style=['dayData','hisTick','hisTickToMin','realTick','realTickToMin']
def initDatDateSelectFileWithCode(code,date):
    datastyle='dayData'
    if not tt.isExist(tt.select_stk_code):
        selectOneStkCode(code,datastyle,date,'05')
    else:
        selectOtherCode(code)
        selectOtherDate(date)
        selectCodeOtherDatastyle(datastyle)
    return getSelectList(),data_style
def initRealTickSelectFileWithCode(code,date):
    datastyle='realTick'
    if not tt.isExist(tt.select_stk_code):
        selectOneStkCode(code,datastyle,date,'05')
    else:
        selectOtherCode(code)
        selectOtherDate(date)
        selectCodeOtherDatastyle(datastyle)
    return getSelectList(), datastyle
def initRealTickToMinSelectFileWithCode(code,date,cycle):
    datastyle='realTickToMin'
    if not tt.isExist(tt.select_stk_code)
        selectOneStkCode(code,datastyle,date,cycle)
    else:
        selectOtherCode(code)
        selectOtherDate(date)
        selectCodeOtherDatastyle(datastyle)
        selectCodeOtherCycle(cycle)
    return getSelectList(),datastyle
#只获取date日的Tick数据
def initHisTickSelectFileWithCode(code,date):
    datastyle='hisTick'
    if not tt.isExist(tt.select_stk_code):
        selectOneStkCode(code,datastyle,date,'05')
    else:
        selectOtherCode(code)
        selectOtherDate(date)
        selectCodeOtherDatastyle(datastyle)
        selectCodeOtherCycle(cycle)
    return getSelectList(),datastyle
def initHisTickToMinSelectFileWithCode(code,date,cycle):
    datastyle='hisTickToMin'
    if not tt.isExist(tt.select_stk_code):
        selectOneStkCode(code,datastyle,date,cycle)
    else:
        selectOtherCode(code)
        selectOtherDate(date)
        selectCodeOtherCycle(cycle)
        selectCodeOtherDatastyle(datastyle)
    return getSelectList(),datastyle
#codeList = [600129]
#选中股票代码只能有一只
def selectOneStkCode(code,datastyle,date,cycle):
    tt.remove(tt.select_stk_code)
    #df=pd.read_csv(tt.stk_code, encoding='gbk')
    df=getSelectList()
    df=df[df['code'].isin([code])]
    df['datastyle']=datastyle
    df['date']=date
    df['cycle']=cycle
    #df['hisCodeMinEndDate']=hisCodeMinEndDate
    tt.saveDf(tt.select_stk_code,df)
    #df.to_csv(select_stk_code,index=False,encoding='gbk',date_format='str');
    return tt.readDf(tt.select_stk_code)
def selectNextCodeInStkCode():
    df=tt.readDf(tt.stk_code)
    #sdf=tt.readDf(tt.select_stk_code)
    sdf=getSelectList()
    index=df[df['code']==sdf['code'][0]].index.values[0]
    index+=1
    df0=df[df.index==index]
    df0['datastyle']=sdf.loc[0,'datastyle']
    df0['date']=sdf.loc[0,'date']
    df0['cycle']=sdf.loc[0,'cycle']
    df0=pd.concat([df0],ignore_index=True)
    tt.saveDf(tt.select_stk_code,df0)
    return df0
def selectOtherCode(code):
    df=getSelectList()
    df['code']=code
    tt.saveDf(tt.select_stk_code,df)
    return df
def selectCodeAddDate(xday):
    #df=pd.read_csv(select_stk_code,encoding='gbk')
    #df=tt.readDf(select_stk_code)
    df=getSelectList()
    date=df['date'].values[0]
    #date=dt.datetime.strptime(date,'%Y-%m-%d')
    date=tt.str2dateYmd(date)
    date+=xday*tt.one_Day_Delta
    #date=dt.datetime.strftime(date,'%Y-%m-%d')
    date=tt.dateYmd2str(date)
    df['date']=date
    tt.saveDf(tt.select_stk_code,df)
    return df
def selectOtherDate(date):
    df=getSelectList()
    df['date']=date
    tt.saveDf(tt.select_stk_code,df)
    return df
def selectCodeNextDatastyle():
    #df=pd.read_csv(select_stk_code,encoding='gbk')
    #df=tt.readDf(tt.select_stk_code)
    df=getSelectList()
    datastyle=df['datastyle'].values[0]
    index=0
    for ds in data_style:
        if ds==datastyle:
            index=data_style.index(ds)
    index+=1
    if index>=len(data_style):
        index=0
    df['datastyle']=data_style[index]
    #df.to_csv(select_stk_code,encoding='gbk')
    tt.saveDf(tt.select_stk_code,df)
    return df
def selectCodeOtherDatastyle(datastyle):
    df=getSelectList()
    df['datastyle']=datastyle
    tt.saveDf(tt.select_stk_code,df)
def selectCodeOtherCycle(cycle):
    #df=pd.read_csv(select_stk_code,encoding='gbk')
    #df=tt.readDf(tt.select_stk_code)
    df=getSelectList()
    df['cycle']=cycle
    tt.saveDf(tt.select_stk_code,df)
    #df.to_csv(select_stk_code,encoding='gbk')
    return df
def getSelectList():
    return tt.readDf(tt.select_stk_code)
    #return pd.read_csv(select_stk_code,encoding='gbk')
'''
def selectCodeOtherHisCodeMinEndDate(hisCodeMinEndDate):
    df=pd.read_csv(select_stk_code,encoding='gbk')
    df['hisCodeMinEndDate']=hisCodeMinEndDate
    df.to_csv(select_stk_code,encoding='gbk')
    return df

def selectOneStkCode(code):
    return selectStkCodeList([code])


def selectStkCodeList(codeList):
    if os.path.exists(select_stk_code):
        os.remove(select_stk_code)
    df=pd.read_csv(stk_code, encoding='gbk')    
    df=df[df['code'].isin(codeList)]
    name=(df['name'])
    df.to_csv(select_stk_code,index=False,encoding='gbk',date_format='str');
    return pd.read_csv(select_stk_code, encoding='gbk'),name
'''     

    
#selectStkCodeList(codeList)
def addStkCodesToFav(codeList):
    df=pd.read_csv(stk_code, encoding='gbk')
    df=df[df['code'].isin(codeList)]
    if df.size>1:
        if tt.isExist(fav_stk_code):
            #df.to_csv(fav_stk_code,index=False,encoding='gbk',date_format='str')
            #else:
            df0=tt.readDf(fav_stk_code)
            df=pd.concat([df0,df],ignore_index=True)
            df=df[df.duplicated()==False].sort_values(by='code')
        tt.saveDf(fav_stk_code, df)
        #df.to_csv(fav_stk_code,index=False,encoding='gbk',date_format='str')
        return df
    else:
        print('can not add this stk code')
        return

def removeStkFromFav(code):
    if tt.isExist(fav_stk_code):
        if code=='ALL':
            #os.remove(fav_stk_code)
            #tt.readDf(fav_stk_code)
            tt.remove(fav_stk_code)
        #df=pd.read_csv(fav_stk_code,encoding='gbk')
        df=tt.readDf(fav_stk_code)
        df0=df[df['code'].isin([code])]
        if df0.size>1:
            index=df0.index.values[0]
            df=df.drop(index)
            if df.size>1:
                #df.to_csv(fav_stk_code,encoding='gbk')
                tt.saveDf(fav_stk_code,df)
            else:
                #os.remove(fav_stk_code)
                tt.remove(fav_stk_code)
        

#addStkCodesToFav(['603999','603980'])
def getFavList():
    return tt.readDf(fav_stk_code)

'''
指数数据
'''
def getInxFromFile(filePath):
    #下载大盘指数文件，
    #filepath = 'data/inx_code.csv';
    qx=zw.zwDatX(zw._rdatCN);
    zwx.down_stk_inx(qx, filePath)
    
#getInxFromFile(stk_inx0)


'''
个股数据指定日期至今的日结数据
'''



#日数据
#传入周期，和文件路径
def getStkFromFile(StkSourcePath,startTime): 
   #自动下载，追加数据
   #-------设置参数       
    #股票代码文件 
    #filePath='./data/stk_code.csv';
    #startTime = '1994-01-01'
    qx = zw.zwDatX(zw._rdatCN)
    zwx.down_stk_all(qx,StkSourcePath,startTime)
    
#获取code从starttime起的日数据
def getStkDayDateToSelectFile(code,startTime):
    #readPath=os.path.join(dayDataPath,code+'.csv')
    #selectDF=selectOneStkCode(code,datastyle,date,cycle)
    selectDF,datastyle=initDatDateSelectFileWithCode(code,startTime)
    readPath=tt.joinPath(tt.dayDataDir,code+'.csv')
    if os.path.exists(readPath)==False:
        getStkFromFile(select_stk_code,startTime)
    else:
        #tdf=pd.read_csv(readPath,encoding='gbk')
        tdf=tt.readDf(readPath)
        sd=tt.str2dateYmd(startTime)
        ed=tt.today_Date
        fd=tt.str2dateYmd(tdf.tail(1)['date'].values[0])
        td=tt.str2dateYmd(tdf.head(1)['date'].values[0])
        if abs((fd-sd)/tt.one_Day_Delta)>=3 or ed>td:
            tt.remove(readPath)
            fd,td=sd,ed
            getStkFromFile(select_stk_code,startTime)
    tdf=tt.readDf(readPath)
    fromDate=tt.str2dateYmd(tdf.tail(1)['date'].values[0])+' '+tt.endTradeTime
    toDate=tt.str2dateYmd(tdf.head(1)['date'].values[0])+' '+tt.endTradeTime
    return readPath,tdf,fromDate,toDate,selectDF,datastyle
#getStkFromFile(stk_code,'2017-05-01')
#getStkFromFile(select_stk_code, '2010-04-01')
#当天tick数据数据并转换成分时数据
def getTodayTickAndCycle(StkSourcePath, cycles):
    qx = zw.zwDatX(zw._rdatTickReal)
    #qx.ksgns=cycles
    zwx.xtick_real_down_all(qx,StkSourcePath,cycles)
    
#getTodayTickAndCycle(stk_code, ['01','05','30'])
#getTodayTickAndCycle(select_stk_code,['01','05','30'])

def getStkCodeTodayTickData(code):
    selectDF=initRealTick
    readPath=tt.realTickPath
    readPath=tt.joinPath(readPath,code+'.csv')
    
'''
历史Tick数据
'''
def getPastTick(StkSourcePath,startDate,endDate):
    #testfinx='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/Base/stk_test.csv'
    #testfinx='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/Base/stk_code.csv'
    #qx = zw.zwDatX(zw._rdatMin)
    #qx.xday0k='2016-01-01'
    #qx.xday9k='2017-07-20'
    #qx.xdayNum=2
    #zwx.xtick_down8tim_all(qx, testfinx)
    qx = zw.zwDatX(zw._rdatMin)
    qx.xday0k=startDate
    qx.xday9k=endDate
    zwx.xtick_down8tim_all(qx, StkSourcePath)
    
#getPastTick(stk_code,'2015-01-03','2015-03-04')
#getPastTick(select_stk_code,'2015-01-03','2016-03-04')
#这个方法可以将任意tick数据转化成定制的
def transfToMinWithTick(tickSourceFile, outputMinDir, cycles):
    rsk=outputMinDir
    qx=zw.zwDatX()
    qx.code=tickSourceFile.split(os.path.sep)[-1].split('_')[1].split('.')[0]
    qx.min_ksgns=cycles
    zwx.xtick2tim100(qx,tickSourceFile)
    zwx.xtick2minWr(qx, rsk)
    


'''
tickSourceDir指定需要转换的历史tick数据父路径../TomQuantData/min/tick
outputMinDir转换完成以后传出到该文件目录，无需添加日期标记文件夹
date传入需要转换的日期data='yyyy-mm-dd'
cycle指定修改的周期列表
'''
def transToMinWithTickSourceDir(selectCodefile,tickSourceDir,outputMinDir,startdate,enddate,cycles):
    #date='2015-01-01'
    sdf=pd.read_csv(selectCodefile,encoding='gbk')
    selectCodes=sdf['code']
    #print[selectCodes]
    os.chdir(tickSourceDir)
    os.listdir()
    sd=dt.datetime.strptime(startdate, '%Y-%m-%d')
    #startdate=dt.datetime.strptime('2015-01-06', '%Y-%m-%d')
    ed=dt.datetime.strptime(enddate, '%Y-%m-%d')
    delta=dt.timedelta(days=1)
    while(sd<=ed):
        getYM=sd.strftime('%Y-%m')
        for d in os.listdir():
            if d == getYM:
                mouthDir=os.path.join(tickSourceDir,getYM)
                datestr=sd.strftime('%Y-%m-%d')
                for f in os.listdir(mouthDir):
                    if f.startswith(datestr):
                        for code in selectCodes:
                            if f.split('_')[1].split('.')[0]==str(code):
                                f=os.path.join(mouthDir, f)
                                #print(f)
                                outD=os.path.join(outputMinDir,datestr)
                                if not os.path.exists(outD):
                                    os.makedirs(outD)
                                transfToMinWithTick(f,outD,cycles)
        sd+=delta
    '''
    #转换完成以后才能合并所以不能合在一起
    for code in selectCodes:
        for cycle in cycles:
            mergeMinData(startdate,enddate,cycle,str(code))
    '''
#批量下载才允许合并
def mergeMinData(startdate,enddate,cycle,code):
    delta=dt.timedelta(days=1)
    sd=dt.datetime.strptime(startdate,'%Y-%m-%d')
    ed=dt.datetime.strptime(enddate,'%Y-%m-%d')
    df=pd.DataFrame()
    #cycle=1
    cycle='M'+'%02d' %int(cycle)
    code='%06d' %int(code)
    print(code)
    while(sd<=ed):
        datestr=dt.datetime.strftime(sd,'%Y-%m-%d')
        hisMinFilePath=os.path.join(outputMinDir,datestr,cycle,code+'.csv')
        print(hisMinFilePath)
        df0=pd.read_csv(hisMinFilePath, encoding='gbk')
        for i in range(df0.index.size):
            df0.at[i,'time']=datestr+' '+str(df0.loc[i,'time'])
        if df.size<5:
            df=df0
        else:
            df=pd.concat([df,df0],ignore_index=True)
        sd+=delta
    outputPath=os.path.join(hisCodeMinPath,cycle,code+'.csv')
    df.to_csv(outputPath, encoding='gbk')
    
    

#def mergeTwoTick
    #print(df)
#print(outputMinDir)
#transToMinWithTickSourceDir(select_stk_code,tickSourceDir,outputMinDir,'2015-01-06','2015-01-12',['01','30'])

#xstr = 'xxxx_123123'
#xstr =xstr.split('_')[1]

