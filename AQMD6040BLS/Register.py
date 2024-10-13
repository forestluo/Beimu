# -*- coding: utf-8 -*

import struct

from DataType import *

class Register:
    # 数值
    __value = None

    # 读写属性
    __mode = "RW"
    # 索引
    __ind = -1
    # 长度
    __len = 0
    # 名称
    __name = None   
    # 类型
    __type = DataType.null
   
    # 定义构造函数
    def __init__(self, ind, name, type, len = 0):
        self.__ind = ind
        self.__len = len
        self.__name = name
        self.__type = type
        # 检查长度
        assert(self.__len >= 0 and self.__len % 2 == 0)
        # 检查类型，并设置长度
        if type == DataType.float32: self.__len = 4
        elif DataType.is_16bits(type): self.__len = 2
        elif DataType.is_32bits(type): self.__len = 4
        elif DataType.is_array(type): assert(self.__len >= 2)
        
    # 索引
    @property
    def ind(self):
        return self.__ind
    
    # 长度
    @property
    def len(self):
        return self.__len

    # 类型
    @property
    def type(self):
        return self.__type
    
    # 名称
    @property
    def name(self):
        return self.__name

    # 检查合理性
    @property
    def valid(self):
        return True
    
    # 注释信息
    @property
    def info(self):
        return "未定义" \
            if self.get() is None \
            else DataType.info(self.type)

    # 设置模式
    def mode(self, value):
        self.__mode = value

    # 可读
    @property
    def readable(self):
        return self.__mode == "R" or self.__mode == "RW"
    
    # 可写
    @property
    def writable(self):
        return self.__mode == "W" or self.__mode == "RW"
               
    # 获得数值
    def get(self):
        # 检查模式
        '''
        if self.__mode == "W":
            print("[0x%04X].get : write only !"%self.__ind)
            return None
        '''
        # 返回缺省值
        return self.__value
    
    # 设置数值
    def set(self, value):
        # 检查模式
        if self.__mode == "R":
            print("[0x%04X].set : read only !"%self.__ind)
            return False
        # 设置数值
        self.__value = value
        # 检查结果
        if self.valid: return True
        # 打印信息
        print("[0x%04X].set : invalid value(%d) !"%(self.__ind, value))
        return False

    # 打包
    def pack(self):
        # 检查数据
        if self.__value is None:
            # 打印信息
            print("Register.pack : value is None")
            return None
        # 检查类型
        if self.__type == DataType.float32:
            # 转换成浮点数
            return struct.pack("!f", self.__value)
        elif DataType.is_array(self.__type):
            # 字符串
            if self.__type == DataType.string8:
                # 转换成字符串
                return str.encode(self.__value)
            # 返回数据值
            return self.__value
        # 检查类型
        elif DataType.is_8bits(self.__type):
            # 返回结果
            return struct.pack("!B", self.__value & 0xFF)
        # 检查类型
        elif DataType.is_16bits(self.__type):
            # 返回结果
            return struct.pack("!H", self.__value & 0xFFFF)
        # 检查类型
        elif DataType.is_32bits(self.__type):
            # 返回结果
            return struct.pack("!I", self.__value & 0xFFFFFFFF)
        else:
            # 打印信息
            print("Register.unpack : invalid type(%d) !"%self.__type)
        return None
        
    # 解析
    def unpack(self, buffer):
        # 确保长度
        assert(len(buffer) == self.__len)
        # 检查类型
        if self.__type == DataType.float32:
            # 转换成浮点数
            self.__value = struct.unpack("!f", buffer)[0]
        elif DataType.is_array(self.__type):
            # 按照字符串处理
            self.__value = buffer
            # 字符串
            if self.__type == DataType.string8:
                # 转换成字符串
                self.__value = bytes.decode(buffer)
        # 检查类型
        elif DataType.is_16bits(self.__type):
            # 短整数
            self.__value = struct.unpack("!H", buffer)[0]
            # 根据符号调整
            if DataType.is_signed(self.__type):
                if (self.__value & 0x8000) != 0: self.__value -= 0x10000
        # 检查类型
        elif DataType.is_32bits(self.__type):
            # 整数
            self.__value = struct.unpack("!I", buffer)[0]
            # 根据符号调整
            if DataType.is_signed(self.__type):
                if (self.__value & 0x80000000) != 0: self.__value -= 0x100000000
        else:
            # 打印信息
            print("Register.unpack : invalid type(%d) !"%self.__type)
            return False
        return True
       
    # 字符化
    def __str__(self):
        return self.__format__()
    
    # 格式化
    def __format__(self):
        # 检查数值
        if self.__value is None:
            # 返回缺省格式化
            return self.__mode + \
                    "[{:04X}]({:s}) = None". \
                    format(self.__ind, self.__name)
        # 检查类型
        if self.__type == DataType.string8:
            return self.__mode + \
                "[{:04X}]({:s}) = \"{:s}\" ({:s})". \
                format(self.__ind, self.__name, self.__value, self.info)
        if self.__type == DataType.float32:
            return self.__mode + \
                "[{:04X}]({:s}) = {:f} ({:s})". \
                format(self.__ind, self.__name, self.__value, self.info)
        if self.__type == DataType.array8:
            return self.__mode + \
                "[{:04X}]({:s}) = 0x{:s} ({:s})". \
                format(self.__ind, self.__name, self.__value.hex(), self.info)
        # 检查类型
        if DataType.is_16bits(self.__type):
            if self.__type == DataType.hint16:
                return self.__mode + \
                    "[{:04X}]({:s}) = 0x{:04x} ({:s})". \
                    format(self.__ind, self.__name, self.__value, self.info)
            return self.__mode + \
                "[{:04X}]({:s}) = {:d} ({:s})". \
                format(self.__ind, self.__name, self.__value, self.info)
        # 检查类型
        if DataType.is_32bits(self.__type):
            if self.__type == DataType.hint32:
                return self.__mode + \
                    "[{:04X}]({:s}) = 0x{:08x} ({:s})". \
                    format(self.__ind, self.__name, self.__value, self.info)
            return self.__mode + \
                "[{:04X}]({:s}) = {:d} ({:s})". \
                format(self.__ind, self.__name, self.__value, self.info)     
        # 打印信息
        print("Register.unpack : invalid type(%d) !"%self.__type)
        return None
       
