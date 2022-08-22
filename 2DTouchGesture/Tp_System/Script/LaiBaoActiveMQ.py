# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import json
import time
import datetime
import logging
import stomp
import os
import xml.etree.ElementTree as ET
import socket

site_name = '1000'  # 固定值:重庆莱宝工厂标识
device_code = 'TESTRS03'  # 站点: 固定值:当前的设备编号
process_code = 'OP01'  # 工序编号: 固定值:当前的工序编号
message_type1 = 'machine.startsfccheck.process'  # 接口类型: 固定值:接口类型
message_type2 = 'machine.sn.testdata.process'  # 接口类型: 固定值:接口类型

ActiveMQ_ip = '172.16.1.115'
ActiveMQ_port = 61613
ActiveMQ_username = 'admin'
ActiveMQ_password = 'admin'
send_queue_name1 = '/queue/machine.startsfccheck.process'
recv_queue_name1 = '/queue/second.queue'
send_queue_name2 = '/queue/machine.sn.testdata.process'
recv_queue_name2 = '/queue/second.queue'
# send_queue_name = '/queue/first.queue'
# recv_queue_name = '/queue/second.queue'


g_resp_json_str = ''
g_cur_guid_str = ''
g_fw_ver = ''

test_guid_on = False
gtm_server_port = 16688

def log():
    logger = logging.getLogger("gtm")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        fh = logging.FileHandler("gtm_py.log", encoding="utf-8")
        ch = logging.StreamHandler()

        formatter = logging.Formatter(
            fmt = "%(asctime)s %(name)s %(filename)s %(message)s",
            datefmt="%Y/%m/%d %X"
        )

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger


def output_log(msg):
    logger = log()
    logger.info(msg);
    # logger.warning("gtm py warning")
    # logger.error("gtm py error")


def get_time_now_with_java_format():
    time_str = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return time_str[0:19]


def make_guid(before_test):
    # date_str = time.strftime("%Y%m%d", time.localtime())
    time_str = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')
    prefix_str = ''
    if before_test:
        prefix_str = 'GOODIX_BEFORE'
    else:
        prefix_str = 'GOODIX_AFTER'

    guid_str = prefix_str + '_' + time_str
    # just for test
    if test_guid_on:
        guid_str = 'GOODIX_BEFORE_2021/07/26 17:07:38.039212'

    return guid_str


def make_check_before_test_packet(worker_id, order_name_without_ext, gtm_ver, fw_ver, barcode):
    guid_str = make_guid(True)
    data = {
        "MESSAGE_TYPE": message_type1,  # 固定值:重庆莱宝工厂标识
        "GUID": guid_str,  # 唯一标识: 自动生成唯一标识码（如标识码_YYYYMMDD+流水码）
        "SITE": site_name,  # 固定值:重庆莱宝工厂标识
        "USER_ID": worker_id,  # 站点: 固定值:作业员编号
        "RESOURCE": device_code,  # 设备编号: 固定值:当前的设备编号
        "OPERATION": process_code,  # 工序编号: 固定值:当前的工序编号
        "SEND_TIME": get_time_now_with_java_format(),  # 发送时间: yyyy/MM/dd HH:mm:ss
        "CONFIGURATION_FILE_NAME": order_name_without_ext,  # 配置文件名称(即不含.tporder后缀的工单文件名)
        "SW_VERSION": gtm_ver,  # 软件版本: GTM测试软件版本  例:GTLib1.14.0.0.18
        "FW_VERSION": fw_ver,  # 软件版本: 固件版本, 可为空   例:NOR_L-00.00.0D_7863_0A.01.05.11
        "SFC": barcode  # 扫描编号: 产品条码
    }

    req_json_str = json.dumps(data)
    output_log("Python 原始数据：%s" % repr(data))
    output_log("JSON 对象：%s" % req_json_str)

    return req_json_str, guid_str


