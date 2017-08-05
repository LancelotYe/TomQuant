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
    

'''
def getDataFromCSV(filePath, fromDate, toDate):
    quotes = pd.read_csv(filePath, header = None,names="abcdefghi", sep = ',')
    quotes = quotes.values
    #print(quotes)
    qs = np.array([])
    fdt = datetime.strptime(fromDate, '%Y-%m-%d').timestamp()
    tdt = datetime.strptime(toDate, '%Y-%m-%d').timestamp()
    if (fdt > tdt):
        print("ERROR:toDate(val) should bigger than fromDate(val)")
        return
    for record in quotes:
        if record[0] == 'date':
            continue
        datetimeDay = datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') #%H:%M:%S
        t = datetimeDay.timestamp()
        if (t > tdt):
            continue
        if (t < fdt):
            break
        floatday = date2num(datetimeDay)
        _o = float(record[1])
        _c = float(record[3])
        _h = float(record[2])
        _l = float(record[4])
        _v = float(record[5])
        #dates = np.append(dates,iday)
        #volumns = np.append(volumns, _v)
        quote = np.array([floatday, _o, _c, _h, _l, _v])
        #print(quote)
        if qs.size == 0:
            qs = quote
        else:
            qs = np.vstack((qs, quote))
    #print(qs)    
    return qs

    
def tomdrawPlot(code, timeType, fromDate, toDate, plotList):
    plt.style.use('dark_background')
#    date1 = (2017,1,1)
#    date2 = (2017,6,1)
#    quotes = quotes_historical_yahoo_ohlc("INTC", date1, date2)
    
    fname = zw._rdatCN+"day/"+str(code)+".csv"
    
    qs = getDataFromCSV(fname, fromDate, toDate)
        
    
    try:
        left,width = 0, 3.5
    
        rect_vol = [left, 0, width, 0.8]
        rect_main = [left, 0, width, 1.2]
        for plot in plotList:   
            if plot == 'K':
                drawCandlestick(rect_main, qs, False)
            if plot == 'V':
                drawVolumns(rect_vol, qs, True)
        
        
    except Exception as e:
        print(e);
    
   #dates = pd.to_datetime(dates)
   # dates = [datetime.fromtimestamp(i) for i in dates]
    

code1 = '000001'
code2 = '000002'
timeType = "day"
fromDate = "2017-1-4"
toDate = "2017-6-4"
plotList = ['K','V']
tomdrawPlot(code1, timeType, fromDate, toDate, plotList)
#tomdrawPlot(code2, timeType, fromDate, toDate, plotList)
matplotlib.style.available
matplotlib.style.library

datastyle=['dayData','hisTick','hisTickToMin','realTick','realTickToMin']
'''

def drawCandlestick(w,rect, qs, XLabelVisable):
    fig = plt.figure()
    ax_K = fig.add_axes(rect)
    candlestick_ochl(ax_K, qs, width = w, colorup='deeppink', colordown='c')
    ax_K.xaxis_date()
    
    plt.setp(ax_K.get_xticklabels(), rotation= 30, horizontalalignment='right')
    plt.setp(ax_K.get_xticklabels(), visible=XLabelVisable) 
    #plt.xticks(pd.date_range('2017-03-16 09:36:00','2017-03-16 12:00:00'),rotation=90)
    #fig.autofmt_xdate()

'''
def drawCandlestick2(w,rect, qs, XLabelVisable):
    fig = plt.figure()
    ax_K = fig.add_axes(rect)
    def format_date(x, pos=None):
        np.clip(int(x+0.5),0,N-1)
        return r.date[thisind].strftime(%Y-%m-%d)
    
    candlestick_ochl(ax_K, qs, width = w, colorup='deeppink', colordown='c')
    ax_K.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    ax_K.xaxis_date()
    
    plt.setp(ax_K.get_xticklabels(), rotation= 30, horizontalalignment='right')
    plt.setp(ax_K.get_xticklabels(), visible=XLabelVisable) 
    plt.xticks(pd.date_range('2017-03-16 09:36:00','2017-03-16 12:00:00'),rotation=90)
    #fig.autofmt_xdate()
'''

def drawVolumns(rect, qs, XLabelVisable):
    dates = [q[0] for q in qs]
    volumns = [q[5] for q in qs]
    fig = plt.figure()
    ax_vol = fig.add_axes(rect)
    ax_vol.fill_between(dates, volumns, color = 'coral')
    #ax_vol.xaxis_date()
    ax_vol.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M'))
    plt.setp(ax_vol.get_xticklabels(), rotation= 30, horizontalalignment='right')
    plt.setp(ax_vol.get_xticklabels(), visible=XLabelVisable)
   
