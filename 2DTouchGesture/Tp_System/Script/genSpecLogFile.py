#--*— coding: utf-8----
#==========================

import os,sys
par_path = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
lib_path = os.path.abspath(os.path.join(par_path,os.path.pardir)) + "\\Lib"
sys.path.append(lib_path)

import csv
import codecs
import shutil
import logging
import time
import xml.etree.ElementTree as ET

#Python 2.x
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

#Python3.x
import importlib,sys
importlib.reload(sys)

factory_name = "Default"
#factory_name = "JingYuan"
#factory_name = "HuaQin"
#factory_name = 'ChuangWei'
#factory_name = 'OuFei'
#factory_name = 'XXTP'
#factory_name = 'LaiBao'
#factory_name = 'Test'

#modify filedir to be the dir you want
filedir = os.getcwd()
filedir_shopfloor = 'TestResult'
#filedir = "C:\\FPMTESTFILE\\STANDARD\\"
filedir_MES = "D:\\MES\\"

#test point type = 12 OR 11
testPointType = '11'


logging.basicConfig(filename='pylog.log', filemode='a+', level=logging.INFO, format='%(asctime)s : %(levelname)s : %(funcName)s.%(lineno)s : %(message)s')


def on_gtm_startup(paramStr):
        "example"
        '''['','','GT7863','','no-INT_NO_IDLE_britten_TpOrder_Basic_chip_only.tporder','','','','','2021-07-30 16:52:23','','GTVApp08.29','GTLib1.14.0.0.18']'''
        "meaning"
        '''[WorkOrder,ProductName,IcName,Lot_Id,TestPrg,Handler_Id,Tester_Id,Tester_Id,Operator_Id,Factory,Date,Form,BoardVersion,ToolVersion]'''
        
        param_list = paramStr.split(",")
        if len(param_list) < 13:
                print("Error: on_gtm_startup() param number error")
                return

        work_order = param_list[0]
        product_name = param_list[1]
        ic_name = param_list[2]
        lot_id = param_list[3]
        test_prg = param_list[4]
        handler_id = param_list[5]
        tester_id = param_list[6]
        operator_id = param_list[7]
        factory = param_list[8]
        date_str = param_list[9]
        form = param_list[10]
        board_ver = param_list[11]
        tool_ver = param_list[12]


def on_gtm_exit(paramStr):
        "example"
        '''['','','GT7863','','no-INT_NO_IDLE_britten_TpOrder_Basic_chip_only.tporder','','','','',
        '2021-07-30 16:52:23','','GTVApp08.29','GTLib1.14.0.0.18','2000','1990','9','1','0','0']'''

        "meaning"
        '''[WorkOrder,ProductName,IcName,Lot_Id,TestPrg,Handler_Id,Tester_Id,Tester_Id,Operator_Id,Factory,
        Date,Form,BoardVersion,ToolVersion,TotalCount,OkCount,NgCount,BreakCount,WarningCount,UnknownCount]'''
        
        param_list = paramStr.split(",")
        if len(param_list) < 19:
                print("Error: on_gtm_exit() param number error")
                return

        work_order = param_list[0]
        product_name = param_list[1]
        ic_name = param_list[2]
        lot_id = param_list[3]
        test_prg = param_list[4]
        handler_id = param_list[5]
        tester_id = param_list[6]
        operator_id = param_list[7]
        factory = param_list[8]
        date_str = param_list[9]
        form = param_list[10]
        board_ver = param_list[11]
        tool_ver = param_list[12]
        total_count = param_list[13]
        ok_count = param_list[14]
        ng_count = param_list[15]
        break_count = param_list[16]
        warning_count = param_list[17]
        unknown_count = param_list[18]


