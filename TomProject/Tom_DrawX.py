#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 10:12:39 2017

@author: tom
"""

import Tom_tools as tt
import Tom_Strategy as tst

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.dates as mdate
import matplotlib.ticker as ticker
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ochl
from matplotlib.dates import date2num
import numpy as np


db_x,db_y,db_w=0,0,2
db_fig=plt.figure()
#rP='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/cn/day/603859.csv'
#datastyle='dayData'
db_r=0
rect_K=[]
rect_V=[]
rect_A=[]
rect_P=[]
rect_M=[]
rect_Ac=[]
db_cols = ['blue', 'green', 'red', 'cyan',  'magenta', 'yellow', 'black', 'white']
db_datastyle=''
def initRect(h,style):
    global db_y,db_x,db_w
    global rect_K
    global rect_V
    global rect_A
    global rect_M
    global rect_P
    global rect_Ac
    if style=='K':
        if len(rect_K)==0:
            rect_K=rect_M=[db_x,db_y,db_w,h]
            #print(rect_M)
            db_y+=(h+0.1)
    elif style=='V':
        if len(rect_V)==0:
            rect_V=[db_x,db_y,db_w,h]
            db_y+=(h+0.1)
    elif style=='A':
        if len(rect_A)==0:
            rect_A=[db_x,db_y,db_w,h]
            db_y+=(h+0.1)
    elif style=='P':
        if len(rect_P)==0:
            rect_P=rect_M=[db_x,db_y,db_w,h]
            db_y+=(h+0.1)
    elif style=='Ac':
        if len(rect_Ac)==0:
            rect_Ac=[db_x,db_y,db_w,h]
            db_y+=(h+0.1)

def format_date(x,pos=None):
    global db_r
    global db_datastyle
    N=len(db_r)
    thisind=np.clip(int(x+0.5),0,N-1)
    if db_datastyle=='dayData':
        return db_r.date[thisind].strftime('%Y-%m-%d')
    elif db_datastyle=='hisTickToMinMerge':
        return db_r.time[thisind].strftime('%Y-%m-%d %H:%M:%S')
    return db_r.time[thisind].strftime('%H:%M:%S')

def getK_H(dif):
    x=0.15*dif+0.2
    if x < 1.2:
        return 1.2
    elif x > 2.2:
        return 2.2
    else:
        return x

'''
数据初始化函数
'''
def install_K_Data(r):
    quote=np.array([])
    h=r.high.max()
    l=r.low.min()
    dif=h-l
    for t in r:
        ind=r.searchsorted(t)
        _o=t.open
        _h=t.high
        _c=t.close
        _l=t.low
        #_a=t.amount
        qs=np.array([ind,_o,_c,_h,_l])
        if quote.size==0:
            quote=qs
        else:
            quote=np.vstack((quote,qs))
    return quote,dif

def install_VA_Data(r):
    quote=np.array([])
    for t in r:
        ind=r.searchsorted(t)
        #print(ind)
        _v=t.volume
        _a=t.amount
        #_a=t.amount
        qs=np.array([ind,_v,_a])
        if quote.size==0:
            quote=qs
        else:
            quote=np.vstack((quote,qs))
    return quote
def install_P_Data(r):
    quote=np.array([])
    for t in r:
        ind=r.searchsorted(t)
        _p=t.price
        qs=np.array([ind,_p])
        if quote.size==0:
            quote=qs
        else:
            quote=np.vstack((quote,qs))
    return quote

def install_M_Data(r,xdata):
    quote=np.array([])
    for t in r:
        ind=r.searchsorted(t)
        mean='mean'+str(xdata)
        alc='accelerated'+str(xdata)
        _m=t[mean]
        _a=t[alc]
        qs=np.array([ind,_m,_a])
        if quote.size==0:
            quote=qs
        else:
            quote=np.vstack((quote,qs))
    return quote

'''
画图工具函数
'''
#K线图
def draw_K(fig,rect,quote,width,func):
    ax_K=fig.add_axes(rect)
    candlestick_ochl(ax_K,quote,width=width,colorup='deeppink',colordown='c')
    ax_K.xaxis.set_major_formatter(ticker.FuncFormatter(func))
    plt.setp(ax_K.get_xticklabels(),rotation=30,horizontalalignment='right')
    plt.grid(True,which='minor',axis='y')
#画连续数据，不包含很坐标
def drawLine(fig,rect,ys,func,ls,color,label):
    ax=fig.add_axes(rect)
    plt.setp(ax.get_xticklabels(),rotation=0,horizontalalignment='right')
    #,visible=True)
    plt.plot(ys,color,label=label,linewidth=1.5,ls=ls)
    plt.legend(loc='upper right')
    #ax_vol.fill_between(index,volumes,color='coral')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(func))
#画填充数据
def drawFill(fig,rect,xs,ys,func,color):
    ax_prc=fig.add_axes(rect)
    plt.setp(ax_prc.get_xticklabels(),rotation=0,horizontalalignment='right')
    ax_prc.fill_between(xs,ys,color=color)
    ax_prc.xaxis.set_major_formatter(ticker.FuncFormatter(func))
#画点和点之间的连线
def drawPointConnect(fig,rect,xs,ys,func,ls,color,label):
    ax=fig.add_axes(rect)
    plt.setp(ax.get_xticklabels(),rotation=30,horizontalalignment='right')
    plt.plot(xs,ys,color,label=label,linewidth=1.5,ls=ls)
    plt.legend(loc='upper right')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(func))
'''
画图操作函数
'''
def tomdraw_K(rP):
    global db_r
    global rect_K
    global db_fig
    db_r=mlab.csv2rec(rP)
    db_r.sort()
    quote,dif=install_K_Data(db_r)
    k_h=getK_H(dif)
    initRect(k_h,'K')
    draw_K(db_fig,rect_K,quote,0.5,format_date)
    
def tomdraw_KwithDate(rP,sd,ed):
    global db_r
    global rect_K
    global db_fig
    db_r=mlab.csv2rec(rP)
    db_r=db_r[np.where(db_r.time>tt.str2dateYmd(sd))]
    db_r=db_r[np.where(db_r.time<(tt.str2dateYmd(ed)+tt.one_Day_Delta))]
    db_r.sort()
    quote,dif=install_K_Data(db_r)
    k_h=getK_H(dif)
    initRect(k_h,'K')
    draw_K(db_fig,rect_K,quote,0.5,format_date)

def tomdraw_VA(rP):
    global db_r
    global rect_V
    global rect_A
    global db_fig
    db_r=mlab.csv2rec(rP)
    db_r.sort()
    quote=install_VA_Data(db_r)
    indexes,volumes,amounts=[q[0] for q in quote],[q[1] for q in quote],[q[2] for q in quote]
    initRect(0.8,'V')
    initRect(0.8,'A')
    drawFill(db_fig,rect_V,indexes,volumes,format_date,'b')
    drawFill(db_fig,rect_A,indexes,amounts,format_date,'r')
    
def tomdraw_P(rP):
    global db_r
    global rect_P
    global db_fig
    db_r=mlab.csv2rec(rP)
    db_r.sort()
    quote=install_P_Data(db_r)
    prices=[q[1] for q in quote]
    initRect(1.2,'P')
    drawLine(db_fig,rect_P,prices,format_date,'--','g','price')
    
    
'''
画均线和均线加速度
'''
def tomdraw_M_Ac(rP,xdata,ls,colornum):
    if len(rect_K)>0:
        target='close'
    if len(rect_P)>0:
        target='price'
    tst.initMeanAndAcceleratedData(xdata,rP,target)
    global db_r
    global rect_M
    global rect_Ac
    global db_fig
    global db_cols
    color=db_cols[colornum]
    db_r=mlab.csv2rec(rP)
    #print(db_r)
    db_r.sort()
    quote=install_M_Data(db_r,xdata)
    means=[q[1] for q in quote]
    drawLine(db_fig,rect_M,means,format_date,ls,color,str(xdata)+'mean')
    initRect(1.2,'Ac')
    acs=[q[2] for q in quote]
    drawLine(db_fig,rect_Ac,acs,format_date,ls,color,'acs'+str(xdata))
    tst.deleteMeanData(xdata,rP)
    
    
'''
缠图模块(独立)
'''


def tomdraw_Pen(pen_df):
    global rect_K
    global db_fig
    quote=install_chan_data(pen_df)
    xs=[q[0] for q in quote]
    ys=[q[1] for q in quote]
    global rect_K
    global db_fig
    drawPointConnect(db_fig,rect_K,xs,ys,format_date,'--','g','Pen')
  


def tomdraw_Line(line_df,color):
    global rect_K
    global db_fig
    quote=install_chan_data(line_df)
    xs=[q[0] for q in quote]
    ys=[q[1] for q in quote]
    global rect_K
    global db_fig
    drawPointConnect(db_fig,rect_K,xs,ys,format_date,'--',color,'Line')

def install_chanCenter_data(center_df):
    centerPoints=[]
    for i in range(center_df.index.size):
        xS=center_df.loc[i,'startIndex']
        xE=center_df.loc[i,'endIndex']
        yL=center_df.loc[i,'lowPrice']
        yH=center_df.loc[i,'highPrice']
        pointL=[(xS,yL),(xS,yH),(xE,yH),(xE,yL),(xS,yL)]
        centerPoints.append(pointL)
    return centerPoints

def tomedraw_center(center_df):
    global rect_K
    global db_fig
    
    centerPoints=install_chanCenter_data(center_df)
    for points in centerPoints:
        xs, ys = zip(*points)
        #
        #plt.plot(xs, ys, '-')
        ax=db_fig.add_axes(rect_K)
        plt.setp(ax.get_xticklabels(),rotation=30,horizontalalignment='right')
        plt.plot(xs,ys,'blue',linewidth=1)
        #plt.plot(xs,ys,'o')
        plt.legend(loc='upper right')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))


def install_chan_data(df0):
    quote=np.array([])
    #df=tt.readDf(rP)
    #df0=tst.findLineWithDF(df)
    #df0=chanInstance.chan_module
    for i in range(df0.index.size):
        _i = df0.loc[i, 'index']
        _p = df0.loc[i, 'price']
        qs=np.array([_i,_p])
        if quote.size==0:
            quote=qs
        else:
            quote=np.vstack((quote,qs))
    return quote

    
'''
def install_XD_data(r):
    quote=np.array([])
    for t in db_r:
        if(t.xdl==4 or t.xdh==3):
            ind=db_r.searchsorted(t)
            close=t.close
            qs=np.array([ind,close])
            if quote.size==0:
                quote=qs
            else:
                quote=np.vstack((quote,qs))
    return quote

def tomdraw_XD(rP_XD):
    global db_r
    db_r=mlab.csv2rec(rP_XD)
    db_r.sort()
    quote=install_XD_data(db_r)
    #initRect(1.2,'K')
    xs=[q[0] for q in quote]
    ys=[q[1] for q in quote]
    global rect_K
    global db_fig
    ax=db_fig.add_axes(rect_K)
    plt.setp(ax.get_xticklabels(),rotation=30,horizontalalignment='right')
    #,visible=True)
    plt.plot(xs,ys,'r',label='XD',linewidth=1.5,ls='--')
    plt.legend(loc='upper right')
    #ax_vol.fill_between(index,volumes,color='coral')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
'''


'''
自动识别组合画图函数
'''
def tomdraw(rP,datastyle,means):
    global db_datastyle
    db_datastyle=datastyle
    if datastyle=='dayData' or datastyle=='hisTickToMin' or datastyle=='realTickToMin':
        tomdraw_K(rP)
        for mean in means:
            tomdraw_M_Ac(rP,mean,'--',means.index(mean))
        #tomdraw_VA(rP)
        #tomdraw_Pen(rP)
        #tomdraw_Line(rP)
    elif datastyle=='hisTick' or datastyle=='realTick':
        tomdraw_P(rP)
        for mean in means:
            tomdraw_M_Ac(rP,mean,'--',means.index(mean))
        tomdraw_VA(rP)



'''
缠图像
'''
def tomdraw_chan(chanInstance):
    global db_datastyle
    db_datastyle='hisTickToMinMerge'
    tomdraw_K(chanInstance.rP)
    #tomdraw_Pen(chanInstance.pen_df)
    tomdraw_Line(chanInstance.line_df,'red')
    df=tst.findLine(chanInstance.line_df)
    tomdraw_Line(df,'cyan')
    tomdraw_Line(tst.findLine(df),'green')
    
    #tomedraw_center(chanInstance.center_df)
def tomdraw_chan_withdate(chanInstance,sd,ed):
    global db_datastyle
    db_datastyle='hisTickToMinMerge'
    tomdraw_KwithDate(chanInstance.rP,sd,ed)
    #tomdraw_Pen(chanInstance.pen_df)
    tomdraw_Line(chanInstance.line_df,'red')
    df=tst.findLine(chanInstance.line_df)
    tomdraw_Line(df,'cyan')
    tomdraw_Line(tst.findLine(df),'green')
    

'''    
rP_XD='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/tmp/600058.csv'
db_datastyle='hisTickToMinMerge'


tomdraw_K(rP_XD)

tomdraw_XD(rP_XD)

'''
'''
#tst.deleteMeanData(2,rP)
tomdraw_M(rP_XD,5,'--',1)
tomdraw_M(rP_XD,10,'-.',2)
tomdraw_M(rP_XD,20,'-.',3)
tomdraw_M(rP_XD,30,'--',4)
tomdraw_VA(rP)
#tomdraw_P(rP)


tst.initMeanData(10,rP)

N=len(r)
quote,dif=installMinData(r)
k_h=getK_H(dif)
rect_K=[db_x,db_y,db_w,k_h]
draw_K(db_fig,rect_K,quote,0.5,format_date)

db_y+=(k_h+0.1)
rect_kk=[db_x,db_y,db_w,k_h]
draw_K(db_fig,rect_kk,quote,0.5,format_date)

indexs,volumes,amounts,means= [q[0] for q in quote],[q[5] for q in quote],[q[6] for q in quote],[q[7] for q in quote]
drawLine(db_fig,rect_kk,means,format_date,'--','g')
def tomdraw():
'''