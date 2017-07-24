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
codeList = [600129, 600192, 600231,600192]

def selectStkCodeList(codeList):
    if os.path.exists(select_stk_code):
        os.remove(select_stk_code)
    df=pd.read_csv(stk_code, encoding='gbk')    
    df=df[df['code'].isin(codeList)]
    df.to_csv(select_stk_code,index=False,encoding='gbk',date_format='str');
    
        
#selectStkCodeList(codeList)

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
    
    
#getStkFromFile(stk_code,'2017-05-01')
#getStkFromFile(select_stk_code, '2017-05-01')

#当天分时数据
def getTodayTickAndCycle(StkSourcePath, cycles):
    qx = zw.zwDatX(zw._rdatTickReal)
    #qx.ksgns=cycles
    zwx.xtick_real_down_all(qx,StkSourcePath,cycles)
    
#getTodayTickAndCycle(stk_code, ['01','05','30'])
#getTodayTickAndCycle(select_stk_code,['01','05','30'])
'''
历史分时数据
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
    #fdat='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/tick/2016-05/2016-05-03/000001.csv'
    
    #fdat = tickSourceFile
    tickSourceFile = '/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/min/tick/2015-01/2015-01-06_600192.csv'
    #rsk='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/tick/2016-05/2016-05-03/'
    #qx.code='000001'
    #qx.min_ksgns=['01']
    rsk=outputMinDir
    qx=zw.zwDatX()
    
    qx.code=tickSourceFile.split(os.path.sep)[-1].split('_')[1].split('.')[0]
    #df=pd.read_csv(select_stk_code,encoding='gbk')
    #df=pd.read_csv(tickSourceFile,encoding='gbk')
    #codeList=df['code']
    #for code in codeList:
        #qx.code=code
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
    selectCodes=pd.read_csv(selectCodefile,encoding='gbk')['code']
    os.chdir(tickSourceDir)
    os.listdir()
    startdate=dt.datetime.strptime(startdate, '%Y-%m-%d')
    startdate=dt.datetime.strptime('2015-01-06', '%Y-%m-%d')
    enddate=dt.datetime.strptime(enddate, '%Y-%m-%d')
    delta=dt.timedelta(days=1)
    while(startdate<=enddate):
        getYM=startdate.strftime('%Y-%m')
        for d in os.listdir():
            if d == getYM:
                mouthDir=os.path.join(tickSourceDir,getYM)
                datestr=startdate.strftime('%Y-%m-%d')
                for f in os.listdir(mouthDir):
                    if f.startswith(datestr):
                        for code in selectCodes:
                            if f.split('_')[1].split('.')[0]==str(code):
                                f=os.path.join(mouthDir, f)
                                print(f)
                                outD=os.path.join(outputMinDir,datestr)
                                if not os.path.exists(outD):
                                    os.makedirs(outD)
                                    transfToMinWithTick(f,outD,cycles)
        startdate+=delta
                    

print(outputMinDir)
#transToMinWithTickSourceDir(select_stk_code,tickSourceDir,outputMinDir,'2015-01-06','2015-01-12',['01','30'])

#xstr = 'xxxx_123123'
#xstr =xstr.split('_')[1]