def checkBeforeTest(worker_id, order_name, gtm_version, fw_version, barcode, reserved_1, reserved_2, reserved_3):
        """
        example:
        worker_id = 000999
        order_name = xxxxxxxxxxx.tporder
        gtm_version = GTLib1.14.0.0.18
        fw_version = NOR_L-00.00.0D_7863_0A.01.05.11
        barcode = xxxx_xxx_xxx
        reserved_1 =
        reserved_2 =
        reserved_3 =
        """
        if factory_name == 'LaiBao':
                import LaiBaoActiveMQ
                LaiBaoActiveMQ.check_before_test(worker_id, order_name, gtm_version, fw_version, barcode)
        elif factory_name == "Default":
                return

def genSpecLogFile_HuaQin(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes):
        # ================ FOR huaqin ===============
        if testRes == 'OK':
                testRes = 'OK'
                logdir = filedir +'\\'+ filedir_shopfloor + '\\' + testRes + '\\'
                if not os.path.exists(logdir):
                        os.makedirs(logdir)
                #if not os.path.exists(filedir_MES):
                #    os.makedirs(filedir_MES)
        else:
                testRes = 'NG'
                logdir = filedir +'\\'+ filedir_shopfloor + '\\' + testRes + '\\'
                if not os.path.exists(logdir):
                        os.makedirs(logdir)
                #if not os.path.exists(filedir_MES):
                #    os.makedirs(filedir_MES)

        #copy log file
        shutil.copy(originLogPath,logdir)


def get_fw_ver_from_logcsv(originLogPath):
        try:
                fd = open(originLogPath, 'r', encoding="utf-8")
                data = fd.read()
                fd.close()
                root = ET.fromstring(data)

                print("\n*****Version Test*****")
                xpath = "TestItems/Item[@name='Version Test']/CurVerDataHex"
                strFwVer = root.find(xpath).text
                strFwVer = strFwVer.replace("\n", "").replace("\t", "").replace(",", " ").replace("0x", " ")
                print("fwver:" + strFwVer)
                return strFwVer

        except Exception as e:  # 捕获除与程序退出sys.exit()相关之外的所有异常
                print("parse xml fail!")
                return ""


def genSpecLogFile_JingYuan(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes):
        dateTimeNow = time.localtime()
        strToday = time.strftime("%Y%m%d", dateTimeNow)
        strFileDir = filedir_MES + strToday + "\\"
        if not os.path.exists(strFileDir):
                os.makedirs(strFileDir)

        strFwVer = get_fw_ver_from_logcsv(originLogPath)
        strTimeNow = time.strftime("%H:%M:%S", dateTimeNow)
		#strTimeNow = time.strftime("%Y/%m/%d %H:%M:%S", dateTimeNow)
        outTestRes = ''
        if 'OK' == testRes:
                outTestRes = 'Pass'
        elif 'NG' == testRes:
                outTestRes = 'Fail'	
			
        barCode = barCode.strip()
        barcodeToWrite = barCode
        if len(barCode) == 0:
                barcodeToWrite = "null"
                strFileName = barcodeToWrite + time.strftime("%H%M%S", dateTimeNow) + ".csv"
        else:
                strFileName = barCode + ".csv"
        
        strRow1 = "Test Time,Barcode,NG List,FWVer"
        strRow2 = "\t" + strTimeNow + "," "\t"+ barcodeToWrite + "," + outTestRes + "," + strFwVer[-8:]

        strFilePath = strFileDir + strFileName
        f = open(strFilePath, "w")
        f.write(strRow1)
        f.write("\n")
        f.write(strRow2)


def genSpecLogFile_ChuangWei(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes):
        # ================ FOR ChuangWei ===============
        
        if 'OK' == testRes:
                testRes = 'PASS'

        #
        logdir = filedir + testRes + '\\'
        if not os.path.exists(logdir):
                os.makedirs(logdir)

        if -1 != curtime.find('T'):        
                time = curtime[0:8] + curtime[9:15]
                #print time
        else:
                time = curtime

        #create csv file
        filename = chipName + '_' + chipUID +'_'+boardNumber+'_'+boardUID+'_'+ time + '_' + testRes + ".csv"
        #csvfile = open(logdir + filename,'wb')
        #writer = csv.writer(csvfile)
        #writecontent = []
        #writecontent.append(testRes)
        #writer.writerow(writecontent)
        #csvfile.close()

        #copy log file
        shutil.copyfile(originLogPath,logdir + filename)


