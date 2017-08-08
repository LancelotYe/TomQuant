# -*- coding: utf-8 -*-
import os,sys
import numpy as np
import pandas as pd
from datetime import datetime
#import time

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.dates as mdate
import matplotlib.ticker as ticker
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ochl
from matplotlib.dates import date2num

import Tom_tools as tt

drawing_board_x,drawing_board_y,drawing_board_w=0,0,2
drawing_board_fig=plt.figure()
drawing_board_data=pd.DataFrame()
AX_K
AX_P
AX_V
drawing_board_datastyle=''

rP='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/cn/day/603859.csv'
datastyle='dayData'
def initRect(h):
    global drawing_board_y
    rect=[drawing_board_x,drawing_board_y,drawing_board_w,h]
    y0=h+0.1
    drawing_board_y+=y0
    return rect

def initData(readPath):
    global drawing_board_data
    drawing_board_data=mlab.csv2rec(readPath)

def drawing_format_date(x,pos=None): 
    global drawing_board_data
    N=len(drawing_board_data)
    thisind=np.clip(int(x+0.5),0,N-1)
    if datastyle=='dayData':
        return drawing_board_data.date[thisind].strftime('%Y-%m-%d')
    elif datastyle=='hisTickToMinMerge':
        return drawing_board_data.time[thisind].strftime('%Y-%m-%d %H:%M:%S')
    return drawing_board_data.time[thisind].strftime('%H:%M:%S')
def tomdrawK(readPath,datastyle):
    
    global drawing_board_datastyle
    global drawing_board_data
    global drawing_board_fig
    drawing_board_datastyle=datastyle
    if drawing_board_data.size==0:
        initData(readPath)
    r=drawing_board_data
    quote, dif= installMinData(r)
    global drawing_rect_K
    if not drawing_rect_K:
        h=getDrawingBoradMainH(dif)
        drawing_rect_K=initRect(h)
    print(quote)
    drawK(drawing_board_fig,drawing_rect_K,quote,0.5,drawing_format_date)
    
readPath='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/cn/day/603859.csv'
datastyle='dayData'
#tomdraw(readPath,datastyle)
    
def getDrawingBoradMainH(dif):
    x=0.15*dif+0.2
    return x if x<2.0 else 2.0
    
def tomdraw(readPath,datastyle):
    r=mlab.csv2rec(readPath)
    r.sort()
    N=len(r)
    def format_date(x,pos=None):    
        thisind=np.clip(int(x+0.5),0,N-1)
        if datastyle=='dayData':
            return r.date[thisind].strftime('%Y-%m-%d')
        elif datastyle=='hisTickToMinMerge':
            return r.time[thisind].strftime('%Y-%m-%d %H:%M:%S')
        return r.time[thisind].strftime('%H:%M:%S')
    left,width=0,2
    vol_h=0.8
    amount_h=0.8
    tick_h=0.8
    def getMainH(dif):
        x=0.15*dif+0.2
        return x if x<2.0 else 2.0
    fig=plt.figure()
    if datastyle=='dayData' or datastyle=='hisTickToMin' or datastyle=='realTickToMin' or datastyle=='hisTickToMinMerge':
        quote, dif= installMinData(r)
        #main_h=0.2
        #y=0.15x+0.2
        main_h=getMainH(dif)
        rect_main=[left,0,width,main_h]
        drawK(fig,rect_main,quote,0.5,format_date)
        '''
        if(means!= None):
            drawLine(fig,rect_main,means,format_date,'--','y')
        '''
        indexs,volumes,amounts= [q[0] for q in quote],[q[5] for q in quote],[q[6] for q in quote]
        
        rect_vol=[left,main_h+0.1,width,vol_h]
        rect_amount=[left,main_h+vol_h+0.2,width,amount_h]
        drawFill(fig,rect_vol,indexs,volumes,quote,0.5,format_date,'#054E9F')
        drawFill(fig,rect_amount,indexs,amounts,quote,0.5,format_date,'#8B0000')
        
        plt.show()
    elif datastyle=='hisTick' or datastyle=='realTick':
        quote=installTickData(r)
        prices,volumes,amounts= [q[0] for q in quote],[q[1] for q in quote],[q[2] for q in quote]
        rect_price=[left,0,width,0.2]
        rect_volumes=[left,0.2+0.1,width,tick_h]
        rect_amounts=[left,tick_h+0.4,width,tick_h]
        #ax_vol=fig.add_axes(rect_tick)
       
        drawLine(fig,rect_volumes,volumes,format_date,'-.','firebrick')
        drawLine(fig,rect_amounts,amounts,format_date,'--','lawngreen')
        drawLine(fig,rect_price,prices,format_date,':','lightcoral')
        #drawLine(fig,rect_tick,)
    plt.style.use('seaborn-bright')
    plt.show()
    #fig.autofmt_xdate()
    #index=[q[0] for q in quote]
    #volumes=[q[5] for q in quote]
    #fig = plt.figure()
    #ax_vol=fig.add_axes(rect_vol)
    
    #plt.plot(dates,volumes,'#f2c200',label='price',linewidth=0.7)
    #ax_vol.fill_between(index,volumes,color='coral')
    #ax_vol.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    #plt.grid()
    #prices=[q[1] for q in quote]
   
def drawK(fig,rect,quote,width,func):
    ax_K=fig.add_axes(rect)
    candlestick_ochl(ax_K,quote,width=width,colorup='deeppink',colordown='c')
    ax_K.xaxis.set_major_formatter(ticker.FuncFormatter(func))
    plt.setp(ax_K.get_xticklabels(),rotation=0,horizontalalignment='right')
    plt.grid(True,which='minor',axis='y')
             #,visible=True)
    #ylim([6.9,7.1])
    #xlim([0,1])
def drawLine(fig,rect,ys,func,ls,color):
    ax=fig.add_axes(rect)
    plt.setp(ax.get_xticklabels(),rotation=0,horizontalalignment='right')
    #,visible=True)
    plt.plot(ys,color,linewidth=0.7,ls=ls)
    #ax_vol.fill_between(index,volumes,color='coral')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(func))

def drawFill(fig,rect,xs,ys,quote,width,func,color):
    ax_prc=fig.add_axes(rect)
    plt.setp(ax_prc.get_xticklabels(),rotation=0,horizontalalignment='right')
    ax_prc.fill_between(xs,ys,color=color)
    ax_prc.xaxis.set_major_formatter(ticker.FuncFormatter(func))
    
def installMinData(r):
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
        _v=t.volume
        _a=t.amount
        #_a=t.amount
        qs=np.array([ind,_o,_c,_h,_l,_v,_a,])
        if quote.size==0:
            quote=qs
        else:
            quote=np.vstack((quote,qs))
    return quote,dif
def installTickData(r):
    quote=np.array([])
    for t in r:
        _p=t.price
        _v=t.volume
        _a=t.amount
        qs=np.array([_p,_v,_a])
        if quote.size==0:
            quote=qs
        else:
            quote=np.vstack((quote,qs))
    return quote

