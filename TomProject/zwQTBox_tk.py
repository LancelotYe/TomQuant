# -*- coding: utf-8 -*- 
'''
  
  zwQuantToolBox 2016
  zw量化开源工具箱系列软件 
  http://www.ziwang.com,Python量化第一品牌 
  
  文件名:zwQTBox.py
  说明：import zwQTBox as zwx
  常用zwQuant量化工具函数集
  

'''

import sys,os
import numpy as np
import tushare as ts
import pandas as pd
import pandas_datareader.data as web

import matplotlib as mpl
from matplotlib import pyplot as plt
from numba import *

import csv
import pickle
from datetime import * 
from dateutil.parser import parse
from dateutil import rrule
import datetime as dt

import zwSys as zw  #::zwQT
import zwTools as zwt


#-------------
def xtick_down200(qx):
    ''' 
         根据股票代码，时间，下载tick分笔数据，并保存到tick目录下
     中国A股,tick 历史或real实时 tick 分笔数据下载子程序
        会自动将中文type，替换成 英文：中性盘：norm；买盘：buy; 卖盘：sell
         
     【输入】
         xcod,股票代码
         xtim，日期字符串，载的是当天 实时 tick数据
     【输出】
        df,股票 tick  数据
            数据列格式：
            time,price,change,volume,amount,type
            输出目录:\zwdat\tick\code\xtim ，code，xtim根据各个股票不同而变化
            '''
    fss=qx.rdat+qx.code+'\\'+qx.xtim+'.csv'
    xfg=os.path.exists(fss);
    if not xfg:
        df = ts.get_tick_data(qx.code,date=qx.xtim)
        dn=len(xd);#  print('n',dn) # 跳过无数据 日期
        if dn>10:  
            df['type']=df['type'].str.replace(u'中性盘', 'norm');
            df['type']=df['type'].str.replace(u'买盘', 'buy');
            df['type']=df['type'].str.replace(u'卖盘', 'sell');
            df.to_csv(fss,index=False,encoding='utf') 

#-------------xtick tick分笔数据下载
  
def xtick_setTimeDat(qx):
    '''
    设置分时数据下载和转换的初始参数
    根据股票代码，对应的M05，5分钟分时数据。确定上一次下载的最后后期，进行追加
    如果没有数据，默认初始日期是：qx.xday0k   2005-01-01    
    输入：
       qx.code，股票代码
    输出： 
        qx.xday0，起始下载日期
    
    '''
    for ksgn0 in qx.min_ksgns: #qx.min_ksgns=['M05','M15','M30','M60']
        ksgn='M'+ksgn0;
        fss=zw._rdatMin+ksgn+'\\'+qx.code+'.csv'
        xfg=os.path.exists(fss);    #print('@xf',xfg,xday,fss,xcod,xtim)
        if xfg:
            df=pd.read_csv(fss,index_col=False,encoding='utf') 
            df=df.sort_values(by=['time'],ascending=False)
            qx.datMin[ksgn]=df
        else:
            qx.datMin[ksgn]=pd.DataFrame(columns=zw.qxMinName);        
    #    
    if len(qx.datMin['M05'])>0:
        df=qx.datMin['M05'];x0=df.iloc[0];
        s2=x0['time'];xtim0=s2.split(' ')[0]
    else:xtim0=qx.xday0k   #\2005-01-01    
    #xday9,xday9k
    qx.xday0=xtim0
    #print('tim0',xtim0)
    
def xtick_downsub(xcod,xtim):
    ''' 中国A股,tick 历史或real实时 tick 分笔数据下载子程序
        会自动将中文type，替换成 英文：中性盘：norm；买盘：buy; 卖盘：sell
        
    【输入】
        xcod,股票代码
        xtim，日期字符串，当xtim为空时，下载的是当天 实时 tick数据
    【输出】
        df,股票 tick  数据
            数据列格式：
            time,price,change,volume,amount,type
    '''
    
    if xtim=='':
        xd = ts.get_today_ticks(xcod)
    else: 
        xd = ts.get_tick_data(xcod,date=xtim)
    
    dn=len(xd);#  print('n',dn)
    # 跳过无数据 日期
    if dn>10:  
        xd['type']=xd['type'].str.replace(u'中性盘', 'norm');
        xd['type']=xd['type'].str.replace(u'买盘', 'buy');
        xd['type']=xd['type'].str.replace(u'卖盘', 'sell');
        #xd.to_csv('tmp\\'+xcod+'_'+xtim+'.csv',index=False,encoding='utf') 
    else:
        xd=[]
    #
    return xd
  
             
def xtick_t2minsub(df):
    '''
    tick 数据 转换值程序，
    对根据qx.minType切割的数据，进行汇总，
    tick 数据 转换为分时数据：5/15/30/60 分钟
    输入
        df，根据qx.minType切割的数据
    输出
        ds，汇总后的数据，注意，格式是：pd.Series
    '''
    ds=pd.Series(index=zw.qxMinName)
    x9=df.iloc[-1];ds['open']=x9['price']
    x0=df.iloc[0];ds['close']=x0['price']
    #
    ds['high'],ds['low']=np.max(df['price']),np.min(df['price'])        
    ds['volume'],ds['amount']=np.sum(df['volume']),np.sum(df['amount'])    
    #
    xlst=['norm','buy','sell']
    for xsgn in xlst:
        df2=df[df['type']==xsgn]
        if len(df2>0):
            ds['vol_'+xsgn],ds['amo_'+xsgn]=np.sum(df2['volume']),np.sum(df2['amount'])    
        else:
            ds['vol_'+xsgn],ds['amo_'+xsgn]=0,0
    #
    return ds    
  
        
