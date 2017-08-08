# -*- coding: utf-8 -*-

import sys,os
import tushare as ts
import pandas as pd


#----------
def zw_stk_down_base():        
    '''
    下载时基本参数数据时，有时会出现错误提升：
          timeout: timed out
          属于正常现象，是因为网络问题，等几分钟，再次运行几次 
          '''
    rss="tmp/"
    #
    fss=rss+'stk_inx0.csv';print(fss);
    dat = ts.get_index()
    dat.to_csv(fss,index=False,encoding='gbk',date_format='str');

    #=========
    fss=rss+'stk_base.csv';print(fss);
    dat = ts.get_stock_basics();
    dat.to_csv(fss,encoding='gbk',date_format='str');
    
    c20=['code','name','industry','area'];
    d20=dat.loc[:,c20]
    d20['code']=d20.index;
    
    fss=rss+'stk_code.csv';print(fss);
    d20.to_csv(fss,index=False,encoding='gbk',date_format='str');
    
    #sz50,上证50；hs300,沪深300；zz500，中证500
    fss=rss+'stk_sz50.csv';print(fss);
    dat=ts.get_sz50s();
    if len(dat)>3:
        dat.to_csv(fss,index=False,encoding='gbk',date_format='str');
    
    fss=rss+'stk_hs300.csv';print(fss);
    dat=ts.get_hs300s();
    if len(dat)>3:
        dat.to_csv(fss,index=False,encoding='gbk',date_format='str');

    fss=rss+'stk_zz500.csv';print(fss);
    dat=ts.get_zz500s();
    if len(dat)>3:
        dat.to_csv(fss,index=False,encoding='gbk',date_format='str');
    
       
 
#----------
zw_stk_down_base()
