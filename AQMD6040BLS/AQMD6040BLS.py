# -*- coding: utf-8 -*

import time
import struct
import traceback

from Register import *
from SlaveStation import *
    
class AQMD6040BLS(SlaveStation):
    # 控制寄存器列表
    __regs = \
        { \
            # 设备描述信息寄存器
            # 编号, 字节长度, 名称,  数值
            0x0000 : R0000(), 0x0001 : R0001(), 0x0002 : R0002(), 0x000A : R000A(), 0x000B : R000B(),
            0x000C : R000C(), 0x000D : R000D(),
            # 实时状态寄存器
            # 注意：没有0x0036号寄存器说明
            0x0020 : R0020(), 0x0021 : R0021(), 0x0022 : R0022(), 0x0023 : R0023(), 0x0024 : R0024(),
            0x0026 : R0026(), 0x0028 : R0028(), 0x0029 : R0029(), 0x002A : R002A(), 0x002B : R002B(),
            0x002C : R002C(), 0x002D : R002D(), 0x002E : R002E(), 0x002F : R002F(), 0x0030 : R0030(),
            0x0032 : R0032(), 0x0033 : R0033(), 0x0034 : R0034(), 0x0035 : R0035(), 0x0037 : R0037(),
            0x0038 : R0038(), 0x0039 : R0039(), 0x003A : R003A(),
            # 速度控制寄存器
            0x0040 : R0040(), 0x0042 : R0042(), 0x0043 : R0043(), 0x0044 : R0044(), 0x0045 : R0045(),
            0x0046 : R0046(), 0x0050 : R0050(), 0x0051 : R0051(), 0x0052 : R0052(), 0x0053 : R0053(),
            # 电机控制参数配置寄存器
            0x0060 : R0060(), 0x0061 : R0061(), 0x0062 : R0062(), 0x0063 : R0063(), 0x0064 : R0064(),
            0x0065 : R0065(), 0x0066 : R0066(), 0x0067 : R0067(), 0x0069 : R0069(), 0x006A : R006A(),
            0x006B : R006B(), 0x006C : R006C(), 0x006D : R006D(), 0x0070 : R0070(), 0x0071 : R0071(),
            0x0072 : R0072(), 0x0073 : R0073(), 0x0074 : R0074(), 0x0075 : R0075(), 0x0076 : R0076(),
            0x0077 : R0077(), 0x0078 : R0078(), 0x0079 : R0079(), 0x007A : R007A(),
            # 系统参数配置寄存器
            0x0080 : R0080(), 0x0081 : R0081(), 0x0082 : R0082(), 0x0083 : R0083(), 0x0084 : R0084(),
            0x0085 : R0085(), 0x0086 : R0086(), 0x0087 : R0087(), 0x0088 : R0088(), 0x0089 : R0089(),
            0x008A : R008A(), 0x008B : R008B(), 0x008C : R008C(), 0x008E : R008E(), 0x0090 : R0090(),
            0x0092 : R0092(), 0x0093 : R0093(), 0x0094 : R0094(), 0x0095 : R0095(), 0x0096 : R0096(),
            0x0098 : R0098(), 0x0099 : R0099(), 0x009C : R009C(), 0x009D : R009D(),
            # 往复位置控制参数
            0x00A0 : R00A0(), 0x00A1 : R00A1(), 0x00A2 : R00A2(), 0x00A4 : R00A4(), 0x00A5 : R00A5(),
            0x00A6 : R00A6(), 0x00A7 : R00A7(), 0x00A8 : R00A8(), 0x00A9 : R00A9(), 0x00AA : R00AA(),
            # 预设速度寄存器
            0x00B0 : R00B0(), 0x00B1 : R00B1(), 0x00B2 : R00B2(), 0x00B3 : R00B3(),
            # 闭环控制PID参数配置寄存器
            0x00BA : R00BA(), 0x00BC : R00BC(), 0x00BE : R00BE(), 0x00C0 : R00C0(), 0x00C2 : R00C2(),
            0x00C4 : R00C4(), 0x00C6 : R00C6(), 0x00C8 : R00C8(), 0x00CA : R00CA(),
            # 电机学习寄存器
            0x00E1 : R00E1(), 0x00E2 : R00E2(), 0x00E3 : R00C0(), 0x00E3 : R00E3(), 0x00E4 : R00E4(),
            0x00E5 : R00E5(),
            # 安全保护寄存器
            0x0100 : R0100(), 0x0101 : R0101(), 0x0102 : R0102(), 0x0103 : R0103(), 0x0104 : R0104(),
            0x0105 : R0105(), 0x0106 : R0106(), 0x0108 : R0108(), 0x010A : R010A(), 0x010B : R010B(),
            0x010C : R010C(), 0x010D : R010D(),
            # CAN参数配置寄存器
            0x0120 : R0120(), 0x0121 : R0121(), 0x0122 : R0122(), 0x0128 : R0128(), 0x0129 : R0129(),
            # 对象字典操作寄存器
            # 配置参数存储寄存器
            # 程序操作寄存器
            0x00F0 : R00F0(), 0x00F1 : R00F1(), 0x00F2 : R00F2(), 0x00F3 : R00F3(), 0x00FA : R00FA(),
            0x00FB : R00FB(),
            # 外设操作相关寄存器
            0x7000 : R7000(), 0x7001 : R7001(), 0x7002 : R7002(), 0x7003 : R7003(), 0x7004 : R7004(),
            0x700A : R700A(),
        }
       
    # 定义初始化函数
    def __init__(self, name, address = 0x01):
        # 调用父函数初始化
        SlaveStation.__init__(self, name, address)
        
    # 删除寄存器
    def __delitem__(self, index):
        # 删除寄存器
        del self.__regs[index]

    # 获得寄存器
    def __getitem__(self, index):
        # 返回寄存器数值
        return self.__regs[index]
        
    # 设置寄存器
    def __setitem__(self, index, register):
        # 设置寄存器数值
        self.__regs[index] = register 

    # 按名称查询对象
    def get_item(self, name):
        # 遍历字典
        for value in self.__regs.values():
            if name is value.name: return value
        
    # 打印所有寄存器
    # None 表明没有任何可用数据
    # 读写模式[寄存器16进制索引](中文名称) = 数值|单位 (注释)]
    def print_items(self):
        # 打印信息
        print("AQMD6040BLS.print_items : begin !")
        # 遍历字典
        for value in self.__regs.values(): print("\t%s"%value)

    # 读取所有寄存器
    # 通过单个寄存器读取实现
    # 需要多次通讯过程，效率较低
    def read_items(self):
        # 打印信息
        print("AQMD6040BLS.read_items : begin !")
        # 遍历字典
        for value in self.__regs.values():
            if not self.read(value.ind): return False
            print("\t%s"%value)
        # 返回结果
        return True
    
    # 写入寄存器
    def write(self, index, count = 1):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.write : begin !")
        # 数据
        buffer = bytes()
        # 循环处理
        for i in range(index, index + count):
            # 打印数据
            if (self.debug) : \
                print("\t%s"%self[i])
            # 检查模式
            if not self[i].writable:
                # 打印信息
                if (self.debug) : \
                    print("AQMD6040BLS.write : not writable !")
                return False
            # 检查数据有效性
            if not self[i].valid:
                # 打印信息
                if (self.debug) : \
                    print("AQMD6040BLS.write : invalid value !")
                return False
            # 检查是否存在该key
            if i not in self.__regs:
                # 数据补0
                buffer += [0x00, 0x00]
                # 打印信息
                if (self.debug) : \
                    print("AQMD6040BLS.write : skip R[%04X] !"%i)
                continue
            # 打包
            output = self[i].pack()
            # 检查结果
            if output is None:
                # 打印信息
                if (self.debug) : \
                    print("AQMD6040BLS.write : fail to pack !")
                return False
            # 检查长度
            if len(output) != self[i].len:
                # 打印信息
                if (self.debug) : \
                    print("AQMD6040BLS.write : invalid buffer !")
                return False
            # 增加数据包长度
            buffer += output
        # 写入数据
        if not SlaveStation.write(self, index, buffer):
            # 打印信息
            if (self.debug) : \
                print("AQMD6040BLS.write : fail to write !")
            return False
        # 返回结果
        return True

    # 读取单个寄存器
    def read(self, index):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read : begin !")
        # 检查模式
        if not self[index].readable:
            # 打印信息
            if (self.debug) : \
                print("AQMD6040BLS.read : not readable !")
            return True
        # 读取数据
        buffer = SlaveStation.read(self, self[index].ind, self[index].len // 2)
        # 检查结果
        if buffer is None or len(buffer) != self[index].len:
            # 打印信息
            if (self.debug) : \
                print("AQMD6040BLS.read : fail to read !")
            return False
        # 解包
        if not self[index].unpack(buffer):
            # 打印信息
            if (self.debug) : \
                print("AQMD6040BLS.read : fail to unpack(R%04X) !"%index)
            return False
        #返回结果
        return True
        
    # 设备描述信息寄存器
    def read_info(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_info : begin !")
        # 读取数据
        # 地址从0x0000开始
        # 设备描述信息寄存器共14个
        buffer = SlaveStation.read(self, 0x0000, 14)
        # 检查结果
        if buffer is None or len(buffer) != 28:
            # 打印信息
            if (self.debug) : \
                print("AQMD6040BLS.read_info : fail to read !")
            return False
        # 设备描述信息寄存器
        # 设备标识
        if not self[0x0000].unpack(buffer[0 : 2]): return False
        # 设备版本号
        if not self[0x0001].unpack(buffer[2 : 4]): return False
        # 设备名称
        if not self[0x0002].unpack(buffer[4 : 20]): return False
        # PWM分辨率
        if not self[0x000A].unpack(buffer[20 : 22]): return False
        # PWM频率
        if not self[0x000B].unpack(buffer[22 : 24]): return False
        # 最大电流
        if not self[0x000C].unpack(buffer[24 : 26]): return False
        # 电流分辨率
        if not self[0x000D].unpack(buffer[26 : 28]): return False
        # 返回结果
        return True
        
    def read_status(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_status : begin !")
        # 读取数据
        # 地址从0x0020开始
        # 设备实时状态寄存器共27个
        buffer = SlaveStation.read(self, 0x0020, 27)
        # 检查结果
        if buffer is None or len(buffer) != 54:
            # 打印信息
            if (self.debug) : \
                print("Modbus.read_status : fail to read !")
            return False
        # 实时状态寄存器
        # 占空比
        if not self[0x0020].unpack(buffer[0 : 2]): return False
        # 电流
        if not self[0x0021].unpack(buffer[2 : 4]): return False
        # 换向频率
        if not self[0x0022].unpack(buffer[4 : 6]): return False
        # 位置控制完成状态
        if not self[0x0023].unpack(buffer[6 : 8]): return False
        # 电机换向脉冲数
        if not self[0x0024].unpack(buffer[8 : 12]): return False
        # 剩余完成时间
        if not self[0x0026].unpack(buffer[12 : 16]): return False
        # 输入电压
        if not self[0x0028].unpack(buffer[16 : 18]): return False
        if not self[0x0029].unpack(buffer[18 : 20]): return False
        if not self[0x002A].unpack(buffer[20 : 22]): return False
        # 差分电压
        if not self[0x002B].unpack(buffer[22 : 24]): return False
        # SQ1电平
        if not self[0x002C].unpack(buffer[24 : 26]): return False
        # SQ2电平
        if not self[0x002D].unpack(buffer[26 : 28]): return False
        # IN1输入占空比
        if not self[0x002E].unpack(buffer[28 : 30]): return False
        # IN1输入频率
        if not self[0x002F].unpack(buffer[30 : 32]): return False
        # IN1输入脉冲个数
        if not self[0x0030].unpack(buffer[32 : 36]): return False
        # 堵转状态
        if not self[0x0032].unpack(buffer[36 : 38]): return False
        # 错误状态
        if not self[0x0033].unpack(buffer[38 : 40]): return False
        # 电机转速
        if not self[0x0034].unpack(buffer[40 : 42]): return False
        # 转速是否需要乘以10
        if not self[0x0035].unpack(buffer[42 : 44]): return False
        # 内部(驱动电路)温度
        if not self[0x0037].unpack(buffer[46 : 48]): return False
        # 电源电压
        if not self[0x0038].unpack(buffer[48 : 50]): return False
        # 控制方式
        if not self[0x0039].unpack(buffer[50 : 52]): return False
        # 母线电流
        if not self[0x003A].unpack(buffer[52 : 54]): return False
        # 返回结果
        return True
        
    # 速度控制寄存器
    def read_spctl(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_spctl : begin !")
        # 读取数据
        # 地址从0x0050开始
        # 设备实时状态寄存器共4个
        buffer = SlaveStation.read(self, 0x0050, 4)
        # 检查结果
        if buffer is None or len(buffer) != 8:
            # 打印信息
            if (self.debug) : \
                print("Modbus.read_spctl : fail to read !")
            return False        
        if not self[0x0050].unpack(buffer[0 : 2]): return False
        if not self[0x0051].unpack(buffer[2 : 4]): return False
        if not self[0x0052].unpack(buffer[4 : 6]): return False
        if not self[0x0053].unpack(buffer[6 : 8]): return False
        # 返回结果
        return True
        
    # 电机控制参数配置寄存器
    def read_mtcfg(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_mtcfg : begin !")
        # 读取数据
        # 地址从0x0060开始
        # 设备实时状态寄存器共27个
        buffer = SlaveStation.read(self, 0x0060, 27)
        # 检查结果
        if buffer is None or len(buffer) != 54:
            # 打印信息
            if (self.debug) : \
                print("Modbus.read_mtcfg : fail to read !")
            return False        
        # 解析
        if not self[0x0060].unpack(buffer[0 : 2]): return False
        if not self[0x0061].unpack(buffer[2 : 4]): return False
        if not self[0x0062].unpack(buffer[4 : 6]): return False
        if not self[0x0063].unpack(buffer[6 : 8]): return False
        if not self[0x0064].unpack(buffer[8 : 10]): return False
        if not self[0x0065].unpack(buffer[10 : 12]): return False
        if not self[0x0066].unpack(buffer[12 : 14]): return False
        if not self[0x0067].unpack(buffer[14 : 16]): return False
        if not self[0x0069].unpack(buffer[18 : 20]): return False
        if not self[0x006A].unpack(buffer[20 : 22]): return False
        if not self[0x006B].unpack(buffer[22 : 24]): return False
        if not self[0x006C].unpack(buffer[24 : 26]): return False
        if not self[0x006D].unpack(buffer[26 : 32]): return False
        if not self[0x0070].unpack(buffer[32 : 34]): return False
        if not self[0x0071].unpack(buffer[34 : 36]): return False
        if not self[0x0072].unpack(buffer[36 : 38]): return False
        if not self[0x0073].unpack(buffer[38 : 40]): return False
        if not self[0x0074].unpack(buffer[40 : 42]): return False
        if not self[0x0075].unpack(buffer[42 : 44]): return False
        if not self[0x0076].unpack(buffer[44 : 46]): return False
        if not self[0x0077].unpack(buffer[46 : 48]): return False
        if not self[0x0078].unpack(buffer[48 : 50]): return False
        if not self[0x0079].unpack(buffer[50 : 52]): return False
        if not self[0x007A].unpack(buffer[52 : 54]): return False
        # 返回结果
        return True
        
    # 系统参数配置寄存器
    def read_syscfg(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_syscfg : begin !")
        # 读取数据
        # 地址从0x0080开始
        # 设备实时状态寄存器共30个
        buffer = SlaveStation.read(self, 0x0080, 30)
        # 检查结果
        if buffer is None or len(buffer) != 60:
            # 打印信息
            if (self.debug) : \
                print("Modbus.read_syscfg : fail to read !")
            return False        
        # 解析
        if not self[0x0080].unpack(buffer[0 : 2]): return False
        if not self[0x0081].unpack(buffer[2 : 4]): return False
        if not self[0x0082].unpack(buffer[4 : 6]): return False
        if not self[0x0083].unpack(buffer[6 : 8]): return False
        if not self[0x0084].unpack(buffer[8 : 10]): return False
        if not self[0x0085].unpack(buffer[10 : 12]): return False
        if not self[0x0086].unpack(buffer[12 : 14]): return False
        if not self[0x0087].unpack(buffer[14 : 16]): return False
        if not self[0x0088].unpack(buffer[16 : 18]): return False
        if not self[0x0089].unpack(buffer[18 : 20]): return False
        if not self[0x008A].unpack(buffer[20 : 22]): return False
        if not self[0x008B].unpack(buffer[22 : 24]): return False
        if not self[0x008C].unpack(buffer[24 : 28]): return False
        if not self[0x008E].unpack(buffer[28 : 30]): return False
        if not self[0x0090].unpack(buffer[32 : 36]): return False      
        if not self[0x0092].unpack(buffer[36 : 38]): return False
        if not self[0x0093].unpack(buffer[38 : 40]): return False
        if not self[0x0094].unpack(buffer[40 : 42]): return False
        if not self[0x0095].unpack(buffer[42 : 44]): return False
        if not self[0x0096].unpack(buffer[44 : 48]): return False
        if not self[0x0098].unpack(buffer[48 : 50]): return False
        if not self[0x0099].unpack(buffer[50 : 52]): return False
        if not self[0x009C].unpack(buffer[56 : 58]): return False
        if not self[0x009D].unpack(buffer[58 : 60]): return False
        # 返回结果
        return True
        
    # 往复位置寄存器
    def read_poscfg(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_poscfg : begin !")
        # 读取数据
        # 地址从0x00A0开始
        # 设备实时状态寄存器共11个
        buffer = SlaveStation.read(self, 0x00A0, 11)
        # 检查结果
        if buffer is None or len(buffer) != 22:
            # 打印信息
            if (self.debug) : \
                print("Modbus.read_poscfg : fail to read !")
            return False        
        # 解析
        if not self[0x00A0].unpack(buffer[0 : 2]): return False
        if not self[0x00A1].unpack(buffer[2 : 4]): return False
        if not self[0x00A2].unpack(buffer[4 : 8]): return False
        if not self[0x00A4].unpack(buffer[8 : 10]): return False
        if not self[0x00A5].unpack(buffer[10 : 12]): return False
        if not self[0x00A6].unpack(buffer[12 : 14]): return False
        if not self[0x00A7].unpack(buffer[14 : 16]): return False
        if not self[0x00A8].unpack(buffer[16 : 18]): return False
        if not self[0x00A9].unpack(buffer[18 : 20]): return False
        if not self[0x00AA].unpack(buffer[20 : 22]): return False
        # 返回结果
        return True

    # 预设速度寄存器
    def read_spcfg(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_spcfg : begin !")
        # 读取数据
        # 地址从0x00B0开始
        # 设备实时状态寄存器共4个
        buffer = SlaveStation.read(self, 0x00B0, 4)
        # 检查结果
        if buffer is None or len(buffer) != 8:
            # 打印信息
            if (self.debug) : \
                print("Modbus.read_spcfg : fail to read !")
            return False        
        # 解析
        if not self[0x00B0].unpack(buffer[0 : 2]): return False
        if not self[0x00B1].unpack(buffer[2 : 4]): return False
        if not self[0x00B2].unpack(buffer[4 : 6]): return False
        if not self[0x00B3].unpack(buffer[6 : 8]): return False
        # 返回结果
        return True

    # 闭环控制PID参数配置寄存器
    def read_pidcfg(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_pidcfg : begin !")
        # 读取数据
        # 地址从0x00BA开始
        # 设备实时状态寄存器共18个
        buffer = SlaveStation.read(self, 0x00BA, 18)
        # 检查结果
        if buffer is None or len(buffer) != 36:
            # 打印信息
            if (self.debug) : \
                print("Modbus.read_pidcfg : fail to read !")
            return False        
        # 解析
        if not self[0x00BA].unpack(buffer[0 : 4]): return False
        if not self[0x00BC].unpack(buffer[4 : 8]): return False
        if not self[0x00BE].unpack(buffer[8 : 12]): return False
        if not self[0x00C0].unpack(buffer[12 : 16]): return False
        if not self[0x00C2].unpack(buffer[16 : 20]): return False
        if not self[0x00C4].unpack(buffer[20 : 24]): return False
        if not self[0x00C6].unpack(buffer[24 : 28]): return False
        if not self[0x00C8].unpack(buffer[28 : 32]): return False
        if not self[0x00CA].unpack(buffer[32 : 36]): return False
        # 返回结果
        return True
        
    # 电机学习寄存器
    def read_lncfg(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_lncfg : begin !")
        # 读取数据
        # 地址从0x00E0开始
        # 设备实时状态寄存器共16个
        buffer = SlaveStation.read(self, 0x00E0, 16)
        # 检查结果
        if buffer is None or len(buffer) != 32:
            # 打印信息
            if (self.debug) : \
                print("Modbus.read_lncfg : fail to read !")
            return False
        # 解析
        if not self[0x00E1].unpack(buffer[2 : 4]): return False
        if not self[0x00E2].unpack(buffer[4 : 6]): return False
        if not self[0x00E3].unpack(buffer[6 : 8]): return False
        if not self[0x00E4].unpack(buffer[8 : 10]): return False
        if not self[0x00E5].unpack(buffer[10 : 32]): return False
        # 返回结果
        return True

    # 安全保护寄存器
    def read_sfcfg(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_sfcfg : begin !")
        # 读取数据
        # 地址从0x0100开始
        # 设备实时状态寄存器共10个
        buffer = SlaveStation.read(self, 0x0100, 14)
        # 检查结果
        if buffer is None or len(buffer) != 28:
            # 打印信息
            if (self.debug) : \
                print("Modbus.read_sfcfg : fail to read !")
            return False
        # 解析
        if not self[0x0100].unpack(buffer[0 : 2]): return False
        if not self[0x0101].unpack(buffer[2 : 4]): return False
        if not self[0x0102].unpack(buffer[4 : 6]): return False
        if not self[0x0103].unpack(buffer[6 : 8]): return False
        if not self[0x0104].unpack(buffer[8 : 10]): return False
        if not self[0x0105].unpack(buffer[10 : 12]): return False
        if not self[0x0106].unpack(buffer[12 : 14]): return False
        if not self[0x0108].unpack(buffer[16 : 18]): return False
        if not self[0x010A].unpack(buffer[20 : 22]): return False
        if not self[0x010B].unpack(buffer[22 : 24]): return False
        if not self[0x010C].unpack(buffer[24 : 26]): return False
        if not self[0x010D].unpack(buffer[26 : 28]): return False
        # 返回结果
        return True
    
    # CAN参数配置寄存器
    def read_cancfg(self):
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.read_cancfg : begin !")
        # 读取数据
        # 地址从0x0120开始
        # 设备实时状态寄存器共10个
        buffer = SlaveStation.read(self, 0x0120, 10)
        # 检查结果
        if buffer is None or len(buffer) != 20:
            # 打印信息
            if (self.debug) : \
                print("Modbus.read_cancfg : fail to read !")
            return False
        # 解析       
        # CAN通讯模式
        if not self[0x0120].unpack(buffer[0 : 2]): return False
        # CAN节点ID
        if not self[0x0121].unpack(buffer[2 : 4]): return False
        # CAN波特率
        if not self[0x0122].unpack(buffer[4 : 6]): return False
        # CANopen自启动
        if not self[0x0128].unpack(buffer[16 : 18]): return False
        # CANopen心跳周期
        if not self[0x0129].unpack(buffer[18 : 20]): return False
        # 返回结果
        return True

    # 电机学习
    def init_motor(self):
        # 打印信息
        print("AQMD6040BLS.init_motor : check status !")
        # 读取寄存器状态
        if not self.read(0x0075):
            if (self.debug) : \
                print("AQMD6040BLS.init_motor : fail to read R[0075] !")
            return False
        # 打印寄存器数据
        print("\t%s"%self[0x0075])
        # 设置数值
        self[0x0075].set(0) #设置为未学习状态
        # 写入寄存器
        if not self.write(0x0075):
            if (self.debug) : \
                print("AQMD6040BLS.init_motor : fail to write R[0075] !")
            return False
        # 读取学习命令
        if not self.read(0x00E1):
            if (self.debug) : \
                print("AQMD6040BLS.init_motor : fail to read R[00E1] !")
            return False
        # 打印寄存器数据
        print("\t%s"%self[0x00E1])
        # 检查学习命令
        if self[0x00E1].get() != 0:
            if (self.debug) : \
                print("AQMD6040BLS.init_motor : invalid R[00E1] status !")
            return False
        # 读取学习状态
        if not self.read(0x00E2):
            if (self.debug) : \
                print("AQMD6040BLS.init_motor : fail to read R[00E2] !")
            return False
        # 打印寄存器数据
        print("\t%s"%self[0x00E2])
        # 检查学习状态
        if self[0x00E2].get() in (1, 2):
            if (self.debug) : \
                print("AQMD6040BLS.init_motor : invalid R[00E2] status !")
            return False
        # 打印信息
        print("AQMD6040BLS.init_motor : begin to initialize !")
        # 设置电机学习命令
        self[0x00E1].set(1) #开始电机学习
        # 写入寄存器
        if not self.write(0x00E1):
            if (self.debug) : \
                print("AQMD6040BLS.init_motor : fail to write R[00E1] !")
            return False
        # 打印信息
        if (self.debug) : \
            print("AQMD6040BLS.init_motor : command was sent !")
        # 等待电机学习完毕或者失败
        # 大约等待10秒
        for i in range(10):
            # 打印信息
            if (self.debug) : \
                print("AQMD6040BLS.init_motor : wait for a moment !")
            # 睡眠一段时间
            time.sleep(1)
            # 读取学习状态
            if not self.read(0x00E2):
                if (self.debug) : \
                    print("AQMD6040BLS.init_motor : fail to read R[00E2] !")
                continue
            # 打印寄存器数据
            print("\t%s"%self[0x00E2])
            # 检查数据结果
            if self[0x00E2].get() == 4:
                # 打印信息
                if (self.debug) : \
                    print("AQMD6040BLS.init_motor : fail to initialize !")
                break
            # 检查学习状态
            elif self[0x00E2].get() == 3:
                # 打印信息
                if (self.debug) : \
                    print("AQMD6040BLS.init_motor : successfully initialized !")
                break
            else:
                # 打印信息
                if (self.debug) : \
                    print("AQMD6040BLS.init_motor : please wait ... !")
        # 检查结果
        if not self[0x00E2].get() in (3, 4):
            # 打印信息
            if (self.debug) : \
                print("AQMD6040BLS.init_motor : timeout and give up !")
            return False
        # 读取寄存器状态
        if not self.read(0x0075):
            if (self.debug) : \
                print("AQMD6040BLS.init_motor : fail to read R[0075] !")
            return False
        # 打印寄存器数据
        print("\t%s"%self[0x0075])
        # 返回结果
        return self[0x0075].get() == 1
    
    # 操作电机位置
    def stop_motor(self, value):
        # 打印信息
        print("AQMD6040BLS.stop_motor : check status !")
        # 读取寄存器状态
        if not self.read(0x0040):
            if (self.debug) : \
                print("AQMD6040BLS.stop_motor : fail to read R[0040] !")
            return False
        # 打印寄存器数据
        print("\t%s"%self[0x0040])
        # 打印信息
        print("AQMD6040BLS.stop_motor : try to stop motor !")
        # 设置数值
        self[0x0040].set(value) #设置停止方式
        # 写入寄存器
        if not self.write(0x0040):
            if (self.debug) : \
                print("AQMD6040BLS.stop_motor : fail to write R[0040] !")
            return False
        # 打印寄存器数据
        print("\t%s"%self[0x0040])
        return True

    # 清理位置计数        
    def clear_pos(self):
        # 打印信息
        print("AQMD6040BLS.clear_pos : try to clear position !")
        # 设置数值
        self[0x700A].set(1) #清零位置计数
        # 打印寄存器数据
        print("\t%s"%self[0x700A])
        # 写入寄存器
        if not self.write(0x700A):
            if (self.debug) : \
                print("AQMD6040BLS.clear_pos : fail to write R[700A] !")
            return False
        if (self.debug) : \
            # 打印信息
            print("AQMD6040BLS.clear_pos : position cleared !")
        return True

    # 设置绝对位置
    def set_abspos(self, sp, pos):
        # 打印信息
        print("AQMD6040BLS.set_abspos : try to set absolute position !")
        # 设置数值
        self[0x0044].set(sp)
        self[0x0045].set(0) #绝对位置
        self[0x0046].set(pos)
        # 打印寄存器数据
        print("\t%s"%self[0x0044])
        print("\t%s"%self[0x0045])
        print("\t%s"%self[0x0046])
        # 写入寄存器
        if not self.write(0x0044, 3):
            if (self.debug) : \
                print("AQMD6040BLS.set_abspos : fail to write R[0044] ~ R[0046] !")
            return False
        if (self.debug) : \
            # 打印信息
            print("AQMD6040BLS.set_abspos : absolute position was set !")
        return True
        
    # 等待电机完成位置动作
    def wait_pos(self):
        # 打印信息
        print("AQMD6040BLS.stop_motor : wait motor to finish !")
        # 循环
        while True:
            # 读取寄存器状态
            if self.read(0x0024):
                # 打印寄存器数据
                print("\t%s"%self[0x0024])
            # 读取寄存器状态
            if self.read(0x0026):
                # 打印寄存器数据
                print("\t%s"%self[0x0026])
            # 读取寄存器状态
            if not self.read(0x0023):
                if (self.debug) : \
                    print("AQMD6040BLS.stop_motor : fail to read R[0023] !")
                return False
            # 打印寄存器数据
            print("\t%s"%self[0x0023])
            # 检查结果
            if self[0x0023].get() == 1:
                if (self.debug) : \
                    print("AQMD6040BLS.stop_motor : destination reached !")
                break
        return True
        
# 定义主函数
def main():  
    # 创建设备
    myDevice = AQMD6040BLS("/dev/ttyUSB0")

    # 逐个读取所有寄存器
    # 速度比较慢
    # myDevice.read_items()
    # 按区快速读取寄存器
    # myDevice.read_info()
    # myDevice.read_status()
    # myDevice.read_spctl()
    # myDevice.read_mtcfg()
    # myDevice.read_syscfg()
    # myDevice.read_poscfg()
    # myDevice.read_spcfg()
    # myDevice.read_pidcfg()
    # myDevice.read_lncfg()
    # myDevice.read_sfcfg()
    # myDevice.read_cancfg()
    # 打印寄存器数据
    # myDevice.print_items()
       
    # 初始化电机
    # myDevice.init_motor()
    
    # 停止电机
    # 正常停止
    if not myDevice.stop_motor(0):
        # 打印信息
        print("AQMD6040BLS:main : fail to stop motor !")
        return
    # 清理位置
    if not myDevice.clear_pos():
        # 打印信息
        print("AQMD6040BLS:main : fail to clear position !")
        return
    # 设置绝对位置
    if not myDevice.set_abspos(500, 1000):
        # 打印信息
        print("AQMD6040BLS:main : fail to set absolute position !")
        return
    # 等待电机完成动作
    if not myDevice.wait_pos():
        # 打印信息
        print("AQMD6040BLS:main : fail to wait position action !")
        return
    # 删除设备
    del myDevice

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("AQMD6040BLS:__main__ :", str(e))
        print("AQMD6040BLS:__main__ : unexpected exit !")