def genSpecLogFile_OuFei(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes):
        # ============ FOR OuFei ======================
        #
        if not os.path.exists(filedir):
                os.makedirs(filedir)
        #       
        if ' ' != barCode:
                #
                if -1 != curtime.find('T'):        
                        time = curtime[0:8] + curtime[9:15]
                        #print time
                else:
                        time = curtime
                #
                if ' ' == productBatch:
                        proBatch = '00'
                else:
                        proBatch = productBatch
                #       
                if ' ' == station:
                        stationPoint = '00';
                else:
                        stationPoint = station
                #
                if ' ' == workerId:
                        workernumber = '00'
                else: 
                        workernumber = workerId
                #
                if testRes == 'OK':
                        resFlag = '00'
                elif testRes == 'NG':
                        resFlag = '01'
                
                #create csv file
                filename = barCode + '-' + time + '---' + testPointType + '---' + resFlag + '-' + testRes + ".csv"
                csvfile = open(filedir + filename,'w')



def genSpecLogFile_Test(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes):
        # =================== FOR TEST ====================
        #
        if not os.path.exists(filedir):
                os.makedirs(filedir)

        #       
        #if ' ' != barCode:
        #
        if -1 != curtime.find('T'):        
                time = curtime[0:8] + curtime[9:15]
                #print time
        else:
                time = curtime
        #
        if ' ' == productBatch:
                proBatch = '00'
        else:
                proBatch = productBatch
        #       
        if ' ' == station:
                stationPoint = '00';
        else:
                stationPoint = station
        #
        if ' ' == workerId:
                workernumber = '00'
        else: 
                workernumber = workerId
        #
        if testRes == 'OK':
                resFlag = '00'
        elif testRes == 'NG':
                resFlag = '01'
        
        #create csv file
        filename = barCode + '-' + time + '---' + testPointType + '---' + resFlag + '-' + testRes + ".csv"
        #csvfile = open(filedir + filename,'w')
        shutil.copyfile(originLogPath,filedir + filename)


def genSpecLogFile_XXTP(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes):
        # ================ FOR toptouch ===============
        if testRes == 'OK':
                testRes = 'PASS'
                ERROR_CODE = ' '
                # logdir = filedir + testRes + '\\'
                if not os.path.exists(filedir):
                        os.makedirs(filedir)
                if not os.path.exists(filedir_MES):
                        os.makedirs(filedir_MES)
        else:
                testRes = 'FAIL'
                ERROR_CODE = 'Bin2'
                # logdir = filedir + testRes + '\\'
                if not os.path.exists(filedir):
                        os.makedirs(filedir)
                if not os.path.exists(filedir_MES):
                        os.makedirs(filedir_MES)
        # #create csv file
        # filename = barCode + '_' + testRes + '_' + ERROR_CODE + '_' + boardNumber + '_' + curtime + '_' + chipName + ".csv"
        # #copy log file
        # shutil.copyfile(originLogPath,logdir + filename)
        
        #==========MES==========
        time_str = curtime[0:8] + curtime[9:15]
        f = open(filedir + 'a.csv','w')
        f_write = csv.writer(f)
        data_row1 = [("ChipID","QRCode","Result","Error","Time","ERROR_POSITION","START_TIME","END_TIME","MACHINE_ID","SHIPPING_SN","FIRMWARE_REV"),\
        (chipUID,barCode+'\t',testRes,ERROR_CODE,time_str+'\t'," "," "," ",boardUID," "," ")]
        f_write.writerows(data_row1)
        f.close()

        filename_MES = 'MES' + '_' + 'toptouch' + '_' + boardUID + '_' + time_str + ".csv"
        shutil.copyfile(filedir + 'a.csv',filedir_MES + filename_MES)
        os.remove(filedir + 'a.csv')


