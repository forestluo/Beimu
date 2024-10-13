# -*- coding: utf-8 -*

from DataType import *
from Register import *

'''
计米表寄存器
'''

class S0000(Register):
    # 定义构造函数
    def __init__(self):
        Register.__init__(self, 0x0000, \
            "报警状态", DataType.hint16)
    
class S0001(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0001, \
            "上排数码管显示值", DataType.int32)
        
class S0003(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0003, \
            "下排数码管显示值", DataType.int32)
        
class S0020(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0020, \
            "小数点位数", DataType.hint16)
        
class S0021(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0021, \
            "上排数码管整数值", DataType.hint32)
        
class S0023(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0023, \
            "下排数码管整数值", DataType.hint32)
        
class S0025(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0025, \
            "上排数码管浮点值", DataType.float32)
        
class S0027(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0027, \
            "下排数码管浮点值", DataType.float32)