def make_report_after_test_packet(worker_id, barcode, result, error_code, test_begin_time, test_end_time, order_name, gtm_ver, fw_ver):

    test_info = []
    test_info_item1 = {
        "PARAMETER_NAME": "CONFIGURATION_FILE_NAME",  # 配置文件名称(即不含.tporder后缀的工单文件名)
        "ACTUAL_VALUE": order_name,
        "DATA_TYPE": "TEXT"
    }
    test_info_item2 = {
        "PARAMETER_NAME": "SW_VERSION",  # 软件版本: GTM测试软件版本
        "ACTUAL_VALUE": gtm_ver,
        "DATA_TYPE": "TEXT"
    }
    test_info_item3 = {
        "PARAMETER_NAME": "FW_VERSION",  # 软件版本: 固件版本, 可为空
        "ACTUAL_VALUE": fw_ver,
        "DATA_TYPE": "TEXT"
    }
    test_info.append(test_info_item1)
    test_info.append(test_info_item2)
    test_info.append(test_info_item3)

    guid_str = make_guid(False)
    data = {
        "MESSAGE_TYPE": message_type2,  # 固定值:重庆莱宝工厂标识
        "GUID": guid_str,  # 唯一标识: 自动生成唯一标识码（如标识码_YYYYMMDD+流水码）
        "SITE": site_name,  # 固定值:重庆莱宝工厂标识
        "RESOURCE": device_code,  # 设备编号: 固定值:当前的设备编号
        "OPERATION": process_code,  # 工序编号: 固定值:当前的工序编号
        "SFC": barcode,  # 扫描编号: 产品条码
        "USER_ID": worker_id,  # 站点: 固定值:作业员编号
        "RESULT": result,  # 结果: OK/NG
        "ERROR_CODE": error_code,  # 英文逗号分隔的错误码
        "SEND_TIME": get_time_now_with_java_format(),  # 发送时间: yyyy/MM/dd HH:mm:ss
        "TEST_FROM_TIME": test_begin_time,  # 检测开始时间:yyyy-MM-dd HH:mm:ss
        "TEST_TO_TIME": test_end_time,  # 检测结束时间:yyyy-MM-dd HH:mm:ss
        "TEST_INFO": test_info
    }

    req_json_str = json.dumps(data)
    output_log("Python 原始数据：%s" % repr(data))
    output_log("JSON 对象：%s" % req_json_str)

    return req_json_str, guid_str


# class MyListener(stomp.ConnectionListener):
class MyListener(object):
    def on_error(self, frame):
        output_log('Error: "%s"' % frame.body)

    def on_message(self, frame):
        global g_resp_json_str
        output_log('ActiveMQ reply: "%s"' % frame.body)
        resp_data = json.loads(frame.body)
        if 'GUID' in resp_data and 'RESULT' in resp_data and 'MESSAGE' in resp_data:
            if resp_data['GUID'] == g_cur_guid_str:
                g_resp_json_str = frame.body
                output_log('Reply is effective')
                output_log(g_resp_json_str)
            else:
                output_log('Error: reply guid, recved[%s], expect[%s]' % (resp_data['GUID'], g_cur_guid_str))
        else:
            output_log('Error: reply invalid: %s' % frame.body)


def parse_result_csv_file(result_csv_file):
    if os.path.exists(result_csv_file) is False or os.path.isfile(result_csv_file) is False:
        output_log("Error: result file not exist")
        return False, "", "", "", "", "", ""

    try:
        utf8_parser = ET.XMLParser(encoding='utf-8')
        tree = ET.parse(result_csv_file, parser=utf8_parser)
        root = tree.getroot()
    except Exception as e:
        output_log("Error: parse result csv file failed: %s" % result_csv_file)
        output_log("Exception : %s" % e.__str__())
        return False, "", "", "", "", "", ""

    test_result_node = root.find('Header/Result')
    test_result = test_result_node.text

    test_time_node = root.find('Header/Time')
    date_str = test_time_node.attrib.get('Date')

    str_start = test_time_node.attrib.get('Start')
    str_end = test_time_node.attrib.get('End')

    test_start_time = date_str + " " + str_start[0:8]
    test_end_time = date_str + " " + str_end[0:8]

    tool_version_node = root.find('Header/ToolVersion')
    gtm_ver = tool_version_node.text

    order_name_node = root.find('Header/OrderName')
    order_name = order_name_node.text

    order_name = order_name.lower()
    if order_name.endswith('.tporder') is False:
        output_log("order suffix wrong")
        return False, "", "", "", "", "", ""

    order_name_without_ext = order_name[0:-8]

    error_code_list = ''

    for item_head in root.findall(".//ItemHeader"):
        test_item_id = ''
        test_item_result = ''
        test_item_error_code = ''
        for item in item_head:
            if item.tag == 'TestResult':
                test_item_result = item.text
            elif item.tag == 'TestId':
                test_item_id = item.text
            elif item.tag == 'TestItemErrCode':
                test_item_error_code = item.text

        if test_item_result != "0":
            item_err_code = test_item_id + "|(" + test_item_error_code + "),"
            error_code_list = error_code_list + item_err_code

    return True, order_name_without_ext, gtm_ver, test_result, error_code_list, test_start_time, test_end_time


