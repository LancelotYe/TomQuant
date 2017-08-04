#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 10:37:39 2017

@author: tom
"""

from matplotlib import pyplot as plt 
from matplotlib import scale as mscale 
from matplotlib import transforms as mtransforms 
from matplotlib import ticker as mticker 
import numpy as np 
'''
class SegmentLocator(mticker.Locator): 
    def __init__(self, x, gap, nbins=5): 
        self.nbins = nbins 
        self.x = x 
        self.gap = gap 
        self.segments = [] 
        for segment in np.split(x, np.where(np.diff(x) > self.gap)[0]+1): 
            self.segments.append((segment[0], segment[-1])) 
              
    def __call__(self): 
        loc = [] 
        for vmin, vmax in self.segments: 
            nlocator = mticker.MaxNLocator(nbins=self.nbins) 
            loc.append(nlocator.bin_boundaries(vmin, vmax)) 
        locs = np.concatenate(loc) 
        return locs 
         
class SegmentTransform(mtransforms.Transform): 
   def __init__(self, x1, x2): 
       mtransforms.Transform.__init__(self) 
       self.x1 = x1 
       self.x2 = x2 
 
   def transform(self, a): 
       return np.interp(a, self.x1, self.x2) 
 
   def inverted(self): 
       return SegmentTransform(self.x2, self.x1) 
 
class SegmentScale(mscale.ScaleBase): 
   name = "segment" 
   def __init__(self, axis, **kwargs): 
       mscale.ScaleBase.__init__(self) 
       self.x1 = kwargs["x"] 
       self.gap = kwargs["gap"] 
       self.x2 = np.zeros_like(self.x1) 
       self.x2[1:] = np.diff(self.x1) 
       np.clip(self.x2[1:], 0, self.gap, self.x2[1:]) 
       np.cumsum(self.x2, out=self.x2) 
        
   def get_transform(self): 
       return SegmentTransform(self.x1, self.x2) 
 
   def set_default_locators_and_formatters(self, axis): 
       axis.set_major_locator(SegmentLocator(self.x1, self.gap)) 
 
mscale.register_scale(SegmentScale) 
 
x = np.r_[np.arange(0, 10, 0.1), np.arange(50, 70, 0.1), np.arange(100, 120, 0.1)] 
y = np.sin(x) 
 
pos = np.where(np.abs(np.diff(x))>1.0)[0]+1 
x2 = np.insert(x, pos, np.nan) 
y2 = np.insert(y, pos, np.nan) 
 
plt.plot(x2, y2) 
plt.plot(x, y) 
plt.xscale("segment", x=x, gap=2.0) 
plt.xlim(0, 120) 
ax = plt.gca() 
xlabels = ax.get_xticklabels() 
for label in xlabels: 
    label.set_rotation(45) 
plt.show()







import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker

#读数据
r = mlab.csv2rec('/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/cn/hisTickToMin/2017-03-16/M05/000010.csv')
r.sort()
r = r[-1:] # get the last 30 days
N = len(r)
ind = np.arange(N) # the evenly spaced plot indices
def format_date(x, pos=None):
    #保证下标不越界,很重要,越界会导致最终plot坐标轴label无显示
    thisind = np.clip(int(x+0.5), 0, N-1)
    return r.date[thisind].strftime('%Y-%m-%d')

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(ind, r.adj_close, 'o-')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
fig.autofmt_xdate()
plt.show()

'''
from matplotlib import pyplot as plt
from numpy import arange
import numpy
from matplotlib import rc

rc("figure",figsize=(15,10))
#rc('figure.subplot',bottom=0.1,hspace=0.1)
rc("legend",fontsize=16)
fig = plt.figure()


Test_Data = numpy.random.normal(size=20)

fig = plt.figure()
Dimension = (2,3)
plt.subplot2grid(Dimension, (0,0),rowspan=2)
plt.plot(Test_Data)
plt.subplot2grid(Dimension, (0,1),colspan=2)
for i,j in zip(Test_Data,arange(len(Test_Data))):
    plt.bar(i,j)
plt.legend(arange(len(Test_Data)))
plt.subplot2grid(Dimension, (1,1),colspan=2)
xticks = [r"%s (%i)" % (a,b) for a,b in zip(Test_Data,Test_Data)]
plt.xticks(arange(len(Test_Data)),xticks)
fig.autofmt_xdate()
plt.ylabel(r'$Some Latex Formula/Divided by some Latex Formula$',fontsize=14)
plt.plot(Test_Data)
#plt.setp(plt.xticks()[1],rotation=30)
plt.tight_layout()



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker


from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ochl
from matplotlib.dates import date2num
import matplotlib.dates as mdate
file='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/cn/day/000010.csv'
r=mlab.csv2rec(file)
r.sort()
#r=r[-20:]
N=len(r)

ind=np.arange(N)
def format_date(x, pos=None):
    thisind = int(x-0.5)
#    np.clip(int(x+0.5), 0, N-1)
    return r.date[thisind].strftime('%Y-%m-%d')

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(ind, r.close, 'o-')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
fig.autofmt_xdate()
plt.show()


ind=np.arange(len(r))
_o=r.open
_h=r.high
_c=r.close
_l=r.low


quote=np.array([])
for t in r:
#    ind=r.index(t)
    ind=r.searchsorted(t)
    print(ind)
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
    thisind = int(x-0.5)
#    np.clip(int(x+0.5), 0, N-1)
    return r.date[thisind].strftime('%Y-%m-%d')
left,width = 0, 0.3
rect_main = [left, 0, width, 0.3]
fig = plt.figure()
ax_K = fig.add_axes(rect_main)
candlestick_ochl(ax_K, quote, width = 0.5, colorup='deeppink', colordown='c')
ax_K.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
fig.autofmt_xdate()
#ax_K.xaxis_date()
    
#plt.setp(ax_K.get_xticklabels(), rotation= 30, horizontalalignment='right')
plt.show
#    plt.setp(ax_K.get_xticklabels(), visible=XLabelVisable) 
    #plt.xticks(pd.date_range('2017-03-16 09:36:00','2017-03-16 12:00:00'),rotation=90)
    #fig.autofmt_xdate()


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtk

file=r'/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/cn/hisTickToMin/2017-03-16/M05/000010.csv'
df=pd.read_csv(file, parse_dates=[0,2])
r = 