def xtick_t2min(qx,sgnMin):
    '''
       将下载的tick分笔数据，转换为分时数据：5/15/30/60 分钟
       并且追加到对应的分时数据列表当中
       注意qx.xtimTick0,qx.xtimTick9是预设时间数据，在zwDatX类定义并初始化
       输入
           sgnMin，分时数据符号
           qx.minTyp，分时数据间隔数据
           
    '''
    
    wrkDTim0,dt9=parse(qx.xtimTick0),parse(qx.xtimTick9)
    xt=dt9-wrkDTim0;numMin=xt.total_seconds()/60
    xn9=int(numMin/qx.minType)+1;     #print(wrkDTim0,xn9); #xn9=7
    for tc in range(xn9):
        wrkDTim9=wrkDTim0+dt.timedelta(minutes=qx.minType) 
        strTim0,strTim9=wrkDTim0.strftime('%H:%M:%S'),wrkDTim9.strftime('%H:%M:%S')
        #---cut tick.dat by tim
        df=qx.datTick;#print(df.head())
        df2=df[df['time']<strTim9]
        df3=df2[df2['time']>=strTim0]
        if len(df3)>0:
            #-----tick 数据 转换为分时数据：5/15/30/60 分钟
            ds=xtick_t2minsub(df3)
            ds['time']=qx.xtim+' '+strTim0
            qx.datMin[sgnMin]=qx.datMin[sgnMin].append(ds.T,ignore_index=True)
        #----ok,#tc
        wrkDTim0=wrkDTim9
    #
    #
    #
    #print('\n x2min ok')

def xtick_xminWr(qx):
    '''
    把所有分时数据，保存到文件
    会自动去重
    对应的数据目录 \zwdat\min\
        输出数据在min目录对应的分时目录当中，已经自动转换为5,15,30,60分钟分时数据
    
    '''
    print(qx.min_ksgns)
    for ksgn0 in qx.min_ksgns:
        sgnMin='M'+ksgn0;
        xdf=qx.datMin[sgnMin]    
        xdf.drop_duplicates(subset='time', keep='last', inplace=True);
        xdf=np.round(xdf,2)
        xdf=xdf.sort_values(by=['time'],ascending=False)
        fss=qx.rdat+sgnMin+'\\'+qx.code+'.csv';print(fss)
        xdf.to_csv(fss,columns=zw.qxMinName,index=False,encoding='utf') 
        qx.datMin[sgnMin]=xdf
    
def xtick_down100(qx):
    '''
    根据股票代码，时间，下载tick分笔数据，并转换为对应的分时数据：5/15/30/60 分钟
    
    '''
    df=xtick_downsub(qx.code,qx.xtim)
    if len(df)>10:
        #print(len(df),qx.fn_tick,'\n',df.head())
        qx.datTick=df
        for ksgn0 in qx.min_ksgns: #qx.min_ksgns=['M05','M15','M30','M60']
            sgnMin='M'+ksgn0;qx.minType=int(ksgn0);       # print('@mt',qx.minType)
            xtick_t2min(qx,sgnMin)    
#----    
        
def xtick_down_all_time(qx):
    '''
    下载制定股票代码的所有tick历史分笔数据
    并转换成对应的分时数据：5/15/30/60 分钟
    数据文件保存在：对应的数据目录 \zwdat\min\
    [输入]
      qx.code，股票代码
    '''
    xtick_setTimeDat(qx)
    # xday9k#
    qx.DTxtim0,qx.DTxtim9=parse(qx.xday0),dt.datetime.now();
    nday=rrule.rrule(rrule.DAILY,dtstart=qx.DTxtim0,until=qx.DTxtim9).count()
    #print('@t',nday,qx.DTxtim0,'@',qx.DTxtim9);   #nday=13;
    kc=0
    for tc in range(nday):
        qx.DTxtim=qx.DTxtim0+dt.timedelta(days=tc) 
        qx.xtim=qx.DTxtim.strftime('%Y-%m-%d'); print(tc,'tc',kc,qx.xtim,qx.code)
        #
        xtick_down100(qx)
        kc+=1;
        if kc>100:
            kc=0
            xtick_xminWr(qx)
            
        #qx.datLib.to_csv(qx.fn_dat,index=False,encoding='utf') #
    #----#tc,cod#1
    if kc>0:
        xtick_xminWr(qx)
    #if kc>0:qx.datLib.to_csv(qx.fn_dat,index=False,encoding='utf') #

        
def xtick_down_all(qx,finx):
    '''
       下载finx股票列表，所有股票的历史tick分笔数据
       并转换成对应的分时数据：5/15/30/60 分钟
       数据文件保存在：对应的数据目录 \zwdat\min\
    输入：
        finx，股票目录索引文件，一般每个股票，下载需要2-3分钟，
            单机股票代码不要太多，可以分组在多台电脑运行
    输出
        \zwdat\min\
        输出数据在min目录对应的分时目录当中，已经自动转换为5,15,30,60分钟分时数据
        为当天最新实时分笔数据，会自动覆盖以前的就数据
    '''
    #fss=qx.rdatInx+'stk_code.csv';print(fss);
    qx.rdat=zw._rdatMin;print('finx',finx);
    dinx = pd.read_csv(finx,encoding='gbk') 
    i,xn9=0,len(dinx['code']);
    for xc in dinx['code']:
        code="%06d" %xc
        #code=zwTools.v2sk(xc,6);
        print("\n",i,"/",xn9,"code,",code)
        #---
        qx.code=code;
        xtick_down_all_time(qx)
        i+=1;qx.codeCnt=i
#----------------------
def xtick2_down_all(qx,finx):
    '''
       下载finx股票列表，所有股票的历史tick分笔数据
       并转换成对应的分时数据：5/15/30/60 分钟
       数据文件保存在：对应的数据目录 \zwdat\min\
    输入：
        finx，股票目录索引文件，一般每个股票，下载需要2-3分钟，
            单机股票代码不要太多，可以分组在多台电脑运行
    输出
        \zwdat\min\
        输出数据在min目录对应的分时目录当中，已经自动转换为5,15,30,60分钟分时数据
        为当天最新实时分笔数据，会自动覆盖以前的就数据
        ---
        fss=zw._rdatMin+ksgn+'\\'+qx.code+'.csv'
        xfg=os.path.exists(fss);  
    '''
    #fss=qx.rdatInx+'stk_code.csv';print(fss);
    qx.rdat=zw._rdatTick;print('finx',finx);
    dinx = pd.read_csv(finx,encoding='gbk') 
    i,xn9=0,len(dinx['code']);
    for xc in dinx['code']:
        code="%06d" %xc
        #code=zwTools.v2sk(xc,6);
        print("\n",i,"/",xn9,"code,",code)
        rss,qx.code=qx.rdat+code+'\\',code
        xfg=os.path.exists(rss);  
        print(xfg,rss)
        #---
        if not xfg:
            os.mkdir(rss)
        #xtick2_down_all_time(qx)
        #i+=1;qx.codeCnt=i       
#---------------------
    
