# -*- coding: utf-8 -*

import serial
import traceback

from Register import *
from YP353Regs import *

from SlaveStation import *

class YP353(SlaveStation):
    # 控制寄存器列表
    __regs = \
        { \
            0x0001 : Y0001(),
        }
       
    # 定义初始化函数
    def __init__(self, name, address = 0x01):
        # 调用父函数初始化
        SlaveStation.__init__(self, name, address)
        # 设置寄存器列表
        SlaveStation.__setregs__(self, self.__regs)
        # 设置串口参数
        # 需要与设备设置保持一致
        self._set_port(115200, serial.EIGHTBITS,
            serial.PARITY_NONE, serial.STOPBITS_ONE)

    # 检查属性
    @property
    def wait_time(self):
        return 0.025
    
    # 获得重量值
    def get_weight(self):
        # 写寄存器
        if not self.read_reg(0x0001):
            print("YP353.get_weight : fail to read R[0x0001]")
            return None
        # 分离数据
        status = self[0x0001].get() & 0xFFFF
        value = (self[0x0001].get() >> 16) & 0xFFFF
        # 检查结果
        if ((status & 0x0100) != 0): value = - value
        # 返回缺省值
        return (status, value)
        
# 定义主函数
def main():  
    # 创建设备
    myDevice = YP353("/dev/ttyUSB1", 0x01)

    # 读取数据
    myDevice.read_items()
    # 打印数据
    myDevice.print_items()

    # 删除设备
    del myDevice

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("YP353:__main__ :", str(e))
        print("YP353:__main__ : unexpected exit !")
