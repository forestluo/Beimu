# -*- coding: utf-8 -*
import time
import serial
import struct

from crcmod import mkCrcFun
from serial.tools import list_ports

class Modbus:
    # 串口设备名
    # Win32上缺省为COM3
    # Raspberry上缺省为ttyUSB0
    __portName = None
    # 485通讯控制方式时（拨码开关第 8 位为 ON）
    # 波特率默认为9600bps，数据位为 8位，偶校验，停止位为1位；
    # 波特率
    __baudrate = 9600
    # 数据位
    __bytesize = serial.EIGHTBITS
    # 校验
    __parity = serial.PARITY_EVEN
    # 停止位
    __stopbits = serial.STOPBITS_TWO
        
    # 检查Debug
    @property
    def debug(self):
        return False
        
    # 定义构造函数
    def __init__(self, name):
        # 设置设备名
        self.__portName = name
        # 检查设备名
        if Modbus.name_exists(name) is False:
            # 打印信息
            print("Modbus:__init__ : invalid name(%s) !"%name)
            return
         
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
            print("Modbus:list_ports : no serial ports !")

    # 检查串口设备名
    def name_exists(name):
        # 列举设备
        portList = \
            list(serial.tools.list_ports.comports())
        # 检查结果
        if len(portList) <= 0:
            # 打印信息
            print("Modbus:name_exists : no serial ports !")
        
        # 列举设备名
        portNames = list(portList[0])
        # 检查列表
        if name in portNames: return True
        else:
            # 打印信息
            print("Modbus:name_exists : no such port(%s) !"%name)
        return False

    # 串口设备错误信息
    def error_info(code):
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

    # 读取寄存器
    def read(self, addr, start, count):
        # 打印信息
        if (self.debug): print("Modbus.read : begin !")
        # 拼接命令字
        buffer = struct.pack(">BBHH", addr, 0x03, start, count)
        # 打印信息
        if (self.debug):
            print("\tcmd = 0x03")
            print("\taddr = 0x%02x"%addr)
            print("\tstart = 0x%02x"%start)
            print("\tcount = %u"%count)
        # 计算CRC16结果
        crc16 = mkCrcFun(0x18005, rev = True,
                initCrc = 0xFFFF, xorOut = 0x0000)
        output = crc16(buffer)
        # 打印信息
        if (self.debug): print("\tcrc16 = 0x%02x"%output)
        # 拼接RTU
        buffer = struct.pack("<6BH", *buffer, output)
        # 打印信息        
        if (self.debug): print("\tbytes = 0x%s"%buffer.hex())
        
        try:
            # 打开设备
            serialPort = serial.Serial(
                        port = self.__portName,
                        baudrate = self.__baudrate,
                        bytesize = self.__bytesize,
                        parity = self.__parity,
                        stopbits = self.__stopbits,
                        timeout = 0.5)
            # 打印信息
            if (self.debug): \
                print("Modbus.read : port was opened !")
            # 向串口输出
            serialPort.write(buffer)
            # 打印信息
            if (self.debug): \
                print("Modbus.read : send request !")
            # 等待必要的时间
            time.sleep(0.1)
            # 从串口读取
            input = serialPort.read_all()
            # 打印信息
            if (self.debug): \
                print("Modbus.read : receive response !")
            # 关闭串口
            serialPort.close()
            # 打印信息
            if (self.debug): \
                print("Modbus.read : port was closed !")
            # 检查反馈结果
            if input is None or len(input) < 5:
                # 打印信息
                if (self.debug): \
                    print("Modbus.read : invalid response !")
                return None
            # 打印信息
            if (self.debug): \
                print("\tbytes[%d] = 0x%s"%(len(input), input.hex()))

        except Exception as e:
            print("Modbus:read :", str(e))
            print("Modbus:read : unexpected exit !")
            # 返回结果
            return None
                        
        # 计算CRC校验
        value = crc16(input[ : len(input) - 2])
        # 检查CRC校验
        if input[len(input) - 2] != (value & 0xFF) or \
            input[len(input) - 1] != ((value >> 8) & 0xFF):
            # 打印信息
            if (self.debug): \
                print("Modbus.read : invalid CRC16 !")
        # 打印信息
        if (self.debug): print("\tcrc16 = 0x%02x"%value)
            
        # 检查从站地址
        if input[0] != addr:
            # 打印信息
            if (self.debug): \
                print("Modbus.read : invalid addr(0x%02x) !"%input[0])
        # 打印信息
        if (self.debug): print("\taddr = 0x%02x"%input[0])
        
        # 打印信息
        if (self.debug): print("\tcmd = 0x%02x"%input[1])
        # 检查反馈指令
        if input[1] == 0x83:
            # 打印错误信息
            if (self.debug): \
                print("\terror = 0x%02x (%s)"% \
                    (input[2], Modbus.error_info(input[2])))
            return None
            
        # 检查反馈指令
        if input[1] != 0x03:
            # 打印信息
            if (self.debug): \
                print("Modbus.read : invalid cmd(0x%02x) !"%input[1])
            return None
        
        # 打印信息
        if (self.debug): print("\tlen = %u"%input[2])
        # 检查数据长度
        if input[2] < 2 or ((input[2] % 2) != 0):
            # 打印信息
            if (self.debug): \
                print("Modbus.read : invalid len(%d) !"%input[2])
            return None
        # 截取数据字节
        input = input[3 : len(input) - 2]
        # 打印数据字节
        if (self.debug): print("\tbytes = 0x%s"%input.hex())
        # 返回结果
        return input

    # 写入寄存器
    def write(self, addr, start, buffer):
        # 确认数据长度
        assert(len(buffer) % 2 == 0)
        # 打印信息
        if (self.debug): print("Modbus.write : begin !")
        # 必须是偶数个字节
        data_len = len(buffer)
        # 寄存器数量
        count = data_len // 2
        # 打印信息
        if (self.debug): \
            print("\tdata[%d] = 0x%s"%(data_len, buffer.hex()))
        # 检查长度
        if data_len == 2:
            # 按照单个寄存器读写处理
            buffer = struct.pack("!BBH", addr, 0x06, start) + buffer
        else:
            # 按照多个寄存器读写处理
            buffer = struct.pack("!BBHHB", addr, 0x10, start, count, data_len) + buffer
        # 计算CRC16结果
        crc16 = mkCrcFun(0x18005, rev = True,
                initCrc = 0xFFFF, xorOut = 0x0000)
        value = crc16(buffer)
        # 打印信息
        if (self.debug): print("\tcrc16 = 0x%02x"%value)
        # 组合数据包
        buffer = buffer + struct.pack("<H", value)
        # 打印信息
        if (self.debug): print("\tbytes[%d] = 0x%s"%(data_len, buffer.hex()))

        try:
            # 打开设备
            serialPort = serial.Serial(
                        port = self.__portName,
                        baudrate = self.__baudrate,
                        bytesize = self.__bytesize,
                        parity = self.__parity,
                        stopbits = self.__stopbits,
                        timeout = 0.5)
            # 打印信息
            if (self.debug): \
                print("Modbus.write : port was opened !")
            # 向串口输出
            serialPort.write(buffer)
            # 打印信息
            if (self.debug): \
                print("Modbus.write : send request !")
            # 等待必要的时间
            time.sleep(0.1)
            # 从串口读取
            input = serialPort.read_all()
            # 打印信息
            if (self.debug): \
                print("Modbus.write : receive response !")
            # 关闭串口
            serialPort.close()
            # 打印信息
            if (self.debug): \
                print("Modbus.write : port was closed !")
            # 检查反馈结果
            if input is None or len(input) < 5:
                # 打印信息
                if (self.debug): \
                    print("Modbus.write : invalid response !")
                return False
            # 打印信息
            if (self.debug): \
                print("\tbytes[%d] = 0x%s"%(len(input), input.hex()))

        except Exception as e:
            print("Modbus:write :", str(e))
            print("Modbus:write : unexpected exit !")
            # 返回结果
            return False

        # 计算CRC校验
        value = crc16(input[ : len(input) - 2])
        # 检查CRC校验
        if input[len(input) - 2] != (value & 0xFF) or \
            input[len(input) - 1] != ((value >> 8) & 0xFF):
            # 打印信息
            if (self.debug): \
                print("Modbus.write : invalid CRC16 !")
            return False
        # 打印信息
        if (self.debug): print("\tcrc16 = 0x%02x"%value)

        # 检查从站地址
        if input[0] != addr:
            # 打印信息
            if (self.debug): \
                print("Modbus.write : invalid addr(0x%02x) !"%input[0])
            return False
        # 打印信息
        if (self.debug): print("\taddr = 0x%02x"%input[0])

        # 打印信息
        if (self.debug): print("\tcmd = 0x%02x"%input[1])
        # 检查数据长度
        if data_len == 2:
            # 检查反馈指令
            if input[1] == 0x86:
                # 打印错误信息
                if (self.debug): 
                    print("\terror = 0x%02x (%s)"%(input[2], \
                        Modbus.error_info(input[2])))
                return False

            # 检查反馈指令
            if input[1] != 0x06:
                # 打印信息
                if (self.debug): \
                    print("Modbus.write : invalid cmd(0x%02x) !"%input[1])
                return False
            
            # 检查输入字节是否与输出字节一致
            if input != buffer:
                # 打印信息
                if (self.debug): \
                    print("Modbus.write : response is not as same as output !")
                return False
            
        else:
            # 检查反馈指令
            if input[1] == 0x90:
                # 打印错误信息
                if (self.debug): \
                    print("\terror = 0x%02x (%s)"%(input[2], \
                        Modbus.error_info(input[2])))
                return False

            # 检查反馈指令
            if input[1] != 0x10:
                # 打印信息
                if (self.debug): \
                    print("Modbus.write : invalid cmd(0x%02x) !"%input[1])
                return False
            
            # 检查输入字节是否与输出字节一致
            if input[:6] != buffer[:6]:
                # 打印信息
                if (self.debug): \
                    print("Modbus.write : response is not as same as output !")
                return False
        # 返回结果
        return True