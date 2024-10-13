# -*- coding: utf-8 -*

from Modbus import Modbus

class SlaveStation(Modbus):
    # 从站地址
    address = 0x00
    
    def __init__(self, name, address):
        # 调用父对象初始化
        Modbus.__init__(self, name)    
        # 设置从站地址
        self.address = address
        # 检查设备名
        if address < 0 or address > 127:
            # 打印信息
            print("SlaveStation:__init__ : invalid address(%d) !"%address)
        return

    def read(self, start, count):
        # 调用父对象函数
        return super(SlaveStation, self).read(self.address, start, count)
    
    def write(self, start, buffer):
        # 调用父对象函数
        return super(SlaveStation, self).write(self.address, start, buffer)

