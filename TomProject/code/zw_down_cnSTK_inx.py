# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import tushare as ts

#  zwQuant
import zwSys as zw  
import zwQTBox as zwx
import zwTools as zwt


#----------

#下载大盘指数文件，
qx=zw.zwDatX(zw._rdatCN);#qx.prDat();

#指数索引文件
finx='data/inx_code.csv';
zwx.down_stk_inx(qx,finx);

