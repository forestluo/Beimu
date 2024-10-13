# -*- coding: utf-8 -*

from DataType import *
from Register import *

'''
单相电能表寄存器
'''    

class D0000(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0000, \
            "编程密码", DataType.hint16)

class D0001(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0001, \
            "软件版本", DataType.hint16)

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
        return "R[{:04X}]({:s}) = ver{:d}.{:02d}". \
            format(self.ind, self.name, (self.get() >> 8) & 0xFF, self.get() & 0xFF)

class D0002(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("W")
        Register.__init__(self, 0x0002, \
            "电能清零", DataType.hint16)
    
class D0005(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0005, \
            "当前协议", DataType.int16)
            
    # 注释信息
    @property
    def info(self):
        # 检查数值
        if self.get() == 1: return "DL/T 645-2007"
        elif self.get() == 2: return "Modbus-RTU"
        else: return "未定义"

class D0006(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0006, \
            "设备地址", DataType.int16)

    # 注释信息
    @property
    def info(self):
        return "此地址只有Modbus-RTU时有效"

class D0007(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0007, \
            "电压变比", DataType.int16)
    
    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 1 and self.get() <= 999.9

class D0008(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0008, \
            "电流变比", DataType.int16)

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 1 and self.get() <= 9999

class D000C(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x000C, \
            "波特率", DataType.int16)

    # 注释信息
    @property
    def info(self):
        # 检查数值
        if self.get() == 0: return "1200bps"
        elif self.get() == 1: return "2400bps"
        elif self.get() == 2: return "4800bps"
        elif self.get() == 3: return "9600bps"
        else: return "未定义"

    # 检查合理性
    @property
    def valid(self):
        if self.get() is None: return False
        return self.get() >= 0 and self.get() <= 3

class D000D(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x000D, \
            "开关量输出", DataType.int16)
        
class D000E(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x000E, \
            "年月", DataType.uint16)
        
    # 格式化
    def __format__(self):
        # 检查数值
        if self.get() is None:
            return Register.__format__(self)
        # 返回缺省格式化
        return "R[{:04X}]({:s}) = {:02d}年{:02d}月". \
            format(self.ind, self.name, (self.get() >> 8) & 0xFF, self.get() & 0xFF)
    
class D000F(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x000F, \
            "天时", DataType.uint16)
        
    # 格式化
    def __format__(self):
        # 检查数值
        if self.get() is None:
            return Register.__format__(self)
        # 返回缺省格式化
        return "R[{:04X}]({:s}) = {:d}天{:d}时". \
            format(self.ind, self.name, (self.get() >> 8) & 0xFF, self.get() & 0xFF)
    
class D0010(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0010, \
            "分秒", DataType.uint16)
        
    # 格式化
    def __format__(self):
        # 检查数值
        if self.get() is None:
            return Register.__format__(self)
        # 返回缺省格式化
        return "R[{:04X}]({:s}) = {:d}分{:d}秒". \
            format(self.ind, self.name, (self.get() >> 8) & 0xFF, self.get() & 0xFF)
    
class D2000(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x2000, \
            "相电压", DataType.float32)
        
    # 注释信息
    @property
    def info(self):
        return "单位V"
            
class D2002(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x2002, \
            "相电流", DataType.float32)
        
    # 注释信息
    @property
    def info(self):
        return "单位A"
    
class D2004(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x2004, \
            "瞬时总有功功率", DataType.float32)

    # 注释信息
    @property
    def info(self):
        return "单位kW"

class D2006(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x2006, \
            "瞬时总无功功率", DataType.float32)
        
    # 注释信息
    @property
    def info(self):
        return "单位kW"
    
class D2008(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x2008, \
            "瞬时总视在功率", DataType.float32)
    
    # 注释信息
    @property
    def info(self):
        return "单位kW"
            
class D200A(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x200A, \
            "总功率因数", DataType.float32)
        
class D200E(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x200E, \
            "电网频率", DataType.float32)
        
    # 注释信息
    @property
    def info(self):
        return "单位Hz"        
    
class D4000(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x4000, \
            "有功总电能", DataType.float32)
        
    # 注释信息
    @property
    def info(self):
        return "单位KWH"        