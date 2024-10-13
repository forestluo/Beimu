# -*- coding: utf-8 -*

import serial
import traceback

from Register import *
from SD76CRegs import *

from SlaveStation import *

class SD76C(SlaveStation):
    # 控制寄存器列表
    __regs = \
        { \
            0x0000 : S0000(),
            0x0001 : S0001(), 0x0003 : S0003(),
            
            0x0020 : S0020(),
            0x0021 : S0021(), 0x0023 : S0023(),
            0x0025 : S0025(), 0x0027 : S0027()
        }
       
    # 定义初始化函数
    def __init__(self, name, address = 0x03):
        # 调用父函数初始化
        SlaveStation.__init__(self, name, address)
        # 设置寄存器列表
        SlaveStation.__setregs__(self, self.__regs)
        # 设置串口参数
        # 需要与设备设置保持一致
        self._set_port(57600, serial.EIGHTBITS,
            serial.PARITY_NONE, serial.STOPBITS_ONE)

    # 检查属性
    @property
    def wait_time(self):
        return 0.1
    
    # 工作模式
    def work_mode(value):
        if value == 0x00 :
            return "计数计米器"
        elif value == 0x01 :
            return "计时器"
        elif value == 0x02 :
            return "计时计数器"
        elif value == 0x03 :
            return "总量计米器"
        elif value == 0x04 :
            return "批次计米器"
        return "未定义"
        
    # 复位所有数值
    def reset(self):
        # 设置复位模式
        self[0x0000].set(0x0001 | 0x0002)
        # 写寄存器
        if not self.write_reg(0x0000):
            print("SD76C.reset : fail to write R[0x0000]")
            return False
        return True
    
    # 读取位置信息
    def get_pos(self):
        # 读取数据
        # 地址从0x0020开始
        # 设备实时状态寄存器共9个
        buffer = SlaveStation.read_regs(self, 0x0020, 9)
        # 检查结果
        if buffer is None or len(buffer) != 18:
            # 打印信息
            if (self.debug) : \
                print("SD76C.get_pos : fail to read !")
            return None
        # 解析
        if not self[0x0020].unpack(buffer[0 : 2]): return False
        if not self[0x0021].unpack(buffer[2 : 6]): return False
        if not self[0x0023].unpack(buffer[6 : 10]): return False
        if not self[0x0025].unpack(buffer[10 : 14]): return False
        if not self[0x0027].unpack(buffer[14 : 18]): return False
        
        # 返回结果
        if (self[0x0021].get() & 0xF000) == 0:
            return self[0x0025].get()
        return -1.0 * self[0x0025].get()

# 定义主函数
def main():  
    # 创建设备
    myDevice = SD76C("/dev/ttyUSB1", 0x03)

    # 读取数据
    myDevice.read_items()
    # 打印数据
    myDevice.print_items()
    
    # 复位
    #myDevice.reset()
    
    # 获得位置信息
    pos = myDevice.get_pos()
    # 打印信息
    if pos is not None:
        print("current position : %f米"% pos)
 
    # 读取数据
    #myDevice.read_items()
    # 打印数据
    #myDevice.print_items()   

    # 删除设备
    del myDevice

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("SD76C:__main__ :", str(e))
        print("SD76C:__main__ : unexpected exit !")
