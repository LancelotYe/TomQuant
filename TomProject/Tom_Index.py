# -*- coding: utf-8 -*-
#Editing by Tom
import os,sys
import Tom_AutoReadData as ta
import Tom_DrawX as tda
import Tom_DownloadStkData as td
import Tom_Strategy as tst
import Tom_tools as tt
#import Tom_Draw as tda
import pandas as pd
import numpy as np
import tushare as ts

#td.addStkCodesToFav(['600259','600549'])
#td.removeStkFromFav('ALL')

#test1
'''
startcode='000002'
cycle='01'
date='2017-08-04'
datastyle='hisTickToMin'
#hisCodeMinEndDate='2017-03-17'
rP,df,fromDate,toDate,selectDF,datastyle=ta.readStk(datastyle,date,cycle,startcode)

#hldf=tst.filterRepeatTopsAndBottomsData(df)

x=5
x2=15
x3=30

tda.tomdraw(rP,datastyle,[x,x2,x3])

df=tt.readDf(rP)

'''




#plotList=['P']
#tomdraw(code,readPath,datastyle, fromDate, toDate, plotList)
#获取数据

'''
datastyle='hisTickToMin'
fromDate='2017-08-01'
toDate='2017-08-07'
rP='/Users/tom/Library/Mobile Documents/com~apple~CloudDocs/Documents/TomLearning/Python/QuantTrade/TomQuant/TomQuantData/min/M01/600058.csv'
df=tt.readDf(rP)
fromDate=df.tail(1)['time'].values[0]
toDate=df.head(1)['time'].values[0]
tda.tomdraw(rP,datastyle,fromDate,toDate)
print(rP,fromDate,toDate,selectDF,datastyle,df)
td.removeStkFromFav('ALL')
pd.read_csv(td.fav_stk_code,encoding='gbk')
'''
#td.addStkCodesToFav(['600058'])
#tt.readDf(tt.fav_stk_code)
#td.getPastTick(tt.fav_stk_code,'2017-07-21','2017-07-24')
#td.transToMinWithTickSourceDir(tt.fav_stk_code,tt.his_tick_sourceDir,tt.outputMinDir,'2017-07-21','2017-07-24',['01'])

#批量下载数据合并

'''
操作favList
'''
'''
tt.getFavList()
tt.removeStkFromFav('ALL')
tt.addStkCodesToFav([603968])
'''
#tt.readDf(tt.stk_code)
'''
合并的分时数据分析
'''
startdate='2017-04-28'
enddate='2017-08-15'
#code='000001'
cycle='01'
#datastyle='hisTickToMin'
datastyle='hisTickToMinMerge'

#td.mergeMinData(startdate,enddate,cycle,str(code))

#tt.strDateYmdAddDelta(startdate,tt.ten_Days_Delta)

rP=td.getFavLongTimeData(startdate,enddate,[cycle])[0]
#readPath=tt.getHisTickToMinMergeCodePath(600058,1)



#df=tt.readDf(rP)

sd='2017-04-28'
ed='2017-08-30'
chan=tst.Chan(rP,sd,ed)

#tda.tomdraw_chan(chan)
tda.tomdraw_chan_withdate(chan,sd,ed)
#tda.tomdraw_KwithDate(rP,sd,ed)
#tda.tomdraw(rP,datastyle,[])

#df=ts.get_tick_data('000001',date='2017-01-03')
#df=tt.readDf('/Users/yejunhai/Desktop/sz000002_成交明细_2017-08-21.xls')
#df=pd.read_excel('/Users/yejunhai/Desktop/sz000002_成交明细_2017-08-21.xls',sheetname=None ,skiprows=[0])