def xtick_down_all_real(qx,finx):
    '''
    下载当天的实时tick分笔数据
    输入：
        finx，股票目录索引文件，一般每个股票，下载需要2-3分钟，
            单机股票代码不要太多，可以分组在多台电脑运行
    输出
        \zwdat\tick\
        输出数据在tick目录对应的分时目录当中，已经自动转换为5,15,30,60分钟分时数据
        为当天最新实时分笔数据，会自动覆盖以前的就数据
    '''
    #fss=qx.rdatInx+'stk_code.csv';
    qx.rdat=zw._rdatTick;print('finx',finx);
    dinx = pd.read_csv(finx,encoding='gbk');
    i,xn9=0,len(dinx['code']);
    for xc in dinx['code']:
        i+=1;qx.codeCnt=i
        code="%06d" %xc
        #code=zwTools.v2sk(xc,6);
        print("\n",i,"/",xn9,"code,",code)
        #---
        qx.code=code;
        #xtick_down_all_time(qx)
        df=xtick_downsub(code,'')
        if len(df)>10:
            #print(len(df),qx.fn_tick,'\n',df.head())
            fss=qx.rdat+'tick\\'+qx.code+'.csv';print('\n',fss)
            df.to_csv(fss,index=False,encoding='utf') 
            qx.datTick=df
            #---------- tick 分笔数据，转换为分时数据：05,15,30,60
            for ksgn0 in qx.min_ksgns: #qx.min_ksgns=['M05','M15','M30','M60']
                sgnMin='M'+ksgn0;qx.minType=int(ksgn0);       # print('@mt',qx.minType)
                qx.datMin[sgnMin]=pd.DataFrame(columns=zw.qxMinName);        
                xtick_t2min(qx,sgnMin)   

#----------------down.stk

def down_stk_cn020inx(qx,xtim0):
    ''' 下载大盘指数数据,简版股票数据，可下载到1994年股市开市起
    【输入】
        qx.xcod:指数代码

    '''
    xcod=qx.code;tim0=xtim0;#tim0='1994-01-01'
    xd=[];rss=qx.rXDay;fss=rss+xcod+'.csv';
    #if ((xtyp!='D')and(xtyp!='9') ):    tim0=tim0+" 00:00:00";
        
    #-------------------
    xfg=os.path.exists(fss);xd0=[];
    if xfg:
        xd0= pd.read_csv(fss,index_col=0,parse_dates=[0],encoding='gbk') 
        #print(xd0.head())
        xd0=xd0.sort_index(ascending=False);
        #tim0=xd0.index[0];
        _xt=xd0.index[0];#xt=xd0.index[-1];###
        s2=str(_xt);tim0=s2.split(" ")[0]
    
    #    
    print('\n',xfg,fss,",",tim0);   
    #-----------    
    try:
        xd=ts.get_h_data(xcod,start=tim0,index=True,end=None,retry_count=5,pause=1)     #Day9        
        #-------------
        if xd is not None:
            if (len(xd0)>0):         
                xd2 =xd0.append(xd)                
                #  flt.dup 
                xd2["index"]=xd2.index
                xd2.drop_duplicates(subset='index', keep='last', inplace=True);
                del(xd2["index"]);
                #xd2.index=pd.to_datetime(xd2.index)
                xd=xd2;
                
            xd=xd.sort_index(ascending=False);            
            xd=np.round(xd,3);
            xd.to_csv(fss,encoding='gbk')
    except IOError: 
        pass    #skip,error
    
           
    return xd      
    
def down_stk_cn010(qx,xtyp="D"):
    ''' 中国A股数据下载子程序
    【输入】
        qx (zwDatX): 
        xtyp (str)：数据类型，9,Day9,简版股票数据，可下载到2001年，其他的全部是扩充版数据，只可下载近3年数据
            D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
    :ivar xcod (int): 股票代码
    :ivar fss (str): 保存数据文件名
    '''
    
    xcod=qx.code;xd=[];tim0='2012-01-01';
    if (xtyp=='0'):    
        rss=qx.rDay
        tim0='1994-01-01'  #2000-01-01
    elif (xtyp=='D'):    
        rss=qx.rDay9            
    elif (xtyp=='T'):    
        rss=qx.rTmp;
    
    elif (xtyp=='5'):  
        rss=qx.rM05
    elif (xtyp=='15'):        
        rss=qx.rM15
    elif (xtyp=='30'):        
        rss=qx.rM30
    elif (xtyp=='60'):        
        rss=qx.rM60;
    
    fss=rss+xcod+'.csv'
    #if ((xtyp!='D')and(xtyp!='9') ):    tim0=tim0+" 00:00:00";
        
    #-------------------
    xfg=os.path.exists(fss);xd0=[];
    if xfg:
        xd0= pd.read_csv(fss,index_col=0,parse_dates=[0],encoding='gbk') 
        #print(xd0.head())
        xd0=xd0.sort_index(ascending=False);
        #tim0=xd0.index[0];
        _xt=xd0.index[0];#xt=xd0.index[-1];###
        s2=str(_xt);tim0=s2.split(" ")[0]
        
    print('\n',xfg,fss,",",tim0);   
    #-----------    
    try:
        if ((xtyp=="0")or(xtyp=="T")):
            xd=ts.get_h_data(xcod,start=tim0,end=None,retry_count=5,pause=1)     #Day9
        else: #ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
            xd=ts.get_hist_data(xcod,start=tim0,end=None,retry_count=5,pause=1,ktype=xtyp);
        #-------------
        if xd is not None:
            if (len(xd0)>0):         
                xd2 =xd0.append(xd)                
                #  flt.dup 
                xd2["index"]=xd2.index
                xd2.drop_duplicates(subset='index', keep='last', inplace=True);
                del(xd2["index"]);
                #xd2.index=pd.to_datetime(xd2.index)
                xd=xd2;
                
            xd=xd.sort_index(ascending=False);   
            xd=np.round(xd,3);
            xd.to_csv(fss,encoding='gbk')
    except IOError: 
        pass    #skip,error
    
           
    return xd  
    
    
def down_stk_yahoo010(qx,ftg):
    '''
		美股数据下载子程序
		Args:
        qx (zwDatX): 
        ftg,数据文件名
        
    :ivar xcod (int): 股票代码
    :ivar xdat (pd.DataFrame): yahoo xcod股票数据
    '''
    try:
        xcod=qx.code;
        xdat= web.DataReader(xcod,"yahoo",start="1/1/1900");
        xdat.to_csv(ftg);print(ftg);
    except IOError: 
        pass    #skip,error    

       
       
