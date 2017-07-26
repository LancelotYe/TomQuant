# -*- coding: utf-8 -*-
import Tom_AutoReadData as ta
import Tom_Draw as tda
import pandas as pd


rP,df,fromDate,toDate,selectDF=ta.readOtherCycleData(10)# -*- coding: utf-8 -*-

tda.tomdraw(rP,datastyle,fromDate,toDate,['K','V'])