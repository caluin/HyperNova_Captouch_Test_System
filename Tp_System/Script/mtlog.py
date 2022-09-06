# -*- coding: utf-8 -*-
# ==========================
# Version   : V0.1
# Date      : 2021.07.09
# Modify    : xiaowenkui
# Copyright : Goodix
# Note V0.1 : first version
# ==========================

import os
import shutil
import time
import xml.etree.ElementTree as ET
import json
import logging

log_default_path = 'D:\\Local_Log\\HD'
log_path = log_default_path
run_log = 'run_log.json'

# logging.basicConfig(filename='pylog.log', filemode='a+', level=logging.INFO, format='%(asctime)s : %(levelname)s : %(funcName)s.%(lineno)s : %(message)s')

factory_jsondata = {
    "24"        : "XXTP",
    "25"        : "JYT" 
}

cfg_jsondata = {
    "HardBin":
    {
        "ALL_PASS"                      : "1",
        "Rst Pin Test"                  : "21",
        "I2c Pin Test"                  : "4",
        "Chip uid process"              : "41",
        "Version Test"                  : "42",
        "Custom Information Process"    : "43",
        "Chip Config Process"           : "44",
        "Sensor Id Test"                : "45",
        "Int Pin Test"                  : "22",
        "Pin1 Test"                     : "23",
        "Pin2 Test"                     : "24",
        "Pin3 Test"                     : "25",
        "Pin4 Test"                     : "26",
        "Sleep Current Test"            : "15",
        "Flash Test"                    : "46",
        "Drv Sense as GIO Test"         : "29",
        "Short Test"                    : "31",
        "Active Current Test"           : "16",
        "Rawdata Test Sets"             : "32",
        "NFC Test"                      : "51",
        "Send Special Config"           : "46",
        "Key Touch Test"                : "52",
        "Save result to ic storage"     : "47",
        "UNKNOW"                        : "59",
        "ERROR"                         : "60"
    },
    "SoftBin":
    {
        "ALL_PASS"                      : "1",
        "Rst Pin Test"                  : "21",
        "I2c Pin Test"                  : "4",
        "Chip uid process"              : "41",
        "Version Test"                  : "42",
        "Custom Information Process"    : "43",
        "Chip Config Process"           : "44",
        "Sensor Id Test"                : "45",
        "Int Pin Test"                  : "22",
        "Pin1 Test"                     : "23",
        "Pin2 Test"                     : "24",
        "Pin3 Test"                     : "25",
        "Pin4 Test"                     : "26",
        "Sleep Current Test"            : "15",
        "Flash Test"                    : "46",
        "Drv Sense as GIO Test"         : "29",
        "Short Test"                    : "31",
        "Active Current Test"           : "16",
        "Rawdata Upper Limit Test"      : "321",
        "Rawdata Lower Limit Test"      : "322",
        "Adjcent Deviation Test"        : "323",
        "NFC Test"                      : "51",
        "Send Special Config"           : "46",
        "Key Touch Test"                : "52",
        "Save result to ic storage"     : "47",
        "UNKNOW"                        : "999",
        "ERROR"                         : "1000"
    },
    "TestItem":
    {
        "Rst Pin Test"                  : ["RstGndVolt"],
        "I2c Pin Test"                  : ["avdd28_volt", "vddio_volt", "SclGndVolt", "SdaGndVolt"],
        "Chip uid process"              : [],
        "Version Test"                  : ["Version"],
        "Custom Information Process"    : ["CustomInfo"],
        "Chip Config Process"           : [],
        "Sensor Id Test"                : ["SensorId"],
        "Int Pin Test"                  : ["IntGndVolt"],
        "Pin1 Test"                     : [],
        "Pin2 Test"                     : [],
        "Pin3 Test"                     : [],
        "Pin4 Test"                     : [],
        "Sleep Current Test"            : ["SleepCurrent"],
        "Flash Test"                    : [],
        "Drv Sense as GIO Test"         : ["sen25_high", "sen25_low"],
        "Short Test"                    : [],
        "Active Current Test"           : ["ActiveCurrent"],
        "Rawdata Test Sets"             : ["RawMax_Max", "RawMax_Min", "RawMax_Avg", "RawMin_Max", "RawMin_Min", "RawMin_Avg", "AccordMax_Max", "AccordMax_Min", "AccordMax_Avg"],
        "NFC Test"                      : [],
        "Send Special Config"           : [],
        "Key Touch Test"                : [],
        "Save result to ic storage"     : ["SaveResult"]
    },
    "TestData":
    {
        "avdd28_volt":
        {
            "XML_PATH"      : "TestItems/Item[@name='I2c Pin Test']/AvddVolt",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "None",
            "UNIT"          : "mV"
        },
        "vddio_volt":
        {
            "XML_PATH"      : "TestItems/Item[@name='I2c Pin Test']/VddioVolt",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "None",
            "UNIT"          : "mV"
        },
        "SclGndVolt":
        {
            "XML_PATH"      : "TestItems/Item[@name='I2c Pin Test']/SclGndVolt",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "None",
            "UNIT"          : "mV"
        },
        "SdaGndVolt":
        {
            "XML_PATH"      : "TestItems/Item[@name='I2c Pin Test']/SdaGndVolt",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "None",
            "UNIT"          : "mV"
        },
        "IntGndVolt":
        {
            "XML_PATH"      : "TestItems/Item[@name='Int Pin Test']/IntGndVolt",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "None",
            "UNIT"          : "mV"
        },
        "RstGndVolt":
        {
            "XML_PATH"      : "TestItems/Item[@name='Rst Pin Test']/RstGndVolt",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "None",
            "UNIT"          : "mV"
        },
        "SleepCurrent":
        {
            "XML_PATH"      : "TestItems/Item[@name='Sleep Current Test']/AVDD",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "None",
            "UNIT"          : "uA"
        },
        "ActiveCurrent":
        {
            "XML_PATH"      : "TestItems/Item[@name='Active Current Test']/AVDD",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "None",
            "UNIT"          : "uA"
        },
        "Version":
        {
            "XML_PATH"      : "TestItems/Item[@name='Version Test']/CurVerDataHex",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "fun_version",
            "UNIT"          : "Hex"
        },
        "CustomInfo":
        {
            "XML_PATH"      : "TestItems/Item[@name='Custom Information Process']/CustomInfoInFlash",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "fun_custom_info",
            "UNIT"          : "Hex"
        },
        "SensorId":
        {
            "XML_PATH"      : "TestItems/Item[@name='Sensor Id Test']/SenIdNum",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "None",
            "UNIT"          : "Hex"
        },
        "SaveResult":
        {
            "XML_PATH"      : "TestItems/Item[@name='Save result to ic storage']/TestResult",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "fun_save_result",
            "UNIT"          : "Hex"
        },
        "sen25_high":
        {
            "XML_PATH"      : "TestItems/Item[@name='Drv Sense as GIO Test']/J5-SI/pulledUpSelfRaw",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "fn_sen25",
            "UNIT"          : "Raw"
        },
        "sen25_low":
        {
            "XML_PATH"      : "TestItems/Item[@name='Drv Sense as GIO Test']/J5-SI/pulledDownSelfRaw",
            "ATTRIBUTE"     : "None",
            "FUNCTION"      : "fn_sen25",
            "UNIT"          : "Raw"
        },
        "RawMax_Max":
        {
            "XML_PATH"      : "TestItems/Item[@name='Rawdata Test Sets']/MaxRawTmpData",
            "ATTRIBUTE"     : "Maximum",
            "FUNCTION"      : "None",
            "UNIT"          : "Raw"
        },
        "RawMax_Min":
        {
            "XML_PATH"      : "TestItems/Item[@name='Rawdata Test Sets']/MaxRawTmpData",
            "ATTRIBUTE"     : "Minimum",
            "FUNCTION"      : "None",
            "UNIT"          : "Raw"
        },
        "RawMax_Avg":
        {
            "XML_PATH"      : "TestItems/Item[@name='Rawdata Test Sets']/MaxRawTmpData",
            "ATTRIBUTE"     : "Average",
            "FUNCTION"      : "None",
            "UNIT"          : "Raw"
        },
        "RawMin_Max":
        {
            "XML_PATH"      : "TestItems/Item[@name='Rawdata Test Sets']/MinRawTmpData",
            "ATTRIBUTE"     : "Maximum",
            "FUNCTION"      : "None",
            "UNIT"          : "Raw"
        },
        "RawMin_Min":
        {
            "XML_PATH"      : "TestItems/Item[@name='Rawdata Test Sets']/MinRawTmpData",
            "ATTRIBUTE"     : "Minimum",
            "FUNCTION"      : "None",
            "UNIT"          : "Raw"
        },
        "RawMin_Avg":
        {
            "XML_PATH"      : "TestItems/Item[@name='Rawdata Test Sets']/MinRawTmpData",
            "ATTRIBUTE"     : "Average",
            "FUNCTION"      : "None",
            "UNIT"          : "Raw"
        },
        "AccordMax_Max":
        {
            "XML_PATH"      : "TestItems/Item[@name='Rawdata Test Sets']/MaxAccordTmpData",
            "ATTRIBUTE"     : "Maximum",
            "FUNCTION"      : "None",
            "UNIT"          : "Raw"
        },
        "AccordMax_Min":
        {
            "XML_PATH"      : "TestItems/Item[@name='Rawdata Test Sets']/MaxAccordTmpData",
            "ATTRIBUTE"     : "Minimum",
            "FUNCTION"      : "None",
            "UNIT"          : "Raw"
        },
        "AccordMax_Avg":
        {
            "XML_PATH"      : "TestItems/Item[@name='Rawdata Test Sets']/MaxAccordTmpData",
            "ATTRIBUTE"     : "Average",
            "FUNCTION"      : "None",
            "UNIT"          : "Raw"
        }
    }
}
run_jsondata = {
    'FileName'                  : '',
    'CreatTime'                 : '',
    'ModifyTime'                : '',
    'ProgramName'               : '',
    'GtmVerion'                 : ''
}


