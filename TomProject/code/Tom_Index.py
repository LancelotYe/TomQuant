# -*- coding: utf-8 -*-
#Editing by Tom
import os,sys
import Tom_AutoReadData as ta
import Tom_Draw as tda
#import Tom_Draw as tda
import pandas as pd
import numpy as np


code='000006'
cycle='01'
date='2017-05-10'
datastyle='dayData'
rP,df,fromDate,toDate=ta.readStk(datastyle,date,cycle,code)


#tomdraw(code,readPath,datastyle, fromDate, toDate, plotList)
tda.tomdraw(code,rP,datastyle,fromDate,toDate,['K','V'])