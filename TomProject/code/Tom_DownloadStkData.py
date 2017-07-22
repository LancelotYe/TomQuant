# -*- coding: utf-8 -*-


import os,sys
import numpy as np
import pandas as pd
import tushare as ts

#  zwQuant
import zwSys as zw  
import zwQTBox as zwx
import zwTools as zwt

import tushare as ts
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
codeList = [600129, 600192, 600231]

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
个股数据
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
#当天分时数据
def getTodayTickAndCycle(StkSourcePath, cycles):
    qx = zw.zwDatX(zw._rdatTickReal)
    #qx.ksgns=cycles
    zwx.xtick_real_down_all(qx,StkSourcePath,cycles)
    
#getTodayTickAndCycle(stk_code, ['01','05','30'])
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
#这个方法可以将任意tick数据转化成定制的
def transfToMinWithTick(tickSourceFile, outputMinDir, cycles):
    #fdat='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/tick/2016-05/2016-05-03/000001.csv'
    fdat = tickSourceFile
    #rsk='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/tick/2016-05/2016-05-03/'
    #qx.code='000001'
    #qx.min_ksgns=['01']
    rsk=outputMinDir
    qx=zw.zwDatX()
    #df=pd.read_csv(select_stk_code,encoding='gbk')
    df=pd.read_csv(tickSourceFile,encoding='gbk')
    codeList=df['code']
    for code in codeList:
        qx.code=code
        qx.min_ksgns=cycles
        zwx.xtick2tim100(qx,fdat)
        zwx.xtick2minWr(qx, rsk)
    
def transfToMinWithTickList(tickSourceFileList, outputMinDir, cycles):
    for file in tickSourceFileList:
        transfToMinWithTick(file, outputMinDir, cycles)
        



