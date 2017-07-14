# -*- coding: utf-8 -*-
'''
   zw_sta00.py
   zwQT策略库课程模版文件
   
'''
import os, sys
import numpy as np
import pandas as pd

#zwQuant
import zwSys as zw
import zwTools as zwt
import zwQTBox as zwx
import zwQTDraw as zwdr
import zwBacktest as zwbt
import zwStrategy as zwsta
import zw_talib as zwta

#=======================    
  
     
#----策略函数    
def sta00(qx):
    '''
    策略说明
     Args:
        qx (zwQuantX): zwQuantX数据包

    '''
    stknum=0;
    xtim,xcod=qx.xtim,qx.stkCode;
    dprice=zwx.stkGetVars(qx,'dprice')
    xnum=zwx.xusrStkNum(qx,xcod);
    #
    ksma='ma_%d' %qx.staVars[1]
    dsma=qx.xbarWrk[ksma][0]
    #
    if (dprice>dsma)and(xnum==0):
        stknum=10;
        print('buy',xtim,dprice,dsma,xnum);
    if (dprice<=dsma)and(xnum>0):
        stknum=-1;
        print('sell',xtim,dprice,dsma,xnum);
    #
    return stknum   

def sta00_dataPre(qx,xnam0,ksgn0):
    ''' 策略.数据预处理函数 说明
    
    Args:
        qx (zwQuantX): zwQuantX数据包 
        xnam0 (str)：函数标签
        ksgn0 (str): 价格列名称，一般是'adj close'
        '''

    zwx.sta_dataPre0xtim(qx,xnam0);
    #----对各只股票数据，进行预处理，提高后期运算速度
    ksgn,qx.priceCalc=ksgn0,ksgn0;  #'adj close';
    for xcod in zw.stkLibCode:
        d20=zw.stkLib[xcod];
        
        #  计算交易价格kprice和策略分析采用的价格dprice,kprice一般采用次日的开盘价
        #d20['dprice']=d20['open']*d20[ksgn]/d20['close']
        d20['dprice']=d20['close']
        #d20['kprice']=d20['dprice'].shift(-1)
        d20['kprice']=d20['dprice']
        #
        d=qx.staVars[0];d20=zwta.MA(d20,d,ksgn);
        d=qx.staVars[1];d20=zwta.MA(d20,d,ksgn);
        #
        zw.stkLib[xcod]=d20;
        if qx.debugMod>0:
            print(d20.tail())    
            #---
            #fss='tmp\\'+qx.prjName+'_'+xcod+'.csv'
            fss=os.path.join('tmp',qx.prjName+'_'+xcod+'.csv')
            d20.to_csv(fss)   
    
   
def bt_endRets(qx):            
    #---ok ，测试完毕
    # 保存测试数据，qxlib，每日收益等数据；xtrdLib，交易清单数据
    #qx.qxLib=qx.qxLib.round(4)
    qx.qxLib.to_csv(qx.fn_qxLib,index=False,encode='utf-8')
    qx.xtrdLib.to_csv(qx.fn_xtrdLib,index=False,encode='utf-8')
    qx.prQLib()
    #
    #-------计算交易回报数据
    zwx.zwRetTradeCalc(qx)
    zwx.zwRetPr(qx)
    
    #-------绘制相关图表，可采用不同的模板
    # 初始化绘图模板：dr_quant3x
    zwdr.dr_quant3x_init(qx,12,8);
    #  设置相关参数
    xcod=zw.stkLibCode[0];ksgn=qx.priceBuy;
    #xcod='glng';ksgn=qx.priceBuy;
    #kmid8=[['aeti',ksgn],['egan',ksgn],['glng',ksgn,'ma_5','ma_30'],['simo',ksgn,'ma_5','ma_30']]   
    ma1='ma_%d' %qx.staVars[0]
    ma2='ma_%d' %qx.staVars[1]
    kmid8=[[xcod,qx.priceWrk,ma1,ma2]]   
    # 绘图
    zwdr.dr_quant3x(qx,xcod,'val',kmid8,'')
    # 可设置，中间图形窗口的标识
    #qx.pltMid.legend([]);
    #
    print('')
    print('每日交易推荐')
    print('::xtrdLib',qx.fn_xtrdLib)
    print(qx.xtrdLib.tail())
    #print(qx.xtrdLib)

    

#==================main
#--------init，设置参数
#rss='\\zwdat\\cn\\day\\'
rss='dat\\'
xlst=['600401']   #600401,*ST海润,*SThr 
qx=zwbt.bt_init(xlst,rss,'sta00',10000);
#
#---设置策略参数

#qx.staVars=[163,'2014-01-01','']    
qx.staVars=[20,'2014-01-01','']    
qx.debugMod=1
#qx.staFun=zwsta.CMA_sta; #---绑定策略函数&运行回溯主函数
#---根据当前策略，对数据进行预处理
#zwsta.CMA_dataPre(qx,'sta00','close')
#----运行回溯主程序

#zwbt.zwBackTest(qx)
#----输出回溯结果
#bt_endRets(qx)
    