def read_json_data(jsonfile):
    try:
        fd = open(jsonfile, 'r')
        jsonstr = fd.read()
        fd.close()
        jsondata = json.loads(jsonstr)
        return jsondata
    except Exception as e:
        logging.critical(e)
        logging.critical(jsonfile)
        return False
def write_json_file(jsonfile, jsondata):
    try:
        fd = open(jsonfile, 'w')
        data = json.dumps(jsondata, indent=4)
        fd.write(data)
        fd.close()
        return True
    except Exception as e:
        logging.critical(e)
        logging.critical(jsonfile)
        logging.critical(jsondata)
        return False

def get_xpath_text_from_tree(root, xpath):
    try:
        text = root.find(xpath).text
        if text == None:
            text = ''
    except Exception as e:
        logging.error(e)
        logging.error('xpath = %s' %(xpath))
        text = ''
    finally:
        return text
def get_xpath_attr_from_tree(root, xpath, attrib):
    try:
        text = root.find(xpath).attrib[attrib]
        if text == None:
            text = ''
    except Exception as e:
        logging.error(e)
        logging.error('xpath = %s, attrib = %s' %(xpath, attrib))
        text = ''
    finally:
        return text


def fn_sen25(text):
    values = [int(x) for x in text.split(',') if x!='']
    retval = str(sum(values)/len(values))
    return retval
