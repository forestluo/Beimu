# -*- coding: utf-8 -*

from Register import *

from SlaveStation import *


'''
称重传感器寄存器
'''

class Y0001(Register):
    # 定义构造函数
    def __init__(self):
        self.mode("R")
        Register.__init__(self, 0x0001, \
            "重量数据", DataType.hint32)