#--------stk.InxLib.xxx

def stkInxLibRd(qx):    
    '''
		读取指定的大盘数据到zw.stkInxLib
		
		Args:
            
    :
    qx.stkInxRDat='\\zwdat\\cn\\xday\\''    #大盘指数数据源路径
    qx.stkInxCode='000001'    #大盘指数代码
    qx.stkInxName='sz001'    #大盘指数名称，拼音
    qx.stkInxCName='上证指数'    #大盘指数中文名称，拼音
    #
    zw.stkInxLib=None  #全局变量，大盘指数，内存股票数据库
    
    '''
    if qx.stkInxCode!='':
        fss=qx.stkInxRDat+qx.stkInxCode+".csv";
        xfg=os.path.exists(fss);
        if xfg:
            df10=pd.read_csv(fss,index_col=0,parse_dates=[0]);
            df10=df2zwAdj(df10)
            zw.stkInxLib=df10.sort_index();

def stkInxLibSet8XTim(qx,dtim0,dtim9):
    ''' 根据时间段，切割大盘指数数据 zw.stkInxLib
    
    Args:
        dtim0（str）：起始时间
        dtim9（str）:结束时间
            
    :ivar
    zw.stkInxLib，大盘指数数据
    '''
    df10=zw.stkInxLib
    if dtim0=='':
        df20=df10;
    else:
        df20=df10[(df10.index>=dtim0)&(df10.index<=dtim9)]
        
    zw.stkInxLib=df20.sort_index();
        
    

        
#--------stk.Lib.xxx



def stkLibRd(xlst,rdir):    
    '''
		读取指定的股票数据到stkLib，可多只股票，以及股票代码文件名
		
		Args:
        xlst (list): 指定股票代码列表,
          如果xlst参数首字母是'@'，表示是股票代码文件名，而不是代码本身
          用于批量导入股票代码 
        rdir (str)：数据类存放目录 
            
    :ivar xcod (int): 股票代码
    
    '''
    zw.stkLib={}   #全局变量，相关股票的交易数据
    zw.stkLibCode=[]  #全局变量，相关股票的交易代码
    
    #
    x0=xlst[0];
    if x0.find('@')==0:
        fss=x0[1:];#print('fss',fss);  #fss=_rdatInx+fs0
        flst=pd.read_csv(fss, dtype=str,encoding='gbk')
        xlst=list(flst['code'])
        #print(xlst)
    for xcod in xlst:
        fss=rdir+xcod+".csv";
        xfg=os.path.exists(fss);
        if xfg:
            df10=pd.read_csv(fss,index_col=0,parse_dates=[0]);
            df10=df2zwAdj(df10)
            zw.stkLib[xcod]=df10.sort_index();
            zw.stkLibCode.append(xcod);


def stkLibPr():
    ''' 输出股票数据 
            
    :ivar xcod (int): 股票代码
    '''

    for xcod in zw.stkLibCode:
        df10=zw.stkLib[xcod]
        print('\n::code,',xcod)
        print(df10.head())
    print('\n stk code num',len(zw.stkLibCode))

def stkLibSet8XTim(dtim0,dtim9):
    ''' 根据时间段，切割股票数据
    
    Args:
        dtim0（str）：起始时间
        dtim9（str）:结束时间
            
    :ivar xcod (int): 股票代码
    '''
    for xcod in zw.stkLibCode:
        df10=zw.stkLib[xcod]
        if dtim0=='':
            df20=df10;
        else:
            df20=df10[(df10.index>=dtim0)&(df10.index<=dtim9)]
        #
        #zw.stkLibCode.append(xcod);
        zw.stkLib[xcod]=df20.sort_index();
        #print(zw.stkLib[xcod])
        #print(df20)

def stkLibSetDVix():
    ''' 根据时间段，切割股票数据
    
    Args:
        dtim0（str）：起始时间
        dtim9（str）:结束时间
            
    :ivar xcod (int): 股票代码
    '''
    for xcod in zw.stkLibCode:
        df10=zw.stkLib[xcod]
        df10['dvix']=df10['dprice']/df10['dprice'].shift(1)*100
        #
        zw.stkLib[xcod]=np.round(df10,2);

        
#--------stk.Lib.get.xxx        
def stkGetVars(qx,ksgn):
    '''
      获取股票代码，指定字段的数据
    
    Args:
        qx (zwQuantX): zwQuantX交易数据包
        ksgn (str): qx.stkCode,qx.xtim,qx.stkSgnPrice 
        '''
    d10=zw.stkLib[qx.stkCode]
    d01=d10[qx.xtim:qx.xtim];
    #
    dval=0;
    if len(d01)>0:
        d02=d01[ksgn]
        dval=d02[0];
    
    return dval
    
def stkGetPrice(qx,ksgn):
    '''
      获取当前价格
    
    Args:
        qx (zwQuantX): zwQuantX交易数据包
        ksgn (str): 价格模式代码
        '''
    d10=zw.stkLib[qx.stkCode]
    d01=d10[qx.xtim:qx.xtim];
    #
    price=0;
    if len(d01)>0:
        d02=d01[ksgn]
        price=d02[0];
        if pd.isnull(price):
            d02=d01['dprice']
            price=d02[0];
    
    return price
    
def stkGetPrice9x(qx,ksgn):
    '''
      获取首个、末个交易日数据
    
    Args:
        qx (zwQuantX): zwQuantX交易数据包
        ksgn (str): 价格模式代码
        '''
    d10=zw.stkLib[qx.stkCode]
    #d05=d10[qx.stkSgnPrice]
    d05=d10[ksgn]
    price0=d05[0];price9=d05[-1];
    
    return price0,price9
    
def stkLibGetTimX(xcod):
    '''
    返回指定股票代码首个、末个交易日时间数据
    
    Args:
        xcod (int): 股票代码
        '''
    d10=zw.stkLib[xcod]
    d01=d10.index;
    xtim0=d01[0];
    xtim9=d01[-1];
    #xtim0s=xtim0.strftime()
    
    return xtim0,xtim9


def stkLibName8Code(xcod):
    ''' 根据股票代码，返回股票中文、英文/拼音缩写名称
    
    Args:
        xcod (int): 股票代码
        '''
    d10=zw.stkCodeTbl[zw.stkCodeTbl['code']==xcod];
    #print(d10)
    enam='';cnam='';
    if len(d10)>0:
        xc=d10.index[0]
        enam=d10.at[xc,'ename']
        cnam=d10.at[xc,'cname']
        #print('c',xc,cnam,enam)
    
    return enam,cnam
    