def fun_version(text):
    retval = text.replace('0x','').replace(',','').replace('\t','').replace('\n','')
    return retval
def fun_custom_info(text):
    retval = text[:-1].replace(' ', '').replace(',','_')
    return retval
def fun_save_result(text):
    retval = text[1:].replace(' ', '').replace(',','_')
    return retval



def make_log_path(log_default_path, product_name, lot_id):
    try:
        log_path = log_default_path+'\\'+product_name+'\\'+lot_id
        if not os.path.exists(log_path):
            os.makedirs(log_path)
            logging.info('make_log_path %s.' %log_path)
        return log_path
    except Exception as e:
        logging.critical(e)
        return log_default_path
def check_filename(filename, test_program, tool_version):
    now_ticks = time.time()
    creat_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    try:
        run_log_info = read_json_data(run_log)
        # print(json.dumps(run_log_info, indent=4))
        if filename == run_log_info['FileName']:
            if test_program == run_log_info['ProgramName']:
                if tool_version == run_log_info['GtmVerion']:
                    last_modify_ticks = float(run_log_info['ModifyTime'])
                    if (now_ticks - last_modify_ticks) < 600:  # 10 min
                        run_log_info['ModifyTime'] = str(now_ticks)
                        creat_time = run_log_info['CreatTime']
                        write_json_file(run_log, run_log_info)
                        return filename+'_'+creat_time+'.csv'
        run_log_info['FileName'] = filename
        run_log_info['CreatTime'] = creat_time
        run_log_info['ModifyTime'] = str(now_ticks)
        run_log_info['ProgramName'] = test_program
        run_log_info['GtmVerion'] = tool_version
        if os.path.exists(run_log):
            shutil.copyfile(run_log, run_log+'.backup')
        write_json_file(run_log, run_log_info)
        logging.info('new_log_file %s.' %(filename+'_'+creat_time+'.csv'))
        return filename+'_'+creat_time+'.csv'   
    except Exception as e:
        logging.critical(e)
        return filename+'_'+creat_time+'.csv'
