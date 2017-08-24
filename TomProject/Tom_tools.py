# -*- coding: utf-8 -*-
import os ,sys
import datetime as dt
import pandas as pd

def dateYm2str(date):
    return dt.datetime.strftime(date,'%Y-%m')

def dateYmd2str(date):
    return dt.datetime.strftime(date,'%Y-%m-%d')

def dateYmdHMS2str(date):
    return dt.datetime.strftime(date,'%Y-%m-%d %H:%M:%S')
    
def str2dateYmd(dateStr):
    return dt.datetime.strptime(dateStr,'%Y-%m-%d')

def str2dateYmdHMS(dateStr):
    return dt.datetime.strptime(dateStr,'%Y-%m-%d %H:%M:%S')

one_Day_Delta=dt.timedelta(days=1)
today_Date=dt.datetime.now()
today_Date_Ymd_Str=dateYmd2str(today_Date)
today_Date_YmdHMS_Str=dateYmdHMS2str(today_Date)


def joinPath(*path):
    return os.path.join(*path)

def isExist(path):
    return os.path.exists(path)

def makeDirs(path):
    if not isExist(path):
        os.makedirs(path)
def gotoProjectPath():
    #tomMobileTank  
    #os.chdir('e:\\Users\\yjh19\\workspace\\TomQuant\\TomProject\\')
    #TomMacPro
    os.chdir('/Users/yejunhai/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomProject')
    #TomMacBookAir   
    #os.chdir('/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomProject/')
    #TomMacPro
    #os.chdir('/Users/yejunhai/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomProject/')    
    #print('[+]ProjectPath : '+ os.getcwd())
    return os.getcwd()

def getTomQuantDataPath():
    gotoProjectPath()
    os.chdir(os.pardir)
    rss=os.getcwd()
    rss=os.path.join(rss,'TomQuantData')
    if os.path.exists(rss)==False:
        os.makedirs(rss)
    return rss
def getBasePath():
    rss=getTomQuantDataPath()
    rss=os.path.join(rss,'Base')
    if os.path.exists(rss)==False:
        os.makedirs(rss)
    return rss

base_Path=getBasePath()
Tom_Quant_Date_Path=getTomQuantDataPath()
Tom_Project_Path=gotoProjectPath()

_rdat0=getTomQuantDataPath()
_rdatCN=joinPath(Tom_Quant_Date_Path,'cn')
_rdatUS=joinPath(Tom_Quant_Date_Path,'us')
_rdatInx=joinPath(Tom_Quant_Date_Path,'inx')
_rdatMin=joinPath(Tom_Quant_Date_Path,'min')
_rdatTick=joinPath(Tom_Quant_Date_Path,'tick')
_rdatTickReal=joinPath(Tom_Quant_Date_Path,'tickreal')
_rdatZW=joinPath(Tom_Quant_Date_Path,'zw')
_rTmp=joinPath(Tom_Quant_Date_Path,'demo','tmp')



stk_inx0 = joinPath(base_Path, 'stk_inx0.csv')
stk_base = joinPath(base_Path, 'stk_base.csv')
stk_code = joinPath(base_Path, 'stk_code.csv')
stk_sz50 = joinPath(base_Path, 'stk_sz50.csv')
stk_hs300 = joinPath(base_Path, 'stk_hs300.csv')
stk_zz500 = joinPath(base_Path, 'stk_zz500.csv')

select_stk_code = joinPath(base_Path,'select_stk_code.csv')
fav_stk_code = joinPath(base_Path,'fav_stk_code.csv')

#his_tick_sourceDir = joinPath(Tom_Quant_Date_Path, 'min', 'tick')



#sourcePath
dayDataDir=joinPath(_rdatCN,'day')


realTickPath=joinPath(_rdatCN,'realTick')
realTickToMinPath=joinPath(realTickPath)
#单只股票一段时间的历史分时数据（包含多天的），有hisTickToMin组装而来
hisCodeMinPath=os.path.join(_rdatCN,'hisTickToMinMerge')

tickSourceDir=joinPath(_rdatMin,'tick')

#hisTickPath=joinPath(_rdatMin,'tick')
hisTickPath=his_tick_sourceDir=joinPath(_rdatCN,'hisTick')
hisTickToMinPath=joinPath(_rdatCN,'hisTickToMin')
outputMinDir=joinPath(_rdatCN,'hisTickToMin')

endTradeTime='15:00:00'

def readDf(path):
    if isExist(path):
        df=pd.read_csv(path,encoding='gbk')
        return df
    else:
        print('No such file')

def saveDf(filePath,df):
    df.to_csv(filePath,encoding='gbk')
    
def saveDFNoIndex(filePath,df):
    df.to_csv(filePath,encoding='gbk',index=False)

def saveFileToDir(fileName,dirPath,df):
    if not isExist(dirPath):
        os.makedirs(dirPath)
    readPath=joinPath(dirPath,fileName)
    saveDf(readPath,df)

def remove(filePath):
    if isExist(filePath):
        os.remove(filePath)
        
'''
选取自定义股票
'''
data_style=['dayData','hisTick','hisTickToMin','realTick','realTickToMin']
def initDatDateSelectFileWithCode(code,date):
    datastyle='dayData'
    if not isExist(select_stk_code):
        selectOneStkCode(code,datastyle,date,'05')
    else:
        selectOtherCode(code)
        selectOtherDate(date)
        selectCodeOtherDatastyle(datastyle)
    return getSelectList(),datastyle