def drawTickPrices(rect, qs):
    dates = [q[0] for q in qs]
    prices = [q[1] for q in qs]
    fig = plt.figure()
    
    ax_vol = fig.add_axes(rect)
    plt.setp(ax_vol.get_xticklabels(), rotation= 30, horizontalalignment='right')
    plt.plot(dates,prices,'#f2c200',label='price',linewidth=1.0)
    ax_vol.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))
    
    #ax_vol.xaxis_date()
    #plt.xticks(dates)
    plt.grid()
    plt.show()
def tomdraw(readPath,datastyle, fromDate, toDate):
    #plt.style.use('dark_background')'seaborn-bright'
#    date1 = (2017,1,1)
#    date2 = (2017,6,1)
#    quotes = quotes_historical_yahoo_ohlc("INTC", date1, date2)
    #if datastyle=='dayData':
    fname=readPath
    
    '''
    r=tt.readDf(fname)
    #r=mlab.csv2rec(fname)
    r.sort()
    N=len(r)
    quote=np.array([])
    for t in r:
        ind=r.searchsorted(t)
        _o=t.open
        _h=t.high
        _c=t.close
        _l=t.low
        qs=np.array([ind,_o,_c,_h,_l])
        if quote.size==0:
            quote=qs
        else:
            quote=np.vstack((quote,qs))
    def format_date(x, pos=None):
        thisind=np.clip(int(x+0.5),0,N-1)
        return r.date[thisind].strftime('%Y-%m-%d')
    left,width=0,0.3
    rect_main=[left,0,width,0.3]
    fig=plt.figure()
    ax_K=fig.add_axes(rect_main)
    candlestick_ochl(ax_K,quote,width=0.5,colorup='deeppink',colordown='c')
    ax_K.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    fig.autofmt_xdate()
    plt.show()
    '''
    qs,w,plotList= getDataFromCSVWithDataStyle(datastyle,fname,fromDate,toDate)
    try:
        left,width = 0, 1.7
        rect_vol = [left, 0, width, 0.8]
        rect_main = [left, 0, width, 1.2]
        rect_price = [left,0, width, 2.0]
        for plot in plotList:   
            if plot == 'K':
                drawCandlestick(w,rect_main, qs, True)
            if plot == 'V':
                drawVolumns(rect_vol, qs, True)
            if plot == 'P':
                drawTickPrices(rect_price,qs)
    except Exception as e:
        print(e);