def get_bin(root, cfg):
    try:
        hwbin = cfg['HardBin']['ALL_PASS']
        swbin = cfg['SoftBin']['ALL_PASS']
        items = root.findall('ItemList/Item')
        for item in items:
            if item.attrib['result']=='NG':
                name = item.attrib['name']
                hwbin = cfg['HardBin'][name]
                subitems = item.findall('subItem')
                if len(subitems) == 0:
                    swbin = cfg['SoftBin'][name]
                    return hwbin,swbin
                else:
                    for subitem in subitems:
                        if subitem.attrib['result']=='NG':
                            swbin = cfg['SoftBin'][subitem.attrib['name']]
                            return hwbin,swbin
            elif item.attrib['result']=='UNKNOW':
                hwbin = cfg['HardBin']['UNKNOW']
                swbin = cfg['SoftBin']['UNKNOW']

        return hwbin,swbin
    except Exception as e:
        logging.critical(e)
        return "60",'1000'
def write_test_date_1st(fd_log, root, cfg):
    testdate = get_xpath_attr_from_tree(root, "Header/Time", "Date")
    testtime = get_xpath_attr_from_tree(root, "Header/Time", "Start")
    testdatetime = testdate.replace('/', '-') + ' ' + testtime.split(' ')[0]
    usetime = get_xpath_attr_from_tree(root, "Header/Time", "TotalTime")
    IcUid = get_xpath_text_from_tree(root, "Header/IcUid")
    if IcUid != '':
        IcUid = '0x'+IcUid
    Barcode = get_xpath_text_from_tree(root, "Header/Barcode")
    if Barcode != '':
        Barcode = '0x'+Barcode
    hwbin,swbin = get_bin(root, cfg)
    fd_log.write(testdatetime+',-1024,-1024,0,'+hwbin+','+swbin+','+IcUid+','+Barcode+','+usetime)
def write_test_data_2nd(fd_log, root, cfg):
    test_data_name_list =[]
    items = root.findall('ItemList/Item')
    for item in items:
        test_item_name = item.attrib['name']
        test_data_name_list = test_data_name_list + cfg['TestItem'][test_item_name]
    test_data_value = {}
    for test_data_name in cfg['TestData']:
        test_data_value[test_data_name] = ''
    for test_data_name in test_data_name_list:
        cfgitem = cfg['TestData'][test_data_name]
        if cfgitem['ATTRIBUTE'] == 'None':
            value = get_xpath_text_from_tree(root, cfgitem['XML_PATH'])
        else:
            value = get_xpath_attr_from_tree(root, cfgitem['XML_PATH'], cfgitem['ATTRIBUTE'])
        if cfgitem['FUNCTION'] != 'None' and value != '':
            value = eval(cfgitem['FUNCTION'])(value)
        test_data_value[test_data_name] = value
    for test_data_name in cfg['TestData']:
        fd_log.write(','+test_data_value[test_data_name])