#--------stk.xxx        
def stkValCalc(qx,xdicts):
    ''' 计算 xdicts 内所有的股票总价值
    
    Args:
        qx (zwQuantX): zwQuantX数据包
        xdicts (list)：所选股票代码列表 
            
    :ivar xcod (int): 股票代码
    '''
    dsum9=0;
    for xcod,xnum in xdicts.items():
        qx.stkCode=xcod;
        #price=stkGetPrice(qx,'dprice')
        price=stkGetPrice(qx,qx.priceCalc)
        dsum=price*xnum;
        dsum9=dsum9+dsum;
        #print('@c',qx.xtim,price,dsum,dsum9)
        
    return dsum9
    
#--------xbars.xxx    
def xbarPr(bars):
    ''' 输出数据包数据
    '''
    for xd in bars:
        xd.prXBar()
        print('')
        
def xbarGet8Tim(xcod,xtim):
    ''' 根据指定股票代码。时间，获取数据包
    
    Args:
        xcod (int): 股票代码
        xtim (str): 交易时间
        '''

    d10=zw.stkLib[xcod]
    d02=d10[xtim:xtim];
    
    return d02

def xbarGet8TimExt(xcod,xtim):
    '''  根据指定股票代码。时间，获取数据包及股票数据
    
    Args:
        xcod (int): 股票代码
        xtim (str): 交易时间
        '''

    d10=zw.stkLib[xcod]
    d02=d10[xtim:xtim];
    
    return d02,d10
    

#--------xtrd.xxx

def xtrdObjSet(qx):
    ''' 设置交易节点数据
    
    Args:
        qx (zwDatX): zwQuant数据包   
    #xtrdName=['date','ID','mode','code','dprice','num','kprice','sum','cash'];
        '''
    b2=pd.Series(zw.xtrdNil,index=zw.xtrdName);
    b2['date']=qx.xtim;b2['code']=qx.stkCode;b2['num']=qx.stkNum;
    if qx.stkNum!=0:
        b2['mode']=zwt.iff3(qx.stkNum,0,'sell','','buy');
        b2['dprice']=stkGetVars(qx,qx.priceWrk)
        #kprice=stkGetVars(qx,qx.priceBuy)  
        kprice=stkGetPrice(qx,qx.priceBuy)  
        b2['kprice']=kprice
        b2['sum']=kprice*qx.stkNum;
        dcash9=qx.qxUsr['cash'];
        b2['cash']=dcash9-kprice*b2['num']
    
    #print('\nb2\n',b2)
    return b2;

  
def xtrdChkFlag(qx):
    ''' 检查是不是有效交易
    
    Args:
        qx (zwQuantX): zwQuantX数据包
        #qx.stkNum，>0，买入股票；<0，卖出股票；-1；卖出全部股票
        #预设参数：qx.qxUsr 
    
    Return：
        xfg,True,有效交易；False，无效交易
        b2：有效交易的数据包 Bar
        
    :ivar xnum (int): 用户持有资产总数
    '''

    kfg=False;b2=None;qx.trdNilFlag=False;  
    dcash9=qx.qxUsr['cash'];
    dnum=qx.stkNum;dnum5=abs(dnum);
    numFg=zwt.xinEQ(dnum5,qx.stkNum0,qx.stkNum9)
    #--------
    #b2=xtrdObjSet(qx); #print('::b2\n',b2)
    if dnum>0:
        #dsum=b2['sum'];
        kprice=stkGetVars(qx,qx.priceBuy)  
        dsum=kprice*dnum;
        #股票买入股票总数，必须在限额内：100-2w手，总值不能超过现金数，买空需修改此处
        if numFg:
            if dsum<dcash9:kfg=True
            else:qx.trdNilFlag=True;      
    else:
        if qx.stkCode in qx.qxUsrStk:
            #print('@',qx.stkCode,dnum)
            xnum=qx.qxUsrStk[qx.stkCode] 
            if dnum==-1:
                qx.stkNum=-xnum;
                kfg=True;
            else:
                kfg=zwt.iff2(dnum5<=xnum,True,False);
            #    
            qx.trdNilFlag=not kfg; 
        elif dnum!=-1:    
            qx.trdNilFlag=True;   

    #        
    if kfg or qx.trdNilFlag:
        b2=xtrdObjSet(qx);	#设置交易节点                 
    else:
        qx.stkNum=0;
        
    
    return kfg,b2;

def xtrdChkFlag00(qx):
    ''' 检查是不是有效交易
    
    Args:
        qx (zwQuantX): zwQuantX数据包
        #qx.stkNum，>0，买入股票；<0，卖出股票；-1；卖出全部股票
        #预设参数：qx.qxUsr 
    
    Return：
        xfg,True,有效交易；False，无效交易
        b2：有效交易的数据包 Bar
        
    :ivar xnum (int): 用户持有资产总数
    '''

    kfg=False;b2=None;dcash9=qx.qxUsr['cash'];
    #--------
    #b2=xtrdObjSet(qx); #print('::b2\n',b2)
    if qx.stkNum>0:
        #dsum=b2['sum'];
        kprice=stkGetVars(qx,qx.priceBuy)  
        dsum=kprice*qx.stkNum;
        #股票买入股票总数，必须在限额内：100-2w手，总值不能超过现金数，买空需修改此处
        kfg=(zwt.xinEQ(qx.stkNum,qx.stkNum0,qx.stkNum9)and(dsum<dcash9))
    else:
        if qx.stkCode in qx.qxUsrStk:
            xnum=qx.qxUsrStk[qx.stkCode] 
            if (qx.stkNum==-1)or(abs(qx.stkNum)>=xnum):
                qx.stkNum=-xnum;
                kfg=True;
            elif abs(qx.stkNum)<xnum:
                kfg=True;

    #        
    if kfg:
        b2=xtrdObjSet(qx);	#设置交易节点                 
    else:
        qx.stkNum=0;
        
    
    return kfg,b2;


    
def xusrStkNum(qx,xcod):
    ''' 返回用户持有的 xcod 股票数目
    
    Args:
        qx (zwQuantX): zwQuantX数据包
        xcod (int): 股票代码
        '''

    dnum=0;
    if xcod in qx.qxUsrStk:
        dnum=qx.qxUsrStk[xcod];
    return dnum

    

