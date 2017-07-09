# -*- coding: utf-8 -*-


import os
import pandas as pd
import tushare as ts

#zwQuant
 
import zwSys as zw  
import zwQTBox as zwx


#----------
#自动下载，追加数据
#-------设置参数       
#股票代码文件 
finx='./data/stk_code.csv';
qx=zw.zwDatX(zw._rdatCN);
zwx.down_stk_all(qx,finx)



