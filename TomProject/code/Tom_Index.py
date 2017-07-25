# -*- coding: utf-8 -*-
#Editing by Tom
import os,sys
import Tom_AutoReadData as ta
import Tom_Draw as tda
#import Tom_Draw as tda
import pandas as pd
import numpy as np


code='000009'
cycle='01'
date='2017-06-14'
datastyle='hisTick'
rP,df,fromDate,toDate,selectDF,codename=ta.readStk(datastyle,date,cycle,code)
print(df)
print(rP)
print(fromDate)
print(toDate)
print(selectDF)
#print(codename)
#tomdraw(code,readPath,datastyle, fromDate, toDate, plotList)
tda.tomdraw(code,rP,datastyle,fromDate,toDate,['P'])