class R0000(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0000, \
            "设备标识", DataType.hint16)
   
class R0001(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0001, \
            "设备版本号", DataType.hint16)

    # 注释信息
    @property
    def info(self):
        return "高字节为主版本号，低字节为副版本号"

    # 格式化
    def __format__(self):
        # 检查数值
        if self.get() is None:
            return Register.__format__(self)
        # 返回缺省格式化
        return "R[{:04x}]({:s}) = ver{:d}.{:02d}". \
            format(self.ind, self.name, (self.get() >> 8) & 0xFF, self.get() & 0xFF)

class R0002(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0002, \
            "设备名称", DataType.string8, 16)

    # 注释信息
    @property
    def info(self):
        return "以\\0结束的字符串"

    # 格式化
    def __format__(self):
        if self.get() is None:
            return Register.__format__(self)
        return "R[{:04X}]({:s}) = \"{:s}\"". \
            format(self.ind, self.name, self.get())

class R000A(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x000A, \
            "PWM分辨率的倒数", DataType.uint16)

    # 格式化
    def __format__(self):
        if self.get() is None:
            return Register.__format__(self)
        return "R[{:04X}]({:s}) = 1/{:d}". \
            format(self.ind, self.name, self.get())

class R000B(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x000B, \
            "PWM频率", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为Hz"
    
class R000C(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x000C, \
            "最大输出电流", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.01A"
    
class R000D(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x000D, \
            "电流分辨率", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为mA"

class R0020(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0020, \
            "实时PWM", DataType.uint16)

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1000
    
    # 注释信息
    @property
    def info(self):
        return "单位为0.1%"

class R0021(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0021, \
            "实时电流", DataType.uint16)

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 5000
    
    # 注释信息
    @property
    def info(self):
        return "单位为0.01A"

class R0022(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0022, \
            "实时换向频率", DataType.int16)

    # 注释信息
    @property
    def info(self):
        return "单位为Hz"

class R0023(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0023, \
            "位置控制完成状态", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        # 检查数值
        if self.get() == 0: return "未完成"
        elif self.get() == 1: return "完成"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R0024(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0024, \
            "电机换向脉冲数", DataType.int32)

    # 注释信息
    @property
    def info(self):
        return "脉冲个数"
    
class R0026(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0026, \
            "剩余完成时间", DataType.uint32)

    # 注释信息
    @property
    def info(self):
        return "单位为ms"

class R0028(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0028, \
            "IN1电压", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为mV"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 10000

class R0029(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0029, \
            "IN2电压", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为mV"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 10000

class R002A(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x002A, \
            "IN3电压", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为mV"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 10000

class R002B(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x002B, \
            "差分电压", DataType.int16)

    # 注释信息
    @property
    def info(self):
        return "单位为mV"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 10000

class R002C(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x002C, \
            "SQ1电平", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "低电平"
        elif self.get() == 0x01: return "高电平"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R002D(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x002D, \
            "SQ2电平", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "低电平"
        elif self.get() == 0x01: return "高电平"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R002E(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x002E, \
            "IN1输入占空比", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1%"

    # 检查合理性
    @property
    def valid(self):
        return self.get() >= 0 and self.get() <= 1000

class R002F(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x002F, \
            "IN1输入频率", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为Hz"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 100000

class R0030(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0030, \
            "IN1输入脉冲个数", DataType.int32)

    # 注释信息
    @property
    def info(self):
        return "脉冲个数"

class R0032(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0032, \
            "堵转状态", DataType.uint16)

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "未堵转"
        elif self.get() == 0x01: return "正转堵转停止"
        elif self.get() == 0x02: return "反转堵转停止"
        else: return "未定义"

class R0033(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0033, \
            "错误状态", DataType.uint16)

    # 检查合理性
    @property
    def valid(self):
        return self.get() >= 0 and self.get() <= 9

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "无错误"
        elif self.get() == 0x01: return "尚未学习"
        elif self.get() == 0x02: return "堵转停止"
        elif self.get() == 0x03: return "霍尔错误"
        elif self.get() == 0x04: return "达不到目标速度"
        elif self.get() == 0x05: return "线圈错误"
        elif self.get() == 0x06: return "过流关断"
        elif self.get() == 0x07: return "过热关断"
        elif self.get() == 0x08: return "过压关断"
        elif self.get() == 0x09: return "欠压关断"
        else: return "未定义"

class R0034(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0034, \
            "电机转速", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为RPM"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535

class R0035(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0035, \
            "转速是否需要乘以10", DataType.uint16)

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "数值即转速"
        elif self.get() == 0x01: return "数值乘以10为转速"
        else: return "未定义"   

class R0037(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0037, \
            "内部驱动电路温度", DataType.int16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1℃"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= -400 and self.get() <= 1250

class R0038(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0038, \
            "电源电压", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1V"

class R0039(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0039, \
            "控制方式", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "本地控制"
        elif self.get() == 0x01: return "通讯控制"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R003A(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x003A, \
            "母线电流", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.01A"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 4000

class R0040(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x0040, \
            "停止", DataType.uint16)
       
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "正常停止"
        elif self.get() == 0x01: return "紧急制动"
        elif self.get() == 0x02: return "自由停止"
        else: return "未定义"
        
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2

class R0042(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x0042, \
            "设定占空比", DataType.int16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1%"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= -1000 and self.get() <= 1000

class R0043(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x0043, \
            "设定速度闭环控制目标速度", DataType.int16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz"

    # 检查合理性
    @property
    def valid(self):
        return self.get() >= -32768 and self.get() <= 32767

class R0044(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x0044, \
            "设定位置闭环控制行走速度", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 32767

class R0045(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x0045, \
            "设定位置闭环控制类型", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "绝对位置"
        elif self.get() == 0x01: return "相对位置"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R0046(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x0046, \
            "设定位置闭环控制目标位置", DataType.int32)

class R0050(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0050, \
            "占空比调速加速缓冲时间", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1s"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 255

class R0051(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0051, \
            "占空比调速减速缓冲时间", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1s"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 255

class R0052(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0052, \
            "速度闭环控制、位置闭环控制加速加速度", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz/s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535

class R0053(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0053, \
            "速度闭环控制、位置闭环控制减速加速度", DataType.uint16)      

    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz/s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535

class R0060(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0060, \
            "上电时默认占空比调速加速缓冲时间", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 255

class R0061(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0061, \
            "上电时默认占空比调速减速缓冲时间", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 255

class R0062(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0062, \
            "速度闭环控制、位置闭环控制最大加速加速度", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz/s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535

class R0063(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0063, \
            "上电时默认速度闭环/位置闭环控制加速加速度", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz/s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535

class R0064(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0064, \
            "速度闭环控制、位置闭环控制最大减速加速度", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz/s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535

class R0065(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0065, \
            "上电时默认速度闭环/位置闭环控制减速加速度", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz/s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535

class R0066(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0066, \
            "速度闭环控制、位置闭环控制最大速度", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz/s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 32767

class R0067(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0067, \
            "上电时速度闭环控制/位置闭环控制默认速度", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz/s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 32767

class R0069(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0069, \
            "位置控制算法", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "水平定位控制"
        elif self.get() == 0x01: return "水平滑行定位控制"
        elif self.get() == 0x02: return "竖直定位控制"
        else: return "未定义"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2
        
class R006A(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x006A, \
            "电机额定电流", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.01A"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 4000

class R006B(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x006B, \
            "电机最大负载电流", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.01A"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2000

class R006C(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x006C, \
            "电机最大制动电流", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.01A"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2000

class R006D(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x006D, \
            "电机相序数据6字节", DataType.array8, 6)

class R0070(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0070, \
            "速度闭环控制算法", DataType.uint16)

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "速度闭环控制"
        elif self.get() == 0x01: return "时间-位置闭环控制"
        elif self.get() == 0x02: return "时间-位置速率控制"
        else: return "未定义"

class R0071(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0071, \
            "位置闭环控制允许误差", DataType.uint16)
        
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535

class R0072(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0072, \
            "位置闭环控制超调后修正", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "不进行修正"
        elif self.get() == 0x01: return "进行修正"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1
        
class R0073(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0073, \
            "电机极个数", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "个"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535
    
class R0074(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0074, \
            "电机减速比", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为0.1"

    # 检查合理性
    @property
    def valid(self):
        return self.get() >= 0 and self.get() <= 65535

class R0075(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0075, \
            "电机学习状态", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "未学习"
        elif self.get() == 0x01: return "已学习"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R0076(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0076, \
            "禁用电机相序学习功能", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "未禁用"
        elif self.get() == 0x01: return "禁用"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R0077(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0077, \
            "速度设定值×10", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "禁用"
        elif self.get() == 0x01: return "启用"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R0078(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0078, \
            "常态自锁电流", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.01A"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 4000

class R0079(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0079, \
            "短时间最大输出电流为最大负载电流的倍数", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "禁用倍流"
        return "单位为0.01倍"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() == 0 or \
            (self.get() >= 100 and self.get() <= 200)

class R007A(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x007A, \
            "允许倍流输出时间", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "禁用倍流"
        return "单位为0.1s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 999

class R0080(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0080, \
            "限位触发极性", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "低电平触发"
        elif self.get() == 0x01: return "高电平触发"
        elif self.get() == 0x02: return "下降沿触发"
        elif self.get() == 0x03: return "上升沿触发"
        elif self.get() == 0x04: return "禁用限位功能"
        else: return "未定义"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 4

class R0081(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0081, \
            "数字信号极性", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "低电平触发"
        elif self.get() == 0x01: return "高电平触发"
        elif self.get() == 0x02: return "下降沿触发"
        elif self.get() == 0x03: return "上升沿触发"
        else: return "未定义"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 3

class R0082(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0082, \
            "电位器用法", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "单点位器"
        elif self.get() == 0x01: return "双电位器独立"
        elif self.get() == 0x02: return "双电位器协同"
        else: return "未定义"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2        

class R0083(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0083, \
            "脉冲信号类型", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "PWM"
        elif self.get() == 0x01: return "频率"
        elif self.get() == 0x02: return "脉冲"
        else: return "未定义"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2        

class R0084(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0084, \
            "模拟信号类型", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "单端信号"
        elif self.get() == 0x01: return "差分信号"
        elif self.get() == 0x02: return "双单端信号独立"
        elif self.get() == 0x03: return "双单端信号协同"
        else: return "未定义"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 3        

class R0085(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0085, \
            "逻辑电平类型", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "开关量"
        elif self.get() == 0x01: return "0/3.3V"
        elif self.get() == 0x02: return "0/5V"
        elif self.get() == 0x03: return "0/12V或0/24V"
        else: return "未定义"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 3        

class R0086(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0086, \
            "电位器最小值", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为mV"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 10000

class R0087(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0087, \
            "电位器最大值", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为mV"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 10000

class R0088(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0088, \
            "模拟量范围最小值", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为mV"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 10000

class R0089(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0089, \
            "模拟量范围最大值", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为mV"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 10000

class R008A(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x008A, \
            "逻辑电平阈值", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为mV"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 10000

class R008B(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x008B, \
            "电位比较死区", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        return "单位为mV"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 10000

class R008C(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x008C, \
            "脉冲信号倍率", DataType.float32)

class R008E(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x008E, \
            "堵转停止时间", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1s"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 255

class R0090(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0090, \
            "波特率", DataType.int32)

    # 注释信息
    @property
    def info(self):
        return "单位为bps"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 9600 and self.get() <= 115200

class R0092(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0092, \
            "校验方式", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "无校验+2停止位"
        elif self.get() == 0x01: return "奇校验+1停止位"
        elif self.get() == 0x02: return "偶校验+1停止位"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2

class R0093(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0093, \
            "485控制默认调速方式", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "占空比"
        elif self.get() == 0x01: return "速度闭环控制"
        elif self.get() == 0x02: return "位置闭环控制"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2

class R0094(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0094, \
            "485控制时禁止参数配置", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "不禁止"
        elif self.get() == 0x01: return "禁止"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R0095(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0095, \
            "通讯中断停止时间", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1s"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 255

class R0096(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0096, \
            "模拟信号调整系数k", DataType.float32)

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0

class R0098(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0098, \
            "模拟信号调整系数b", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为mV"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535

class R0099(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0099, \
            "禁用报警", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "不禁用"
        elif self.get() == 0x01: return "禁用"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R009C(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x009C, \
            "指定485从站地址", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() != 0x00:
            return "指定通讯控制方式时的从站地址，拨码开关设定的地址失效"
        else: return "通讯控制方式由拨码开关1~7设定，数字/模拟信号控制方式时从站地址固定为0x01"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 127

class R009D(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x009D, \
            "数字/模拟信号控制方式时是否指定485从站地址", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00:
            return "数字/模拟信号时485从站地址固定为0x01"
        else: return "数字/模拟信号时485从站地址由0x009C寄存器指定"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R00A0(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00A0, \
            "复位模式", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "不复位"
        elif self.get() == 0x01: return "SQ2复位"
        elif self.get() == 0x02: return "SQ1复位"
        elif self.get() == 0x03: return "SQ2复位并细调"
        elif self.get() == 0x04: return "SQ1复位并细调"
        else: return "未定义"
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 4
            
class R00A1(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00A1, \
            "是否启用复位细调", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "禁用"
        elif self.get() == 0x01: return "启用"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1
            
class R00A2(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00A2, \
            "总行程", DataType.int32)
            
class R00A4(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00A4, \
            "复位粗调速度", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535
            
class R00A5(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00A5, \
            "复位细调速度", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535
            
class R00A6(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00A6, \
            "到端点后最终速度", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1Hz"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535
            
class R00A7(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00A7, \
            "要忽略的信号变化量", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1%"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1000
            
class R00A8(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00A8, \
            "限位后是否重新复位", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "否"
        elif self.get() == 0x01: return "是"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1
            
class R00A9(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00A9, \
            "复位时转矩", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "最大转矩"
        elif self.get() == 0x01: return "配置的电流对应的转矩"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 4000
            
class R00AA(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00AA, \
            "复位测试", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "非复位状态"
        elif self.get() == 0x01: return "取消复位"
        elif self.get() == 0x02: return "SQ1复位"
        elif self.get() == 0x03: return "SQ2复位"
        elif self.get() == 0x04: return "测量行程"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 4
            
class R00B0(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00B0, \
            "工作模式", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "占空比"
        elif self.get() == 0x01: return "力矩"
        elif self.get() == 0x02: return "速度闭环"
        elif self.get() == 0x03: return "位置闭环"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 3
            
class R00B1(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00B1, \
            "控制方式", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "双触点/逻辑电平控制"
        elif self.get() == 0x01: return "单触点/逻辑电平控制"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1
            
class R00B2(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00B2, \
            "正转速度", DataType.uint16)

class R00B3(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00B3, \
            "反转速度", DataType.uint16)

class R00BA(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00BA, \
            "位置自锁P系数", DataType.float32)
        
class R00BC(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00BC, \
            "位置自锁I系数", DataType.float32)

class R00BE(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00BE, \
            "位置自锁D系数", DataType.float32)

class R00C0(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00C0, \
            "速度闭环控制P系数", DataType.float32)

class R00C2(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00C2, \
            "速度闭环控制I系数", DataType.float32)

class R00C4(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00C4, \
            "速度闭环控制D系数", DataType.float32)

class R00C6(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00C6, \
            "位置闭环控制P系数", DataType.float32)

class R00C8(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00C8, \
            "位置闭环控制I系数", DataType.float32)

class R00CA(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00CA, \
            "位置闭环控制D系数", DataType.float32)

class R00E1(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00E1, \
            "学习命令", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "未学习"
        elif self.get() == 0x01: return "开始电机学习/学习中"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R00E2(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x00E2, \
            "学习状态", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "准备就绪"
        elif self.get() == 0x01: return "正在学习"
        elif self.get() == 0x02: return "正在停止"
        elif self.get() == 0x03: return "学习完毕"
        elif self.get() == 0x04: return "学习失败"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 4

class R00E3(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x00E3, \
            "学习进度", DataType.uint16)

class R00E4(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x00E4, \
            "学习结果数据字节数", DataType.uint16)

class R00E5(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x00E5, \
            "学习结果数据", DataType.array8, 22)

class R0100(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0100, \
            "过热关断触发温度", DataType.int16)

    # 注释信息
    @property
    def info(self):
        return "单位为℃"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= -40 and self.get() <= 125

class R0101(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0101, \
            "禁用倍流触发温度", DataType.int16)

    # 注释信息
    @property
    def info(self):
        return "单位为℃"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= -40 and self.get() <= 125

class R0102(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0102, \
            "过压关断触发电压", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1V"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 80 and self.get() <= 660

class R0103(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0103, \
            "欠压关断触发电压", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1V"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 80 and self.get() <= 600

class R0104(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0104, \
            "过流关断触发电流", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.01A"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 11000

class R0105(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0105, \
            "霍尔错误屏蔽时间", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为ms"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 100

class R0106(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0106, \
            "启用自动调节电流环系数", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "禁用"
        elif self.get() == 0x01: return "启用"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1
            
class R0108(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0108, \
            "启用当温度低于过热保护触发值后自动清除报警", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "禁用"
        elif self.get() == 0x01: return "启用"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1
            
class R010A(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x010A, \
            "温度校正系数K（倍数）", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.0001倍"

    # 检查合理性
    @property
    def valid(self):
        return self.get() >= 9500 and self.get() <= 10500

class R010B(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x010B, \
            "温度校正系数B（截距）", DataType.int16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1℃"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= -100 and self.get() <= 100

class R010C(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x010C, \
            "电压校正系数K（倍数）", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.0001倍"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 9700 and self.get() <= 10300
            
class R010D(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x010D, \
            "电压校正系数B（截距）", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        return "单位为0.1V"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= -10 and self.get() <= 10
            
class R0120(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0120, \
            "CAN通讯模式", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "485/CAN模式"
        elif self.get() == 0x01: return "CANopen模式"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1
            
class R0121(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0121, \
            "CAN节点ID", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "CAN通讯控制时节点ID由拨码开关指定，数字/模拟信号控制节点ID为0x01"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 127
            
class R0122(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0122, \
            "CAN波特率", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "10Kbps"
        elif self.get() == 0x01: return "20Kbps"
        elif self.get() == 0x02: return "50Kbps"
        elif self.get() == 0x03: return "125Kbps"
        elif self.get() == 0x04: return "250Kbps"
        elif self.get() == 0x05: return "500Kbps"
        elif self.get() == 0x06: return "800Kbps"
        elif self.get() == 0x07: return "1Mbps"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 7
            
class R0128(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0128, \
            "CANopen自启动", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "上电后最终进入Pre-Operational状态"
        elif self.get() == 0x01: return "上电后最终进入Operational状态"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1
            
class R0129(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0129, \
            "CANopen心跳周期", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "禁用心跳包"
        else: return "单位为ms"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 65535

class R7000(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x7000, \
            "3.3V输出", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "禁用"
        elif self.get() == 0x01: return "使能"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R7001(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x7001, \
            "报警", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "禁用"
        elif self.get() == 0x01: return "使能"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R7002(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x7002, \
            "输入类型", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "模拟"
        elif self.get() == 0x01: return "数字"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R7003(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x7003, \
            "输入脉冲方向", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "减少"
        elif self.get() == 0x01: return "增加"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R7004(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x7004, \
            "清零输入脉冲", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "关闭自动清除零"
        elif self.get() == 0x01: return "手动清除零"
        elif self.get() == 0x02: return "启动自动清除零"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 2

class R700A(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x700A, \
            "清零位置计数器", DataType.uint16)
        
    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "无动作"
        elif self.get() == 0x01: return "清零位置计数"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R00F0(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x00F0, \
            "虚拟机版本", DataType.uint16)

class R00F1(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x00F1, \
            "程序空间大小", DataType.uint16)

class R00F2(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x00F2, \
            "运行状态", DataType.uint16)

class R00F3(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x00F3, \
            "位置控制完成状态", DataType.uint16)

    # 注释信息
    @property
    def info(self):
        if self.get() == 0x00: return "未完成"
        elif self.get() == 0x01: return "完成"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 1

class R00FA(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00FA, \
            "设备地址", DataType.uint16)

class R00FB(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x00FB, \
            "是否自动运行", DataType.uint16)
