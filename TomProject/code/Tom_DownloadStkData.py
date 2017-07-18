# -*- coding: utf-8 -*-


import os,sys
import numpy as np
import pandas as pd
import tushare as ts

#  zwQuant
import zwSys as zw  
import zwQTBox as zwx
import zwTools as zwt

#import Tom_Prefix as tp



path = sys.path[0]
path = os.path.abspath('test')



#下载基础文件
#
'''
base 文件路径
'''
rss = zw.getBasePath()
stk_inx0 = os.path.join(rss, 'stk_inx0.csv')
stk_base = os.path.join(rss, 'stk_base.csv')
stk_code = os.path.join(rss, 'stk_code.csv')
stk_sz50 = os.path.join(rss, 'stk_sz50.csv')
stk_hs300 = os.path.join(rss, 'stk_hs300.csv')
stk_zz500 = os.path.join(rss, 'stk_zz500.csv')



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
    
    d20=d20.sort(columns='code')
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

#传入周期，和文件路径
def downStkFromFile(StkSourcePath, cycle, startTime): 

   #自动下载，追加数据
   #-------设置参数       
    #股票代码文件 
    #filePath='./data/stk_code.csv';
    #startTime = '1994-01-01'
    qx = zw.zwDatX(zw._rdatCN)
    zwx.down_stk_all(qx,StkSourcePath,startTime)
    
    
    
def downInxFromFile(filePath, cycle):
    #下载大盘指数文件，
    #filepath = 'data/inx_code.csv';
    qx=zw.zwDatX(zw._rdatCN);
    zwx.down_stk_inx(qx, filePath)
    



#当天分时数据
def downTodayStkData():
    qx = zw.zwDatX(zw._rdatTickReal)
    zwx.xtick_real_down_all(qx,stk_code)
    
downBase()

downStkFromFile(stk_code,'day', '2015-01-01')