def xusrUpdate(qx):
    ''' 更新用户数据
    
    Args:
        qx (zwQuantX): zwQuantX数据包 
        
        '''
        
    qx.qxUsr['date']=qx.xtim;
    #dcash=qx.qxUsr['cash']
    #qx.qxUsr['cash']=dcash-b2['sum']
    stkVal=stkValCalc(qx,qx.qxUsrStk); 
    qx.qxUsr['stkVal']=stkVal;
    dval0=qx.qxUsr['val'];
    dval=qx.qxUsr['cash']+stkVal;
    qx.qxUsr['val']=dval;
    qx.qxUsr['dret']=(qx.qxUsr['val']-dval0)/dval0;
    #print('\n::xbarUsr\n',qx.qxUsrStk)
    #print('stkVal',stkVal)
    
    #---------drawdown.xxx
    if dval>qx.downHigh:
        qx.downHigh=dval;
        qx.downLow=dval;
        #qx.downHighTime=date.today();
        qx.downHighTime=qx.xtim;
        #qx.downHighTime=datetime.dateTime;
    else:
        qx.downLow=min(dval,qx.downLow);
    #----------    
    qx.qxUsr['downHigh']=qx.downHigh
    qx.qxUsr['downLow']=qx.downLow
    kmax=downKMax(qx.downLow,qx.downHigh);
    qx.downKMax=min(qx.downKMax,kmax);
    qx.qxUsr['downKMax']=qx.downKMax;
    #xday=parse(qx.xtim)-parse(qx.downHighTime);
    nday = rrule.rrule(rrule.DAILY,dtstart=parse(qx.downHighTime), until=parse(qx.xtim)).count()
    
    dmax=max(qx.downMaxDay,nday-1)
    qx.downMaxDay=dmax
    qx.qxUsr['downDay']=qx.downMaxDay;  
    

def xusr4xtrd(qx,b2):    
    ''' 根据交易数据，更新用户数据 qxUsr
    
    Args:
        qx (zwQuantX): zwQuantX数据包
        b2 (pd.Series): 有效交易的数据包 Bar
            
    :ivar xcod (int): 股票代码
    '''

    xcod=b2['code'];
    if xcod!='':
        xfg=xcod in qx.qxUsrStk;
        #s2=zwBox.xobj2str(b2,zw.xbarName);print(xfg,'::b2,',s2)
    
        if xfg:
            xnum=qx.qxUsrStk[xcod];
            xnum2=xnum+b2['num'];
            qx.qxUsrStk[xcod]=xnum2;
            if xnum2==0:del(qx.qxUsrStk[xcod]);
        else:
            qx.qxUsrStk[xcod]=b2['num'];
        
        qx.qxUsr['cash']=qx.qxUsr['cash']-b2['sum']
              
def xtrdLibAdd(qx):
    ''' 添加交易到 xtrdLib
    
    Args:
        qx (zwQuantX): zwQuantX数据包

    '''

    qx.qxIDSet();
    #print('qx.qxID',qx.qxID)
    qx.xtrdChk['ID']=qx.qxID;
    #xbarUsrUpdate(qx,qx.xtrdChk);
    xusr4xtrd(qx,qx.xtrdChk);#qx.qxUsr['cash']=qx.qxUsr['cash']-b2['sum']
    qx.xtrdLib=qx.xtrdLib.append(qx.xtrdChk.T,ignore_index=True)
  
def xtrdLibNilAdd(qx):
    ''' 添加交易到空头记录 xtrdNilLib
    
    Args:
        qx (zwQuantX): zwQuantX数据包

    '''
    qx.xtrdChk['ID']='nil';
    qx.xtrdNilLib=qx.xtrdNilLib.append(qx.xtrdChk.T,ignore_index=True)  
    
#--zw.ret.xxx
  
def zwRetTradeCalc(qx):
    ''' 输出、计算交易数据
    
    Args:
        qx (zwQuantX): zwQuantX数据包
        
        '''
    
    trdNum=len(qx.xtrdLib);
    #print('trdNum',trdNum)
    #
    numAdd=0;numDec=0;
    sumAdd=0;sumDec=0;
    xbar=qx.qxLib.iloc[-1];
    xtim9=xbar['date']
    for xc in range(trdNum):
        xbar=qx.xtrdLib.iloc[xc];
        
        #print(xbar)
        #kprice=xbar['kprice']
        dnum=xbar['num']
        #print('dprice',dprice)
        qx.stkCode=xbar['code']
        #qx.xtim=xbar['date']
        price=xbar['kprice']
        #ksgn='dprice';
        
        #price=stkGetPrice(qx,ksgn);
        qx.xtim=xtim9;ksgn=qx.priceCalc;
        price0,price9=stkGetPrice9x(qx,ksgn);
        #print(qx.stkCode,dprice,'$',dprice0,dprice9)
        #---
        #if dnum>0:sumPut=sumPut+price*dnum;
        #if dnum<0:sumGet=sumGet+price9*dnum;:
        #
        dsum=dnum*(price9-price);
        #料敌从宽，平局，考虑到交易成本，作为亏损处理，
        if dsum>0:
            numAdd+=1;sumAdd=sumAdd+dsum;
        else:
            numDec+=1;sumDec=sumDec+dsum;
            
                    
        #print('trdNum',trdNum,numAdd,numDec,'$',dprice,dprice9,sumAdd,sumDec)
    #---------
    sum9=sumAdd+sumDec;#sumx=sumPut+sumGet;
    print('交易总次数：%d' %trdNum)
    print('交易总盈利：%.2f' %sum9)
    #print('交易总支出：%.2f' %sumPut)
    #print('交易总收入：%.2f' %sumGet)
    #print('交易收益差：%.2f' %sumx)
    print('')
    print('盈利交易数：%d' %numAdd)
    print('盈利交易金额：%.2f' %sumAdd)
    print('亏损交易数：%d' %numDec)
    print('亏损交易金额：%.2f' %sumDec)
    #print('@t',qx.xtim)
    qx.xtim=xtim9
    
    
