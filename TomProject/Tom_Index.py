# -*- coding: utf-8 -*-
#Editing by Tom
import os,sys
import Tom_AutoReadData as ta
import Tom_Draw as tda
import Tom_DownloadStkData as td
import Tom_Strategy as tst
import Tom_tools as tt
#import Tom_Draw as tda
import pandas as pd
import numpy as np
import tushare as ts

#td.addStkCodesToFav(['600259','600549'])
#td.removeStkFromFav('ALL')
startcode='603859'
cycle='05'
date='2017-03-15'
datastyle='dayData'
#hisCodeMinEndDate='2017-03-17'
rP,df,fromDate,toDate,selectDF,datastyle=ta.readStk(datastyle,date,cycle,startcode)
tst.initMeanData(20,rP)
tda.tomdraw(rP,datastyle)
#,fromDate,toDate)
#rP,df,fromDate,toDate,selectDF=ta.readNextStk()
#rP,df,fromDate,toDate,selectDF=ta.readAfterXDay(2)
#rP,df,fromDate,toDate,selectDF,datastyle=ta.readNextDatastyleStk()
#rP,df,fromDate,toDate,selectDF=ta.readOtherCycleData(10)

#plotList=['P']
#tomdraw(code,readPath,datastyle, fromDate, toDate, plotList)
#获取数据
'''
datastyle='hisTickToMin'
fromDate='2017-05-10'
toDate='2017-07-31'
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
#td.getPastTick(tt.fav_stk_code,'2017-07-21','2017-07-24')
#td.transToMinWithTickSourceDir(tt.fav_stk_code,tt.his_tick_sourceDir,tt.outputMinDir,'2017-07-21','2017-07-24',['01'])

'''
startdate='2017-05-10'
enddate='2017-07-31'
code='600058'
cycle='01'
td.mergeMinData(startdate,enddate,cycle,str(code))
'''

#df=ts.get_tick_data('000001',date='2017-01-03')