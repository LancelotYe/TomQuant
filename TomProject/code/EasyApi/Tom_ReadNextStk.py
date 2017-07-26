# -*- coding: utf-8 -*-
import Tom_AutoReadData as ta
import Tom_Draw as tda
import pandas as pd


rP,df,fromDate,toDate,selectDF=ta.readNextStk()

tda.tomdraw(rP,datastyle,fromDate,toDate,['K','V'])