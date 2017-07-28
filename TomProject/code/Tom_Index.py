# -*- coding: utf-8 -*-
#Editing by Tom
import os,sys
import Tom_AutoReadData as ta
import Tom_Draw as tda
import Tom_DownloadStkData as td
#import Tom_Draw as tda
import pandas as pd
import numpy as np

#td.addStkCodesToFav(['600259','600549'])
#td.removeStkFromFav('ALL')
startcode='000010'
cycle='05'
date='2017-03-16'
datastyle='hisCodeMin'
hisCodeMinEndDate='2017-03-17'
rP,df,fromDate,toDate,selectDF,datastyle=ta.readStk(datastyle,date,cycle,startcode,hisCodeMinEndDate)
#rP,df,fromDate,toDate,selectDF=ta.readNextStk()
#rP,df,fromDate,toDate,selectDF=ta.readAfterXDay(2)
#rP,df,fromDate,toDate,selectDF,datastyle=ta.readNextDatastyleStk()
#rP,df,fromDate,toDate,selectDF=ta.readOtherCycleData(10)

#plotList=['P']
#tomdraw(code,readPath,datastyle, fromDate, toDate, plotList)
#获取数据
tda.tomdraw(rP,datastyle,fromDate,toDate)
print(rP,fromDate,toDate,selectDF,datastyle,df)

#pd.read_csv(td.fav_stk_code,encoding='gbk')
#td.getPastTick(td.fav_stk_code,'2017-05-02','2017-05-04')
#td.transToMinWithTickSourceDir(td.fav_stk_code,td.his_tick_sourceDir,td.outputMinDir,'2017-05-02','2017-05-04',['01'])