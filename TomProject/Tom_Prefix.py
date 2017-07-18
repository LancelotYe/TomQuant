'''
os.getcwd()
ha = os.curdir
os.pardir
os.chdir(os.pardir)
os.chdir(os.curdir)
os.listdir(os.getcwd())

os.stat(os.getcwd())
os.sep
os.chdir(os.sep)

os.pathsep
os.environ

print(sys.argv[0])
sys.argv[0]
sys.version
sys.path
def file_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        print(root) #当前目录路径  
        print(dirs) #当前路径下所有子目录  
        print(files) #当前路径下所有非目录子文件  
''' 

'''
目录结构
zwDat/
    基础数据包
    base/
    中国
    cn/
        日
        day/
    美国
    ua/
        日
        day/
'''
import os, sys
import numpy as np
import pandas as pd

#  zwQuant
import zwSys as zw  
import zwQTBox as zwx
import zwTools as zwt





getBasePath()