# -*- coding: utf-8 -*

import serial
import serial.tools
import serial.tools.list_ports

import traceback

from crcmod import mkCrcFun
from serial.tools import list_ports

class SerialPort:
    # 串口设备名
    __portName = None
    # 波特率默认为9600bps，数据位为 8位，无校验，停止位为1位；
    # 波特率
    __baudrate = 9600
    # 数据位
    __bytesize = serial.EIGHTBITS
    # 校验
    __parity = serial.PARITY_NONE
    # 停止位
    __stopbits = serial.STOPBITS_ONE
        
    # 检查Debug
    @property
    def debug(self):
        return False

    # 定义构造函数
    def __init__(self, name):
        # 设置设备名
        self.__portName = name
        # 检查设备名
        if SerialPort.name_exists(name) is False:
            # 打印信息
            print("SerialPort:__init__ : invalid name(%s) !"%name)
            return

    # 设置串口
    def _set_port(self, baudrate, \
            bytesize, parity, stopbits):
        # 设置串口参数
        self.__baudrate = baudrate
        self.__bytesize = bytesize
        self.__parity = parity
        self.__stopbits = stopbits

    # 打开串口
    def open_port(self):
        # 打印信息
        if (self.debug):
            print("SerialPort.open_port : try to open !")
            print("\tport_name = %s"%self.__portName)
            print("\tbaudrate = %d"%self.__baudrate)
            print("\tbytesize = %d"%self.__bytesize)
            print("\tparity = %s"%self.__parity)
            print("\tstopbits = %d"%self.__stopbits)
        # 打开设备
        serialPort = serial.Serial(
                    port = self.__portName,
                    baudrate = self.__baudrate,
                    bytesize = self.__bytesize,
                    parity = self.__parity,
                    stopbits = self.__stopbits,
                    timeout = 0.5)
        # 打印信息
        if (self.debug):
            print("SerialPort.open_port : port was opened !")
        # 返回设备
        return serialPort
    
    # 列举所有串口
    def list_ports():
        # 列举设备
        portList = \
            list(serial.tools.list_ports.comports())
        # 检查结果
        if len(portList) > 0:
            # 打印信息
            print(*portList, sep = "\r\n")
        else:
            # 打印信息
            print("SerialPort:list_ports : no serial ports !")

    # 检查串口设备名
    def name_exists(name):
        # 列举设备
        portList = \
            list(serial.tools.list_ports.comports())
        # 检查结果
        if len(portList) <= 0:
            # 打印信息
            print("SerialPort:name_exists : no serial ports !")
            return False
        
        # 循环
        for i in range(0, len(portList)):
            # 转换
            portInfo = list(portList[i])
            # 检查名称
            if name == portInfo[0]: return True

        # 打印信息
        print("SerialPort:name_exists : no such port(%s) !"%name)
        return False

    # 串口设备错误信息
    def error_info(self, code):
        if code == 0x01: return "非法功能码"
        elif code == 0x02: return "非法数据地址"
        elif code == 0x03: return "非法数据值"
        elif code == 0x04: return "从站设备故障"
        elif code == 0x05: return "请求已被确认，但需要较长时间来处理请求"
        elif code == 0x06: return "从设备忙"
        elif code == 0x08: return "存储奇偶性差错"
        elif code == 0x0A: return "不可用的网关"
        elif code == 0x0B: return "网关目标设备响应失败"
        elif code == 0x40: return "禁止操作"
        elif code == 0x60: return "尚未学习电机相序"
        elif code == 0xff: return "未定义错误"
        else: return "未知错误代码"

# 定义主函数
def main():  

    # 打印所有串口
    SerialPort.list_ports()

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SerialPort:__main__ :", str(e))
        print("SerialPort:__main__ : unexpected exit !")
