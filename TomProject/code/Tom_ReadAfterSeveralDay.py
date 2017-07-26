# -*- coding: utf-8 -*-
import Tom_AutoReadData as ta
import Tom_Draw as tda
import pandas as pd


rP,df,fromDate,toDate,selectDF,datastyle=ta.readAfterXDay(2)

tda.tomdraw(rP,datastyle,fromDate,toDate)
print(df)
print(rP)
print(fromDate)
print(toDate)
print(selectDF)