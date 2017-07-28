# -*- coding: utf-8 -*-\
import pandas as pd

a=1
b=2
max(a,b)

def twoCandleCompare(df,indexA, indexB):
    ha=df.loc[indexA,'high']
    la=df.loc[indexA,'low']
    hb=df.loc[indexB,'high']
    lb=df.loc[indexB,'low']
    if ha<hb and la>lb:
        return 's2b'
    elif ha>hb and la>lb:
        return 'u2d'
    elif ha<hb and la<lb:
        return 'd2u'
    elif ha>hb and la<lb:
        return 'b2s'

