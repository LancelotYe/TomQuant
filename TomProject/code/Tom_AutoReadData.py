# -*- coding: utf-8 -*-
import os,sys
import Tom_DownloadStkData as td
import pandas as pd
import numpy as np
import datetime as dt
from enum import Enum

#DataStyle=Enum('dayData','hisTick','hisTickToMin','realTick')

'''
datastyle=['dayData','hisTick','hisTickToMin','realTick','realTickToMin']
'''
def readStk(datastyle,date,cycle,code):
    td.selectStkCodeList([int(code)])
    if datastyle=='dayData':
        readPath=td.dayDataPath
        readPath=os.path.join(readPath,code+'.csv')
        if os.path.exists(readPath)==False:
            td.getStkFromFile(td.select_stk_code)
    elif datastyle=='hisTick':
        readPath=td.hisTickPath
        #date='1992-01-03'
        Ddate=dt.datetime.strptime(date,'%Y-%m-%d')
        delta=dt.timedelta(days=1)
        Tdate=Ddate+delta
        tdate=dt.datetime.strftime(Tdate,'%Y-%m-%d')
        getYM=dt.datetime.strftime(Ddate,'%Y-%m')
        readPath=os.path.join(readPath,getYM,date+'_'+code+'.csv')
        if os.path.exists(readPath)==False:
            td.getPastTick(td.select_stk_code,date,tdate)
    elif datastyle=='hisTickToMin':
        #cycle='01'
        readPath=td.hisTickToMinPath
        readPath=os.path.join(readPath,date,'M'+cycle,code+'.csv')
        if os.path.exists(readPath)==False:
            XreadPath=td.hisTickPath
        #date='1992-01-03'
            Ddate=dt.datetime.strptime(date,'%Y-%m-%d')
            delta=dt.timedelta(days=1)
            Tdate=Ddate+delta
            tdate=dt.datetime.strftime(Tdate,'%Y-%m-%d')
            getYM=dt.datetime.strftime(Ddate,'%Y-%m')
            XreadPath=os.path.join(XreadPath,getYM,date+'_'+code+'.csv')
            outputdir=os.path.join(td.outputMinDir,date)
            if os.path.exists(XreadPath)==False:
                td.getPastTick(td.select_stk_code,date,tdate)
            td.transfToMinWithTick(XreadPath,outputdir,[cycle])
    elif datastyle=='realTick':
        readPath=td.realTickPath
        readPath=os.path.join(readPath,code+'.csv')
        td.getTodayTickAndCycle(td.select_stk_code,[cycle])
    elif datastyle=='realTickToMin':
        readPath=td.realTickToMinPath
        readPath=os.path.join(readPath,'M'+cycle,code+'.csv')
        td.getTodayTickAndCycle(td.select_stk_code,[cycle])
    else:
        print('No such type')
        return
    #print(readPath)
    df=pd.read_csv(readPath, encoding='gbk')
    print(df)
    
readStk('hisTickToMin','2015-01-09','01','600192')
