# -*- coding: utf-8 -*-
import os,sys
import numpy as np
import pandas as pd
from datetime import datetime
#import time

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ochl
#from matplotlib.dates import date2num
from matplotlib.dates import date2num
import matplotlib.dates as mdate
import zwSys as zw


    

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
   
    
def drawVolumns(rect, qs, XLabelVisable):
    dates = [q[0] for q in qs]
    volumns = [q[5] for q in qs]
    fig = plt.figure()
    ax_vol = fig.add_axes(rect)
    ax_vol.fill_between(dates, volumns, color = 'coral')
    ax_vol.xaxis_date()
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
def tomdraw(code,readPath,datastyle, fromDate, toDate, plotList):
    plt.style.use('dark_background')
#    date1 = (2017,1,1)
#    date2 = (2017,6,1)
#    quotes = quotes_historical_yahoo_ohlc("INTC", date1, date2)
    #if datastyle=='dayData':
    fname=readPath
    qs,w = getDataFromCSVWithDataStyle(datastyle,fname,fromDate,toDate)
    try:
        left,width = 0, 2.5
        rect_vol = [left, 0, width, 0.8]
        rect_main = [left, 0, width, 1.2]
        rect_price = [left,0, width, 1.2]
        for plot in plotList:   
            if plot == 'K':
                drawCandlestick(w,rect_main, qs, False)
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
                #print(floatDayOne)
            elif i==(quotes.index.size-1):
                floatDayEnd=floatday
                #print(floatDayEnd)
                
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
    else:
        for i,time in enumerate(quotes['time']):
            df=quotes[quotes.index==i]
            if datastyle=='hisTickToMin' or datastyle=='realTickToMin':
                if datastyle=='hisTick':
                    getDate=datetime.strftime(datetime.strptime(fromDate, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d ')
                    datetimeDay = datetime.strptime(getDate+time, '%Y-%m-%d %H:%M:%S')
                elif datastyle=='hisTickToMin':
                    getDate=datetime.strftime(datetime.strptime(fromDate, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d ')
                    datetimeDay = datetime.strptime(getDate+time, '%Y-%m-%d %H:%M:%S')
                elif datastyle=='realTick':
                    getDate=datetime.strftime(datetime.now(),'%Y-%m-%d ')
                    datetimeDay = datetime.strptime(getDate+time, '%Y-%m-%d %H:%M:%S')
                elif datastyle=='realTickToMin':
                    getDate=datetime.strftime(datetime.now(),'%Y-%m-%d ')
                    datetimeDay = datetime.strptime(getDate+time, '%Y-%m-%d %H:%M:%S')
                else:
                    print('No such type')
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
    return qs,w
        #datetimeDay = datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S') #%H:%M:%S
