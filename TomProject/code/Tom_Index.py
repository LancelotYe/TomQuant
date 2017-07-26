# -*- coding: utf-8 -*-
#Editing by Tom
import os,sys
import Tom_AutoReadData as ta
import Tom_Draw as tda
import Tom_DownloadStkData as td
#import Tom_Draw as tda
import pandas as pd
import numpy as np


startcode='000010'
cycle='05'
date='2017-05-12'
datastyle='hisTickToMin'
rP,df,fromDate,toDate,selectDF,datastyle=ta.readStk(datastyle,date,cycle,startcode)
#rP,df,fromDate,toDate,selectDF=ta.readNextStk()
#rP,df,fromDate,toDate,selectDF=ta.readAfterXDay(2)
#rP,df,fromDate,toDate,selectDF,datastyle=ta.readNextDatastyleStk()
#rP,df,fromDate,toDate,selectDF=ta.readOtherCycleData(10)
print(df)
print(rP)
print(fromDate)
print(toDate)
print(selectDF)
#plotList=['P']
#tomdraw(code,readPath,datastyle, fromDate, toDate, plotList)
#获取数据
tda.tomdraw(rP,datastyle,fromDate,toDate)
