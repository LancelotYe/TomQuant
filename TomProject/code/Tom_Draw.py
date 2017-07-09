# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from datetime import datetime
#import time

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ochl
from matplotlib.dates import date2num



def drawCandlestick(rect, qs, XLabelVisable):
    fig = plt.figure()
    ax_K = fig.add_axes(rect)
    candlestick_ochl(ax_K, qs, width = 1.1, colorup='deeppink', colordown='c')
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
   
    
def getDataFromCSV(filePath, fromDate, toDate):
    quotes = pd.read_csv(filePath, header = None,names = "abcdefghi", sep = ',')
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
        datetimeDay = datetime.strptime(record[0], '%Y-%m-%d') #%H:%M:%S
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
    
    fname = "../zwDat/cn/"+timeType+"/"+str(code)+".csv"
    
    qs = getDataFromCSV(fname, fromDate, toDate)
        
    
    try:
        left,width = 0, 0.8
    
        rect_vol = [left, 0, width, 0.2]
        rect_main = [left, 0, width, 0.5]
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