# -*- coding: utf-8 -*-


import os,sys
import numpy as np
import pandas as pd
import tushare as ts

#  zwQuant
import zwSys as zw  
import zwQTBox as zwx
import zwTools as zwt



path = sys.path[0]
path = os.path.abspath('Tom_Download')



'''
目录结构
zwDat/
    基础数据包
    base/
    中国
    cn/
        日
        day/
    美国
    ua/
        日
        day/
'''
#下载基础文件
#

def gotoPath(absPath):
  os.chdir(absPath)
  print('[+]CurrentPath:'+ os.getcwd())
  
gotoPath('e:\\Users\\yjh19\\workspace\\TomQuant\\TomProject')
def downBase():        
    '''
    下载时基本参数数据时，有时会出现错误提升：
          timeout: timed out
          属于正常现象，是因为网络问题，等几分钟，再次运行几次 
    '''
    os.getcwd()
    #rss=os.path.join(os.pardir,'zwDat','base')
    rss=zw._rdat0
    rss=os.path.join(rss,'base')
    print(rss)
    if os.path.exists(rss)==False:
      os.makedirs(rss) 
    stk_inx0 = 'stk_inx0.csv'
    stk_base = 'stk_base.csv'
    stk_code = 'stk_code.csv'
    stk_sz50 = 'stk_sz50.csv'
    stk_hs300 = 'stk_hs300.csv'
    stk_zz500 = 'stk_zz500.csv'
    #print(rss)
    #rss="../zwDat/base/"
    #
    #fss=rss+'stk_inx0.csv';print(fss);
    #stk_inx0 = 'stk_inx0.csv'
    fss = os.path.join(rss, stk_inx0)
    print(fss);
    dat = ts.get_index()
    dat.to_csv(fss,index=False,encoding='gbk',date_format='str');

    #=========
    #fss=rss+'stk_base.csv';print(fss);
    #stk_base = 'stk_base.csv'
    fss = os.path.join(rss,stk_base)
    print(fss);
    dat = ts.get_stock_basics();
    dat.to_csv(fss,encoding='gbk',date_format='str');
    
    c20=['code','name','industry','area'];
    d20=dat.loc[:,c20]
    d20['code']=d20.index;
    
    #stk_code = 'stk_code.csv'
    #fss=rss+'stk_code.csv';print(fss);
    fss=os.path.join(rss, stk_code)
    print(fss)
    d20.to_csv(fss,index=False,encoding='gbk',date_format='str');
    
    #sz50,上证50；hs300,沪深300；zz500，中证500
    #stk_sz50 = 'stk_sz50.csv'
    #fss=rss+'stk_sz50.csv';print(fss);
    fss=os.path.join(rss, stk_sz50)
    print(fss)
    dat=ts.get_sz50s();
    if len(dat)>3:
        dat.to_csv(fss,index=False,encoding='gbk',date_format='str');
    
    #stk_hs300 = 'stk_hs300.csv'
    #fss=rss+'stk_hs300.csv';print(fss);
    fss = os.path.join(rss, stk_hs300)
    print(fss)
    dat=ts.get_hs300s();
    if len(dat)>3:
        dat.to_csv(fss,index=False,encoding='gbk',date_format='str');
    
    #stk_zz500 = 'stk_zz500.csv'
    #fss=rss+'stk_zz500.csv';print(fss);
    fss=os.path.join(rss,stk_zz500)
    print(fss)
    dat=ts.get_zz500s();
    if len(dat)>3:
        dat.to_csv(fss,index=False,encoding='gbk',date_format='str');

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
    

downBase()

#downStkFromFile()


 