def show_err_in_gtm(guid_str, err_msg):
    data = {
        "guid": guid_str,
        "time": datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f'),  # "2021/07/26 16:09:00",
        "function": "show_ui_message",
        "devId": 0,
        "msgType": 1,
        "testTag": "ERROR",
        "title": "",
        "msg": err_msg
    }

    req_json_str = json.dumps(data)

    # Socket to talk to server
    output_log("Connecting to GTM server...")
    client = socket.socket()
    client.connect(("127.0.0.1", gtm_server_port))
    # client.send(bytes(req_json_str, encoding='utf-8'))
    client.sendall(bytes(req_json_str, encoding='utf-8'))
    output_log("data sent : GTM ui show error message")
    data = client.recv(4096)
    output_log('GTM reply: %s' % data.decode())
    #time.sleep(1)
    client.close()


def check_before_test(worker_id, order_name, gtm_version, fw_version, barcode):

    output_log("----------------start [check before test]----------------------\n")

    order_name_without_ext = order_name[0:-8]
    packet_str,guid = make_check_before_test_packet(worker_id, order_name_without_ext, gtm_version, fw_version, barcode)
    output_log("GTM request:")
    output_log(packet_str)

    conn = stomp.Connection([(ActiveMQ_ip, ActiveMQ_port)], auto_content_length=False)
    conn.set_listener('', MyListener())
    conn.connect(ActiveMQ_username, ActiveMQ_password, wait=True)
    # conn.subscribe(destination=recv_queue_name, id=1, ack='auto')
    conn.subscribe(destination=recv_queue_name1, id=1, ack='auto')

    global g_resp_json_str
    g_resp_json_str = ''
    global g_cur_guid_str
    g_cur_guid_str = guid

    conn.send(body=packet_str, destination=send_queue_name1)

    dt_begin = datetime.datetime.now()
    dt_now = datetime.datetime.now()
    while len(g_resp_json_str) == 0 and (dt_now - dt_begin).seconds <= 3 :
        time.sleep(0.1)
        dt_now = datetime.datetime.now()

    output_log("\n")

    if len(g_resp_json_str) != 0:
        output_log("ActiveMQ reply:")
        output_log(g_resp_json_str)
        resp_data = json.loads(g_resp_json_str)
        # print('''"GUID":"'''+resp_data['GUID']+'''"''')
        # print('''"RESULT":"'''+resp_data['RESULT']+'''"''')
        # print('''"MESSAGE":"'''+resp_data['MESSAGE']+'''"''')
        ret_guid = resp_data['GUID']
        ret_result = resp_data['RESULT']
        ret_message = resp_data['MESSAGE']

        if ret_guid != g_cur_guid_str:
            output_log('Error: reply guid, recved[%s], expect[%s]' % (ret_guid, g_cur_guid_str))
        else:
            if ret_result == 'NG':
                output_log('reply result is NG')
                show_err_in_gtm(g_cur_guid_str, ret_message)
            else:
                output_log('ActiveMQ reply OK')
                # show_err_in_gtm(g_cur_guid_str, ret_message)
                global g_fw_ver
                g_fw_ver = fw_version
    else:
        output_log('Error: No ActiveMQ reply\n')
        show_err_in_gtm(g_cur_guid_str, "no ActiveMQ reply received")

    conn.disconnect()
    output_log("----------------end-- [check before test]----------------------")