def initRealTickSelectFileWithCode(code):
    datastyle='realTick'
    if not isExist(select_stk_code):
        selectOneStkCode(code,datastyle,today_Date_Ymd_Str,'01')
    else:
        selectOtherCode(code)
        selectCodeOtherDatastyle(datastyle)
        selectCodeOtherCycle('01')
    return getSelectList(), datastyle
def initRealTickToMinSelectFileWithCode(code,cycle):
    datastyle='realTickToMin'
    if not isExist(select_stk_code):
        selectOneStkCode(code,datastyle,today_Date_Ymd_Str,cycle)
    else:
        selectOtherCode(code)
        selectCodeOtherDatastyle(datastyle)
        selectCodeOtherCycle(cycle)
    return getSelectList(),datastyle
#只获取date日的Tick数据
def initHisTickSelectFileWithCode(code,date):
    datastyle='hisTick'
    if not isExist(select_stk_code):
        selectOneStkCode(code,datastyle,date,'05')
    else:
        selectOtherCode(code)
        selectOtherDate(date)
        selectCodeOtherDatastyle(datastyle)
    return getSelectList(),datastyle
def initHisTickToMinSelectFileWithCode(code,date,cycle):
    datastyle='hisTickToMin'
    if not isExist(select_stk_code):
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
    remove(select_stk_code)
    df=readDf(stk_code)
    code=int(code)
    df=df[df['code'].isin([code])]
    if df.size==0:
        print('No Such Code')
        return
    df=pd.concat([df],ignore_index=True,)
    df['datastyle']=datastyle
    df['date']=date
    df['cycle']=cycle
    #df['hisCodeMinEndDate']=hisCodeMinEndDate
    saveDFNoIndex(select_stk_code,df)
    #df.to_csv(select_stk_code,index=False,encoding='gbk',date_format='str');
    return getSelectList()
def selectNextCodeInStkCode():
    df=readDf(stk_code)
    #sdf=tt.readDf(tt.select_stk_code)
    sdf=getSelectList()
    index=df[df['code']==sdf['code'][0]].index.values[0]
    index+=1
    if index==df.index.size:
        index=0
    code=df.loc[index,'code']
    datastyle=sdf.loc[0,'datastyle']
    date=sdf.loc[0,'date']
    cycle='%02d'%sdf.loc[0,'cycle']
    return selectOneStkCode(code,datastyle,date,cycle)
def selectOtherCode(code):
    df=getSelectList()
    datastyle=df.loc[0,'datastyle']
    date=df.loc[0,'date']
    cycle='%02d'%df.loc[0,'cycle']
    return selectOneStkCode(code,datastyle,date,cycle)
def selectCodeAddDate(xday):
    df=getSelectList()
    date=df['date'].values[0]
    #date=dt.datetime.strptime(date,'%Y-%m-%d')
    date=str2dateYmd(date)
    date+=xday*one_Day_Delta
    #date=dt.datetime.strftime(date,'%Y-%m-%d')
    date=dateYmd2str(date)
    df['date']=date
    saveDFNoIndex(select_stk_code,df)
    return df
def selectOtherDate(date):
    df=getSelectList()
    df['date']=date
    saveDFNoIndex(select_stk_code,df)
    return df
def selectCodeNextDatastyle():
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
    saveDFNoIndex(select_stk_code,df)
    return df
def selectCodeOtherDatastyle(datastyle):
    df=getSelectList()
    df['datastyle']=datastyle
    saveDFNoIndex(select_stk_code,df)
def selectCodeOtherCycle(cycle):
    df=getSelectList()
    df['cycle']=cycle
    saveDFNoIndex(select_stk_code,df)
    return df
def getSelectList():
    return readDf(select_stk_code)

#selectStkCodeList(codeList)
def addStkCodesToFav(codeList):
    df=readDf(stk_code)
    df=df[df['code'].isin(codeList)]
    
    if df.size>1:
        if isExist(fav_stk_code):
            df0=readDf(fav_stk_code)
            df=pd.concat([df0,df],ignore_index=True)
            df=df[df.duplicated()==False].sort_values(by='code')
        saveDFNoIndex(fav_stk_code,df)
        #df.to_csv(fav_stk_code,index=False,encoding='gbk',date_format='str')
        return df
    else:
        print('can not add this stk code')
        return

def removeStkFromFav(code):
    if isExist(fav_stk_code):
        if code=='ALL':
            #os.remove(fav_stk_code)
            #tt.readDf(fav_stk_code)
            remove(fav_stk_code)
            return
        #df=pd.read_csv(fav_stk_code,encoding='gbk')
        df=readDf(fav_stk_code)
        df0=df[df['code'].isin([code])]
        if df0.size>1:
            index=df0.index.values[0]
            df=df.drop(index)
            if df.size>1:
                #df.to_csv(fav_stk_code,encoding='gbk')
                saveDFNoIndex(fav_stk_code,df)
            else:
                #os.remove(fav_stk_code)
                remove(fav_stk_code)
        

#addStkCodesToFav(['603999','603980'])
def getFavList():
    return readDf(fav_stk_code)