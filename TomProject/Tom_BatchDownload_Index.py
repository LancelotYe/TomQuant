import Tom_DownloadStkData as td
import Tom_tools as tt
import threading
from time import ctime,sleep
'''
批量下载
'''
def batchdownload(startDate):
    threads=[]
    startD=tt.str2dateYmd(startDate)
    endD=tt.str2dateYmd(tt.today_Date_Ymd_Str)
    if (endD-startD)/tt.one_Day_Delta>4:
        num = 4
    else:
        num = ((endD-startD)/tt.one_Day_Delta)
    if ((endD-startD)/num).seconds>0:
        delta = ((endD-startD)/num)
        delta = delta.days+1
    else:
        delta = (endD-startD)/num
        delta = delta.days
        
    startDateStr=startDate
    #分解日期进行多线程下载
    while not num<=0:
        endDateStr=tt.strDateYmdAddDelta(startDateStr,delta*tt.one_Day_Delta)
        if tt.str2dateYmd(endDateStr)>tt.today_Date:
            endDateStr=tt.today_Date_Ymd_Str
        t=threading.Thread(target=td.downHisFavTickDatasJudgeLocal,args=(startDateStr,endDateStr))
        #td.downHisTickDataJudgeLocal(startDateStr,endDateStr)
        #print(startDateStr+'to'+endDateStr+'isReady')
        startDateStr=endDateStr
        threads.append(t)
        num-=1
        #sleep(5)
    
    for t in threads:
        t.setDaemon(True)
        t.start()
    #sleep(5)

def batchToMin(code,startDate,cycle):
    code='%06d'%int(code)
    for date in tt.getNoWeekendDateList(startDate,tt.today_Date_Ymd_Str):
        minReadPath=tt.getHisTickToMinCodePath(code,date,cycle)
        if not tt.isExist(minReadPath):
            readPath=tt.getHisTickCodePath(code,date)
            if not tt.isExist(readPath):
                print('[-]code:'+code+' date:'+date+' has no hisTick Data')
                continue
            td.transfToMinWithTick(readPath,tt.joinPath(tt.outputMinDir,date),[cycle])
            print('[+]code:'+code+' date:'+date+' just ToMin')

def batchAllCodeToMin(startDate,cycle):
    threads=[]
    for code in tt.getFavList().code:
        t=threading.Thread(target=batchToMin,args=(code,startDate,cycle))
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()
    '''
    if not tt.isExist(readPath):
        xReadPath,xtdf,xfromDate,xtoDate,xSelectDF,xDatastyle=getStkCodeHisTickData(code,date)
        if xReadPath==None:
            print(str(code)+'at:'+date+' No Data')
            return
        if tt.isExist(xReadPath):
            selecDF,datastyle=tt.initHisTickToMinSelectFileWithCode(code,date,cycle)
            transfToMinWithTick(xReadPath,tt.joinPath(tt.outputMinDir,date),[cycle])
    if tt.isExist(readPath):
        tdf=tt.readDf(readPath)
        fromDate=date+' '+tdf.tail(1)['time'].values[0]
        toDate=date+' '+tdf.head(1)['time'].values[0]
    '''
'''
#step setting favlist
tt.getFavList()
tt.removeStkFromFav('ALL')
tt.addStkCodesToFav([603987])
'''
'''
#df=tt.getFavList()
#tt.readDf(tt.stk_code)
'''

startDate='2017-08-01'
batchdownload(startDate)
batchAllCodeToMin(startDate,'01')