def report_after_test(worker_id, barcode, result_csv_file):

    b_parse_ok, order_name_without_ext, gtm_ver, test_result, error_code_list, test_begin_time, test_end_time \
        = parse_result_csv_file(result_csv_file)

    if b_parse_ok is not True:
        output_log('Error: parse result csv file failed')
        return

    output_log("----------------start [report after test]----------------------\n")

    packet_str, guid = make_report_after_test_packet(worker_id, barcode, test_result, error_code_list, test_begin_time,
                                                     test_end_time, order_name_without_ext, gtm_ver, g_fw_ver)
    output_log("GTM request:")
    output_log(packet_str)

    conn = stomp.Connection([(ActiveMQ_ip, ActiveMQ_port)], auto_content_length=False)
    conn.set_listener('', MyListener())
    conn.connect(ActiveMQ_username, ActiveMQ_password, wait=True)
    # conn.subscribe(destination=recv_queue_name, id=1, ack='auto')
    conn.subscribe(destination=recv_queue_name2, id=1, ack='auto')

    global g_resp_json_str
    g_resp_json_str = ''
    global g_cur_guid_str
    g_cur_guid_str = guid

    conn.send(body=packet_str, destination=send_queue_name2)

    dt_begin = datetime.datetime.now()
    dt_now = datetime.datetime.now()
    while len(g_resp_json_str) == 0 and (dt_now - dt_begin).seconds <= 3:
        time.sleep(0.1)
        dt_now = datetime.datetime.now()

    output_log("\n")

    if len(g_resp_json_str) != 0:
        output_log("ActiveMQ reply:")
        output_log(g_resp_json_str)
        resp_data = json.loads(g_resp_json_str)
        # print('''"GUID":"'''+resp_data['GUID']+'''"''')
        # print('''"RESULT":"'''+resp_data['RESULT']+'''"''')
        # print('''"MESSAGE":"'''+resp_data['MESSAGE']+'''"''')
        ret_guid = resp_data['GUID']
        ret_result = resp_data['RESULT']
        ret_message = resp_data['MESSAGE']

        if ret_guid != g_cur_guid_str:
            output_log('Error: reply guid, recved[%s], expect[%s]' % (ret_guid, g_cur_guid_str))
        else:
            if ret_result == 'NG':
                output_log('reply result is NG')
                show_err_in_gtm(g_cur_guid_str, ret_message)
            else:
                output_log('ActiveMQ reply OK')

    else:
        output_log('Error:No ActiveMQ reply\n')
        show_err_in_gtm(g_cur_guid_str, "no ActiveMQ reply received")

    conn.disconnect()
    output_log("----------------end-- [report after test]----------------------")


def send_a_test_activemq_response_message():
    conn = stomp.Connection([(ActiveMQ_ip, ActiveMQ_port)], auto_content_length=False)
    conn.connect(ActiveMQ_username, ActiveMQ_password, wait=True)

    if test_guid_on:
        guid_str = 'GOODIX_BEFORE_2021/07/26 17:07:38.039212'

    data = {
        "GUID": g_cur_guid_str,
        "RESULT": "OK",
        "MESSAGE": "允许进站",
    }

    req_json_str = json.dumps(data)
    conn.send(body=req_json_str, destination=recv_queue_name)


if __name__ == '__main__':
    send_a_test_activemq_response_message()
    # check_before_test("woker9527", "GTM1510_DEBUG_20210624_V0001.tporder", "GTLib1.14.0.0.18", "NOR_L-00.00.0D_7863_0A.01.05.11", "barcode00001")
    report_after_test("woker9527", "barcode00001", "D:\\Code\\GTM-devtp-public-LaibaoActiveMQ\\Debug\\TestResult\\GT7863_所有项压测_repeat_1.14.0.7_20210108(2)\\2021-Jul-26\\NG\\GT7863_No0_01387_E70FF_20210726_173207_NG.csv")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