def mtlog(file):
    try:
        cfg = cfg_jsondata
        # print(json.dumps(cfg, indent=4))
        if not os.path.exists(run_log):
            write_json_file(run_log, run_jsondata)

        try:
            fd = open(file, 'r')
            data = fd.read()
            fd.close()
            root = ET.fromstring(data)
        except Exception as e:
            logging.critical(e)
            logging.critical(file)
            return

        product_name = os.path.basename(file).split('_')[0]
        lot_id = get_xpath_text_from_tree(root, "Header/BatchNo")
        test_station = get_xpath_text_from_tree(root, "Header/StationName")	
        test_mode = 'ST'
        test_program = get_xpath_text_from_tree(root, "Header/OrderName")
        test_program_version = test_program.split('.')[-2].split('_')[-1]
        factoryNum = test_program.split('_')[4]
        if factoryNum in factory_jsondata:
            factory = factory_jsondata[factoryNum]
        else:
            factory = 'UNKNOW'
        ic_name = get_xpath_text_from_tree(root, "Header/DeviceType")
        handler_id = ''	
        tester_id = ''	
        todaytime = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime())
        operator_id = get_xpath_text_from_tree(root, "Header/WorkerId")
        board_version = get_xpath_text_from_tree(root, "Header/BoardVersion")	
        tool_version = get_xpath_text_from_tree(root, "Header/ToolVersion")

        log_path = make_log_path(log_default_path, product_name, lot_id)
        # print(log_path)
        filename = product_name+'_'+test_station+'_'+test_mode+'_'+test_program_version+'_'+ic_name+'_'+lot_id+'_'+handler_id+'.'+tester_id
        filename = check_filename(filename, test_program, tool_version)
        # print(filename)
        log_file =log_path+'\\'+filename
        logging.debug(log_file)

        if not os.path.exists(log_file):
            fd_log = open(log_file, 'w')
            fd_log.write(   'WorkOrder = ' +
                            ',ProductName = ' + product_name +
                            ',IcName = ' + ic_name +
                            ',Lot_Id = ' + lot_id +
                            ',TestPrg = ' + test_program +
                            ',Handler_Id = ' + handler_id +
                            ',Tester_Id = ' + tester_id +
                            ',Operator_Id = ' + operator_id +
                            ',Factory = ' + factory +
                            ',Date = ' + todaytime +
                            ',Form = Modlue' +
                            ',BoardVersion = ' + board_version +
                            ',ToolVersion = ' + tool_version + '\n')
            name = ['TestTime','X_POS','Y_POS','SITE','HW_BIN','SW_BIN','UID','SN','UseTime']
            unit = [' ',' ',' ',' ',' ',' ',' ',' ','Str']
            for item in cfg['TestData']:
                name.append(item)
                unit.append(cfg['TestData'][item]['UNIT'])
            name.append('FileName')
            unit.append('Str')
            fd_log.write(','.join(name)+'\n')
            fd_log.write(','.join(unit)+'\n')
        else:
            fd_log = open(log_file, 'a+')
        
        write_test_date_1st(fd_log, root, cfg)
        write_test_data_2nd(fd_log, root, cfg)
        fd_log.write(','+os.path.basename(file)+'\n')
        
        fd_log.close()
    except Exception as e:
        logging.critical(e)
        logging.critical(file)


if __name__ == '__main__':
    import tkinter.filedialog
    testlogdir = tkinter.filedialog.askdirectory(title='select dir', initialdir='.//')
    def enum_files(dir):
        testlogfiles = []
        g = os.walk(dir)
        for path, dir_list, file_list in g:
            for file_name in file_list:
                testlogfiles.append(os.path.join(path, file_name))
        for sub_dir in dir_list:
            testlogfiles = testlogfiles+enum_files(sub_dir)
        return testlogfiles
    files = enum_files(testlogdir)

    # files = [r'E:\eclipse-workspace\Python2021\2021-Jun-27\OK\GTM1510_GT7863_No0_01138_FE2FF_8SST60R38059J1KS16T0048_20210627_140312_OK.csv']
    for file in files:
        print(file)
        mtlog(file)

    print('\n\n!!!run ending!!!\n')
