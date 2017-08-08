# -*- coding: utf-8 -*-
# 
#  

import numpy as np
import math
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


#from pinyin import PinYin

from dateutil.parser import parse
from dateutil import rrule
import datetime as dt

#zwQuant
import zwSys as zw
import zwTools as zwt
import zwQTBox as zwx
import zwQTDraw as zwdr
import zwBacktest as zwbt
import zwStrategy as zwsta

import zw_talib as zwta


#=======================    

   
      
def bt_endRets(qx):            
    #---ok ，测试完毕
    # 保存测试数据，qxlib，每日收益等数据；xtrdLib，交易清单数据
    #qx.qxLib=qx.qxLib.round(4)
    qx.qxLib.to_csv(qx.fn_qxLib,index=False,encoding='utf-8')
    qx.xtrdLib.to_csv(qx.fn_xtrdLib,index=False,encoding='utf-8')
    qx.prQLib()
    #
    #-------计算交易回报数据
    zwx.zwRetTradeCalc(qx)
    zwx.zwRetPr(qx)
    #-------绘制相关图表，可采用不同的模板
    # 初始化绘图模板：dr_quant3x
    zwdr.dr_quant3x_init(qx,12,8);
    #  设置相关参数
    xcod=zw.stkLibCode[0];
    #ma1='ma_%d' %qx.staVars[0]
    ksgn,ksgn2=qx.priceWrk,'vwap';
    kmid8=[[xcod,ksgn,ksgn2]]   
    # 绘图
    zwdr.dr_quant3x(qx,xcod,'val',kmid8,'apple')
    # 可设置，中间图形窗口的标识
    #qx.pltMid.legend([]);

   

#==================main

#--------设置参数
xlst=['aapl-201x']   
qx=zwbt.bt_init(xlst,'dat/','vwap',1000000);
#
#---设置策略参数
qx.debugMod=1
qx.stkInxCode=''
qx.staVars=[5,0.01,'2011-01-01','2012-12-31']    
#---根据当前策略，对数据进行预处理
zwsta.VWAP_dataPre(qx,'vwap','close')
#---绑定策略函数&运行回溯主函数
qx.staFun=zwsta.VWAP_sta;
zwbt.zwBackTest(qx)
#
bt_endRets(qx)
    



#---
'''
k408x_vwap
Sharpe ratio: 0.89
最终资产价值 Final portfolio value: $1441776.00
累计回报率 Cumulative returns: 44.18 %
夏普比率 Sharpe ratio: 0.89
最大回撤率 Max. drawdown: 11.54 %
最长回撤时间 Longest drawdown duration: 153 days, 0:00:00

'''