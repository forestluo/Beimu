# -*- coding: utf-8 -*
import time
import struct

from SerialPort import *

from crcmod import mkCrcFun

# 串口设备名
# Win32上缺省为COM3
# Raspberry上缺省为ttyUSB0
class Modbus(SerialPort):

    # 定义构造函数
    def __init__(self, name):
        # 调用父函数
        SerialPort.__init__(self, name)

    # 检查属性
    @property
    def multi(self):
        # 是否区别多个和单个寄存器写入模式
        return True
    
    # 检查属性
    @property
    def wait_time(self):
        return 0.1

    # 读取寄存器
    def read_raw(self, addr, start, count):
        # 打印信息
        if (self.debug): print("Modbus.read_raw : begin !")
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
            serialPort = self.open_port()
            # 打印信息
            if (self.debug): \
                print("Modbus.read_raw : port was opened !")
            # 向串口输出
            serialPort.write(buffer)
            # 打印信息
            if (self.debug): \
                print("Modbus.read_raw : send request !")
            # 等待必要的时间
            if self.wait_time > 0 :
                time.sleep(self.wait_time)
            # 从串口读取
            input = serialPort.read_all()
            # 打印信息
            if (self.debug): \
                print("Modbus.read_raw : receive response !")
            # 关闭串口
            serialPort.close()
            # 打印信息
            if (self.debug): \
                print("Modbus.read_raw : port was closed !")
            # 检查反馈结果
            if input is None or len(input) < 5:
                # 打印信息
                if (self.debug): \
                    print("Modbus.read_raw : invalid response !")
                return None
            # 打印信息
            if (self.debug): \
                print("\tbytes[%d] = 0x%s"%(len(input), input.hex()))

        except Exception as e:
            print("Modbus:read_raw :", str(e))
            print("Modbus:read_raw : unexpected exit !")
            # 返回结果
            return None
                        
        # 计算CRC校验
        value = crc16(input[ : len(input) - 2])
        # 检查CRC校验
        if input[len(input) - 2] != (value & 0xFF) or \
            input[len(input) - 1] != ((value >> 8) & 0xFF):
            # 打印信息
            if (self.debug): \
                print("Modbus.read_raw : invalid CRC16 !")
        # 打印信息
        if (self.debug): print("\tcrc16 = 0x%02x"%value)
            
        # 检查从站地址
        if input[0] != addr:
            # 打印信息
            if (self.debug): \
                print("Modbus.read_raw : invalid addr(0x%02x) !"%input[0])
        # 打印信息
        if (self.debug): print("\taddr = 0x%02x"%input[0])
        
        # 打印信息
        if (self.debug): print("\tcmd = 0x%02x"%input[1])
        # 检查反馈指令
        if input[1] == 0x83:
            # 打印错误信息
            if (self.debug): \
                print("\terror = 0x%02x (%s)"% \
                    (input[2], self.error_info(input[2])))
            return None
            
        # 检查反馈指令
        if input[1] != 0x03:
            # 打印信息
            if (self.debug): \
                print("Modbus.read_raw : invalid cmd(0x%02x) !"%input[1])
            return None
        
        # 打印信息
        if (self.debug): print("\tlen = %u"%input[2])
        # 检查数据长度
        if input[2] < 2 or ((input[2] % 2) != 0):
            # 打印信息
            if (self.debug): \
                print("Modbus.read_raw : invalid len(%d) !"%input[2])
            return None
        # 截取数据字节
        input = input[3 : len(input) - 2]
        # 打印数据字节
        if (self.debug): print("\tbytes = 0x%s"%input.hex())
        # 返回结果
        return input

    # 写入寄存器
    def write_raw(self, addr, start, buffer):
        # 确认数据长度
        assert(len(buffer) % 2 == 0)
        # 打印信息
        if (self.debug): print("Modbus.write_raw : begin !")
        # 必须是偶数个字节
        data_len = len(buffer)
        # 寄存器数量
        count = data_len // 2
        # 打印信息
        if (self.debug): \
            print("\tdata[%d] = 0x%s"%(data_len, buffer.hex()))
        # 检查长度
        if data_len == 2 and self.multi:
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
            serialPort = self.open_port()
            # 打印信息
            if (self.debug): \
                print("Modbus.write_raw : port was opened !")
            # 向串口输出
            serialPort.write(buffer)
            # 打印信息
            if (self.debug): \
                print("Modbus.write_raw : send request !")
            # 等待必要的时间
            if self.wait_time > 0 :
                time.sleep(self.wait_time)
            # 从串口读取
            input = serialPort.read_all()
            # 打印信息
            if (self.debug): \
                print("Modbus.write_raw : receive response !")
            # 关闭串口
            serialPort.close()
            # 打印信息
            if (self.debug): \
                print("Modbus.write_raw : port was closed !")
            # 检查反馈结果
            if input is None or len(input) < 5:
                # 打印信息
                if (self.debug): \
                    print("Modbus.write_raw : invalid response !")
                return False
            # 打印信息
            if (self.debug): \
                print("\tbytes[%d] = 0x%s"%(len(input), input.hex()))

        except Exception as e:
            print("Modbus:write_raw :", str(e))
            print("Modbus:write_raw : unexpected exit !")
            # 返回结果
            return False

        # 计算CRC校验
        value = crc16(input[ : len(input) - 2])
        # 检查CRC校验
        if input[len(input) - 2] != (value & 0xFF) or \
            input[len(input) - 1] != ((value >> 8) & 0xFF):
            # 打印信息
            if (self.debug): \
                print("Modbus.write_raw : invalid CRC16 !")
            return False
        # 打印信息
        if (self.debug): print("\tcrc16 = 0x%02x"%value)

        # 检查从站地址
        if input[0] != addr:
            # 打印信息
            if (self.debug): \
                print("Modbus.write_raw : invalid addr(0x%02x) !"%input[0])
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
                        self.error_info(input[2])))
                return False

            # 检查反馈指令
            if input[1] not in (0x03, 0x06, 0x10):
                # 打印信息
                if (self.debug): \
                    print("Modbus.write_raw : invalid cmd(0x%02x) !"%input[1])
                return False
            
            '''
            # 检查输入字节是否与输出字节一致
            if input != buffer:
                # 打印信息
                if (self.debug): \
                    print("Modbus.write_raw : response is not as same as output !")
                return False
            '''
        else:
            # 检查反馈指令
            if input[1] == 0x90:
                # 打印错误信息
                if (self.debug): \
                    print("\terror = 0x%02x (%s)"%(input[2], \
                        self.error_info(input[2])))
                print("Modbus.write_raw : 0x%02x (%s)"%(input[2], \
                        self.error_info(input[2])))
                return False

            # 检查反馈指令
            if input[1] != 0x10:
                # 打印信息
                if (self.debug): \
                    print("Modbus.write_raw : invalid cmd(0x%02x) !"%input[1])
                return False
            
            # 检查输入字节是否与输出字节一致
            if input[:6] != buffer[:6]:
                # 打印信息
                if (self.debug): \
                    print("Modbus.write_raw : response is not as same as output !")
                return False
        # 返回结果
        return True