def zwRetPr(qx):
    ''' 输出、计算回报率
    
    Args:
        qx (zwQuantX): zwQuantX数据包

    '''    
    #---回报测试
    
    retAvg=np.mean(qx.qxLib['dret']);
    retStd=np.std(qx.qxLib['dret']);
    dsharp=sharpe_rate(qx.qxLib['dret'],qx.rfRate)
    dsharp0=sharpe_rate(qx.qxLib['dret'],0)
    dcash=qx.qxUsr['cash'];
    dstk=stkValCalc(qx,qx.qxUsrStk); 
    dval=dstk+dcash;
    dret9=(dval-qx.mbase)/qx.mbase
    
    
    print('')
    print("最终资产价值 Final portfolio value: $%.2f" % dval)
    print("最终现金资产价值 Final cash portfolio value: $%.2f" % dcash)
    print("最终证券资产价值 Final stock portfolio value: $%.2f" % dstk)
    print("累计回报率 Cumulative returns: %.2f %%" % (dret9*100))
    print("平均日收益率 Average daily return: %.3f %%" %(retAvg*100))
    print("日收益率方差 Std. dev. daily return:%.4f " %(retStd))
    print('')
    print("夏普比率 Sharpe ratio: %.3f,（%.2f利率）" % (dsharp,qx.rfRate))    
    print("无风险利率 Risk Free Rate: %.2f" % (qx.rfRate))
    print("夏普比率 Sharpe ratio: %.3f,（0利率）" % (dsharp0))    
    print('')
    print("最大回撤率 Max. drawdown: %.4f %%" %(abs(qx.downKMax)))
    print("最长回撤时间 Longest drawdown duration:% d" %qx.downMaxDay);
    print("回撤时间(最高点位) Time High. drawdown: " ,qx.downHighTime)
    print("回撤最高点位 High. drawdown: %.3f" %qx.downHigh)
    print("回撤最低点位 Low. drawdown: %.3f" %qx.downLow)
    print('')
    print("时间周期 Date lenght: %d (Day)" %qx.periodNDay)
    print("时间周期（交易日） Date lenght(weekday): %d (Day)" %qx.wrkNDay)
    
    print("开始时间 Date begin: %s" %qx.xtim0)
    print("结束时间 Date lenght: %s" %qx.xtim9)
    print('')
    print("项目名称 Project name: %s" % qx.prjName)    
    print("策略名称 Strategy name: %s" % qx.staName)    
    print("股票代码列表 Stock list: ",zw.stkLibCode)    
    print("策略参数变量 staVars[]: ",qx.staVars)    
    print('')
    
#-------------qx.xxxx    
def qxObjSet(xtim,stkVal,dcash,dret):
    ''' 设置 xtrdLib 单次交易节点数据
    
    Args:
        xtim (str): 交易时间
        stkVal (int): 股票总价值
        dcash (int): 资金
        dret (float): 回报率

    '''
    qx10=pd.Series(zw.qxLibNil,index=zw.qxLibName);
    qx10['date']=xtim;qx10['cash']=dcash;
    #stkVal=xbarStkSum(qx10['xBars'],xtim);
    #stkVal=0
    qx10['stkVal']=stkVal;
    qx10['val']=stkVal+dcash;
    
    return qx10;   
    
 
        
#-------------



def xedit_zwXDat(df):
    ''' 编辑用户数据格式
    
    Args:
        df (pd.DataFrame): 股票数据
            
            '''
    df =df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'})
    df.sort_index(ascending=True,inplace=True)
    
    dx=df['open'];
    df['xdiff']=df['high']-df['low']
    df['z-xdiff']=np.round(df['xdiff']*1000/dx)
    df['z-open']=np.round(df['open']*1000/dx.shift(1))
    df['z-high']=np.round(df['high']*1000/dx)
    df['z-low']=np.round(df['low']*1000/dx)
    df['z-close']=np.round(df['close']*1000/dx)
    
    
    df['ma5']=pd.rolling_mean(df['close'],window=5); 
    df['ma10']=pd.rolling_mean(df['close'],window=10);
    df['ma20']=pd.rolling_mean(df['close'],window=20);
    df['ma30']=pd.rolling_mean(df['close'],window=30);
    
    df['v-ma5']=pd.rolling_mean(df['volume'],window=5);
    df['v-ma10']=pd.rolling_mean(df['volume'],window=10);
    df['v-ma20']=pd.rolling_mean(df['volume'],window=20);
    df['v-ma30']=pd.rolling_mean(df['volume'],window=30);
    
    c20=df.columns;#print(c20);
    if ('amount' in c20):del(df['amount']);
    if ('Adj Close' in c20):del(df['Adj Close']);
    
    df=df.round(decimals=2) 
    
    clst=["open","high","low","close","volume","xdiff","z-open","z-high","z-low","z-close","z-xdiff","ma5","ma10","ma20","ma30","v-ma5","v-ma10","v-ma20","v-ma30"]
    d30=pd.DataFrame(df,columns=clst)    
    
    return d30

#------------     
def df2yhaoo(df0):
    ''' 股票数据格式转换，转换为 Yahoo 格式
    
    Args:
        df0 (pd.DataFrame): 股票数据
        
    #Date,Open,High,Low,Close,Volume,Adj Close        
        '''
    
    clst=["Open","High","Low","Close","Volume","Adj Close"]; 
    df2 =pd.DataFrame(columns=clst)
    df0=df0.rename(columns={'date':'Date','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'})
    #df0=df0.round(decimals=2) 
    
    
    df2['Date']=df0['Date'];
    df2['Open']=df0['Open'];df2['High']=df0['High'];
    df2['Low']=df0['Low'];
    df2['Close']=df0['Close'];df2['Adj Close']=df0['Close'];
    df2['Volume']=df0['Volume'];
    df2=df2.set_index(['Date'])

    return df2


def df2cnstk(df0):
    ''' 股票数据格式转换，转换为中国 A 股格式
    
    Args:
        df0 (pd.DataFrame): 股票数据
        
    #date,open,high,close,low,volume,amount    
        '''
    
    clst=["open","high","low","close","volume","amount"]; 
    df2 =pd.DataFrame(columns=clst)
    df0 =df0.rename(columns={'Date':'date','Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'})
    #df0=df0.round(decimals=2) 
    
    df2['date']=df0['date'];
    df2['open']=df0['open'];df2['high']=df0['high'];
    df2['low']=df0['low'];df2['close']=df0['close'];
    df2['volume']=df0['volume'];
    
    df2=df2.set_index(['date'])
    
    return df2
    