def genSpecLogFile_Default(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes):
        if 'OK' == testRes:
                testRes = 'PASS'

        #
        logdir = filedir + testRes + '\\'
        if not os.path.exists(logdir):
                os.makedirs(logdir)

        if -1 != curtime.find('T'):        
                time = curtime[0:8] + curtime[9:15]
                #print time
        else:
                time = curtime

        #create csv file
        filename = chipName + '_' + chipUID +'_'+boardNumber+'_'+boardUID+'_'+ time + '_' + testRes + ".csv"
        #csvfile = open(logdir + filename,'wb')
        #writer = csv.writer(csvfile)
        #writecontent = []
        #writecontent.append(testRes)
        #writer.writerow(writecontent)
        #csvfile.close()

        #copy log file
        shutil.copyfile(originLogPath,logdir + filename)


def genSpecLogFile(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes):
        """
        example:
        chipName = GT9886
        chipUID = 55385033303603FFFFFE00E5FF0BFFFF
        productBatch =
        station = 
        workerId =
        barCode = QR code  
        curtime = 20201023T102101
        testRes = OK or NG
        boardNumber = 1
        boardUID = 01156824434743343337FFD6
        originLogPath = F:\\..\\TestResult\\GT9896_20190902_v1\\2019-Sep-05\\NG\\GT9896_No1_01308_145228.418564_NG'
        testItemRes = 801|OK,802|OK,1212|NG,1213|OK
        """

        if factory_name == 'ChuangWei':
                genSpecLogFile_ChuangWei(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes)
        elif factory_name == 'OuFei':
                genSpecLogFile_OuFei(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes)
        elif factory_name == 'XXTP':
                import mtlog
                import json

                logging.basicConfig(filename='pylog.log', filemode='a+', level=logging.INFO, format='%(asctime)s : %(levelname)s : %(funcName)s.%(lineno)s : %(message)s')

                try:
                        genSpecLogFile_XXTP(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes)
                except Exception as e:
                        logging.critical('genSpecLogFile')
                        logging.critical(e)
                try:
                        mtlog.mtlog(originLogPath)
                except Exception as e:
                        logging.critical('mtlog.mtlog')
                        logging.critical(e)
        elif factory_name == 'LaiBao':
                import LaiBaoActiveMQ
                LaiBaoActiveMQ.report_after_test(workerId, barCode, originLogPath)
        elif factory_name == 'Test':
                genSpecLogFile_Test(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes)
        elif factory_name == 'HuaQin':
                genSpecLogFile_HuaQin(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes)
        elif factory_name == "JingYuan":
                genSpecLogFile_JingYuan(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes)
        elif factory_name == "Default":
                genSpecLogFile_Default(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes)


#For Debug
def start():
        chipName='GT9886'
        chipUID = '55385033303603FFFFFE00E5FF0BFFFF'
        productBatch='10001'
        station='12'
        workerId='1110'
        barCode='1029345123456704'
        curtime='20201023T102101'
        testRes='OK'
        boardNumber = '1'
        boardUID = '01156824434743343337FFD6'
        originLogPath='C:\\Users\\yanghong\\Desktop\\DP270\\TestResult\\NG\\DP270-Machine_GT7986P_NULL_NULL_20210901_201632_(0-1)_NG.csv'
        testItemRes = '801|OK,802|OK,1212|NG,1213|OK'
        genSpecLogFile(chipName,chipUID,productBatch,station,workerId,barCode,curtime,testRes,boardNumber,boardUID,originLogPath,testItemRes)

if __name__ == "__main__":
        start()