def getDataFromCSVWithDataStyle(datastyle,filePath, fromDate, toDate):
    if os.path.exists(filePath)==False:
        print('no file in this filepath')
        return
    quotes = pd.read_csv(filePath,encoding='gbk')
    #print(quotes)
    #print(quotes)
    qs = np.array([])
    fdt = datetime.strptime(fromDate, '%Y-%m-%d %H:%M:%S').timestamp()
    tdt = datetime.strptime(toDate, '%Y-%m-%d %H:%M:%S').timestamp()
    if (fdt > tdt):
        print("ERROR:toDate(val) should bigger than fromDate(val)")
        return
    floatDayOne=float()
    floatDayEnd=float()
    plotList=[]
    if datastyle=='dayData':
        for i,date in enumerate(quotes['date']):
            datetimeDay = datetime.strptime(date+' 13:00:00','%Y-%m-%d %H:%M:%S')
            df=quotes[quotes.index==i]
            t = datetimeDay.timestamp()
            if (t > tdt):
                continue
            if (t < fdt):
                break
            floatday = date2num(datetimeDay)
            if i==0:
                floatDayOne=floatday
                print(floatDayOne)
            elif i==(quotes.index.size-2):
                floatDayEnd=floatday
                print(floatDayEnd)
                
            _o = float(df['open'])
            _c = float(df['close'])
            _h = float(df['high'])
            _l = float(df['low'])
            _v = float(df['volume'])
            #dates = np.append(dates,iday)
            #volumns = np.append(volumns, _v)
            quote = np.array([floatday, _o, _c, _h, _l, _v])
            #print(quote)
            if qs.size == 0:
                qs = quote
            else:
                qs = np.vstack((qs, quote))
        plotList=['K','V']
    else:
        for i,time in enumerate(quotes['time']):
            df=quotes[quotes.index==i]
            if datastyle=='hisTickToMin' or datastyle=='realTickToMin':
                if datastyle=='hisTickToMin':
                    getDate=datetime.strftime(datetime.strptime(fromDate, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d ')
                    datetimeDay = datetime.strptime(getDate+time, '%Y-%m-%d %H:%M:%S')
                elif datastyle=='realTickToMin':
                    getDate=datetime.strftime(datetime.now(),'%Y-%m-%d ')
                    datetimeDay = datetime.strptime(getDate+time, '%Y-%m-%d %H:%M:%S')
                else:
                    print('No such type')
                plotList=['K','V']
                t = datetimeDay.timestamp()
                if (t > tdt):
                    continue
                if (t < fdt):
                    break
                floatday = date2num(datetimeDay)
                if i==0:
                    floatDayOne=floatday
                    #print(floatDayOne)
                elif i==(quotes.index.size-1):
                    floatDayEnd=floatday
                    #print(floatDayEnd)
                #print(floatday)
                _o = float(df['open'])
                _c = float(df['close'])
                _h = float(df['high'])
                _l = float(df['low'])
                _v = float(df['volume'])
                #dates = np.append(dates,iday)
                #volumns = np.append(volumns, _v)
                quote = np.array([floatday, _o, _c, _h, _l, _v])
                #print(quote)
                if qs.size == 0:
                    qs = quote
                else:
                    qs = np.vstack((qs, quote))
            elif datastyle=='hisTick' or datastyle=='realTick':
                if datastyle=='hisTick':
                    getDate=datetime.strftime(datetime.strptime(fromDate, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d ')
                    datetimeDay = datetime.strptime(getDate+time, '%Y-%m-%d %H:%M:%S')
                elif datastyle=='realTick':
                    getDate=datetime.strftime(datetime.now(),'%Y-%m-%d ')
                    datetimeDay = datetime.strptime(getDate+time, '%Y-%m-%d %H:%M:%S')
                else:
                    print('No such type')
                plotList=['P']
                t = datetimeDay.timestamp()
                if (t > tdt):
                    continue
                if (t < fdt):
                    break
                floatday = date2num(datetimeDay)
                if i==0:
                    floatDayOne=floatday
                    #print(floatDayOne)
                elif i==(quotes.index.size-1):
                    floatDayEnd=floatday
                _p = float(df['price'])
                _a = float(df['amount'])
                _t = float()
                if df['type'].values[0] == 'buy':_t=1 
                else:_t=0
                
                #print(_t)
                quote = np.array([floatday, _p,_a,_t])
                if qs.size==0:
                    qs=quote
                else:
                    qs=np.vstack((qs, quote))
    w =((floatDayOne-floatDayEnd)/quotes.index.size)/4
    return qs,w,plotList
        #datetimeDay = datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') #%H:%M:%S
def tomdraw2(readPath,datastyle, fromDate, toDate):
    
    #readPath='e:\\Users\\yjh19\\workspace\\TomQuant\\TomQuantData\\cn\\day\\000010.csv'
    readPath='e:\\Users\\yjh19\\workspace\\TomQuant\\TomQuantData\\cn\\hisTickToMin\\2017-03-16\\M05\\000010.csv'
    #readPath='e:\\Users\\yjh19\\workspace\\TomQuant\\TomQuantData\\cn\\hisTick\\2017-03\\2017-03-16_000010.csv'
    datastyle='hisTickToMin'
    r=mlab.csv2rec(readPath)
    r.sort()
    N=len(r)
    def format_date(x,pos=None):
        thisind=np.clip(int(x+0.5),0,N-1)
        #return r.date[thisind].strftime('%Y-%m-%d')
        if datastyle=='dayData':
            return r.date[thisind].strftime('%Y-%m-%d')
        return r.time[thisind].strftime('%H:%M:%S')

    left,width=0,2.4
    #main_h_ratio=2.5
    vol_h=0.8
    amount_h=0.8
    tick_h=0.8
    #rect_main=[left,0,width,main_h]
    #rect_vol=[left,0.75,width,vol_h]
    #rect_amount=[left,1.6,width,amount_h]
    #rect_tick=[left,1.6,width,tick_h]
    def getMainH(dif):
        return 0.15*dif+0.2
    fig=plt.figure()
    if datastyle=='dayData' or datastyle=='hisTickToMin' or datastyle=='realTickToMin':
        quote, dif= installMinData(r)
        #main_h=0.2
        #y=0.15x+0.2
        main_h=getMainH(dif)
        rect_main=[left,0,width,main_h]
        drawK(fig,rect_main,quote,0.5,format_date)
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
    candlestick_ochl(ax_K,quote,width=0.5,colorup='deeppink',colordown='c')
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
        qs=np.array([ind,_o,_c,_h,_l,_v,_a])
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