def df2zw(df0):
    ''' 股票数据格式转换，转换为 zw 格式
    
    Args:
        df0 (pd.DataFrame): 股票数据

    '''

    clst=["open","high","low","close","volume"]; 
    df2 =pd.DataFrame(columns=clst)
    df0 =df0.rename(columns={'Date':'date','Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'})
    #df0=df0.round(decimals=2) 
    
    df2['date']=df0['date'];
    df2['open']=df0['open'];df2['high']=df0['high'];
    df2['low']=df0['low'];df2['close']=df0['close'];
    df2['volume']=df0['volume'];
    
    df2=df2.set_index(['date'])
    
    return df2

def df2zwAdj(df0):
    ''' 股票数据格式转换，转换为 zw 增强版格式，带 adj close
    
    Args:
        df0 (pd.DataFrame): 股票数据
        '''
    
    clst=["open","high","low","close","volume","adj close"]; 
    df2 =pd.DataFrame(columns=clst)
    df0 =df0.rename(columns={'Date':'date','Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume',"Adj Close":"adj close"})
    #df0=df0.round(decimals=2) 
    
    df0['date']=df0.index;
    df2['date']=df0['date'];
    df2['open']=df0['open'];df2['high']=df0['high'];
    df2['low']=df0['low'];df2['close']=df0['close'];
    df2['volume']=df0['volume'];
    #'adj close'
    ksgn='adj close'
    if ksgn in df0.columns:
        df2[ksgn]=df0[ksgn]
    else:
        df2[ksgn]=df0['close'];
        
    #----index
    df2=df2.set_index(['date'])
    
    return df2    
    
#-----OHLC
def stk_col_renLow(dat):
    ''' 股票数据格式转换，转换小写列名称
    
    Args:
        dat (pd.DataFrame): 股票数据
        '''

    dat =dat.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume',"Adj Close":"adj close"})
    
    return dat;
    
def stk_copy_OHLC(dat0):
    ''' 复制股票 OHLC 数据
    
    Args:
        dat0 (pd.DataFrame): 股票数据
        '''

    df0=dat0;
    df0=stk_col_renLow(df0);
    df2=pd.DataFrame(columns=['open','close','high','low']);
    df2['open']=df0['open'];df2['close']=df0['close'];
    df2['high']=df0['high'];df2['low']=df0['low'];
    df2.index=df0.index; 
    
    return df2;
    


    
   
#---------------- qt.misc.xxx    
def downKMax(dlow,dhigh):
    '''
    downKMax(dlow,dhigh):
        回缩率计算函数
        低位，高位，指的是投资组合的市场总值
    【输入】：
    dlow，当前的低位，低水位，也称，lowerWatermark
    dhigh，当前的高位，高水位，也称，highWatermark
    【输出】
    回缩率,百分比数值
    '''
    
    if dhigh>0:
        kmax=(dlow-dhigh)/float(dhigh)*100
    else:
        kmax=0
    
    return kmax
        
def sharpe_rate(rets,rfRate,ntim=252):
    '''
    sharpe_rate(rets,rfRate,ntim=252):
        计算夏普指数
    【输入】
    	rets (list): 收益率数组（根据ntim，按日、小时、保存）
      rfRate (int): 无风险收益利润
      ntim (int): 交易时间（按天、小时、等计数）
         采用小时(60分钟)线数据，ntim= 252* 6.5 = 1638.
    【输出】
        夏普指数数值
        '''
    rsharp= 0.0
    if len(rets):
        # print('rets',rets)
        rstd = np.array(rets).std(ddof=1) #np.stddev(rets, 1)  #收益波动率
        #print('rstd',rstd,rets[-1]) #,returns[]
        if rstd != 0:
            rfPerRet = rfRate / float(ntim)
            rmean=np.array(rets).mean()
            avgExRet = rmean - rfPerRet
            dsharp = avgExRet / rstd
            rsharp = dsharp * np.sqrt(ntim)
            #print('rmean,avgExRet,dsharp',rmean,avgExRet)
            #print('dsharp,rshapr',dsharp,rsharp) 
    return rsharp
      
    
#----------sta.misc


    
#----

    
def sta_dataPre0xtim(qx,xnam0):
    ''' 策略参数设置子函数，根据预设时间，裁剪数据源stkLib
    
    Args:
        qx (zwQuantX): zwQuantX数据包 
        xnam0 (str)： 函数标签

    '''

    #设置当前策略的变量参数
    qx.staName=xnam0
    qx.rfRate=0.05;  #无风险年收益，一般为0.05(5%)，计算夏普指数等需要
    #qx.stkNum9=20000;   #每手交易，默认最多20000股
    #
    #按指定的时间周期，裁剪数据源
    xt0k=qx.staVars[-2];xt9k=qx.staVars[-1];
    if (xt0k!='')or(xt9k!=''):
        #xtim0=parse('9999-01-01');xtim9=parse('1000-01-01');
            #xtim0=xtim0.strftime('%Y-%m-%d');xtim9=xtim9.strftime('%Y-%m-%d')
        if xt0k!='':
            if qx.xtim0<xt0k:qx.xtim0=xt0k;
        if xt9k!='':                
            if qx.xtim9>xt9k:qx.xtim9=xt9k;
        qx.qxTimSet(qx.xtim0,qx.xtim9)
        stkLibSet8XTim(qx.xtim0,qx.xtim9);#    print('zw.stkLibCode',zw.stkLibCode)
    
    #---stkInx 读取大盘指数数据，并裁剪数据源
    if qx.stkInxCode!='':    
        stkInxLibRd(qx)
        stkInxLibSet8XTim(qx,qx.xtim0,qx.xtim9)
        
    #============
    #---设置qxUsr用户变量，起始数据
    qx.qxUsr=qxObjSet(qx.xtim0,0,qx.money,0);
    
def cross_Mod(qx):
    ''' 均线交叉策略，判断均线向上、向下趋势
    
    Args:
        qx (zwQuantX): zwQuantX数据包
        ksma (str)：均线数据列名称
    Return:
        1:above
        0:=
        -1:below
        '''

    kma='ma_%d' %qx.staVars[0]
    xbar=qx.xbarWrk;
    dma,ma2n=xbar[kma][0],xbar['ma2n'][0]
    dp,dp2n=xbar['dprice'][0],xbar['dp2n'][0]
    #
    kmod=-9;
    if  (dp>dma)and(dp2n<ma2n)and(dp>dp2n):
        kmod=1;
        #print(kmod,'xbar',xbar)
    elif (dp<dma)and(dp2n>ma2n)and(dp<dp2n):
        kmod=-1;
        #print(kmod,'xbar',xbar)

    return kmod    


