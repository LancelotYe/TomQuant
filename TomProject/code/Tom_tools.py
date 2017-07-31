# -*- coding: utf-8 -*-
import os ,sys
import datetime as dt
import pandas as pd

def dateYmd2str(date):
    return dt.datetime.strftime(date,'%Y-%m-%d')
    
def str2dateYmd(dateStr):
    return dt.datetime.strptime(dateStr,'%Y-%m-%d')

def dateYmdHMS2str(date):
    return dt.datetime.strftime(date,'%Y-%m-%d %H:%M:%S')

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
    #TomMacBookAir   
    os.chdir('/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomProject/')
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
_rdatTickReal=joinPath(Tom_Quant_Date_Path, 'tickreal')
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

his_tick_sourceDir = joinPath(Tom_Quant_Date_Path, 'min', 'tick')



#sourcePath
dayDataDir=joinPath(_rdatCN,'day')
hisTickPath=joinPath(_rdatMin,'tick')
hisTickToMinPath=joinPath(_rdatMin)
realTickPath=joinPath(_rdatTickReal,'tick')
realTickToMinPath=joinPath(realTickPath)
#单只股票一段时间的历史分时数据（包含多天的），有hisTickToMin组装而来
hisCodeMinPath=os.path.join(_rdatMin)

tickSourceDir=joinPath(_rdatMin,'tick')
outputMinDir=joinPath(_rdatMin)

endTradeTime='15:00:00'

def readDf(path):
    if isExist(path):
        df=pd.read_csv(path,encoding='gbk')
        return df
    else:
        print('No such file')

def saveDf(filePath,df):
    df.to_csv(filePath,encoding='gbk')

def saveFileToDir(fileName,dirPath,df):
    if not isExist(dirPath):
        os.makedirs(dirPath)
    readPath=joinPath(dirPath,fileName)
    saveDf(readPath,df)

def remove(filePath):
    if isExist(filePath):
        os.remove(filePath)