# -*- coding: utf-8 -*

import serial
import traceback

from Register import *
from DDSU666Regs import *

from SlaveStation import *

class DDSU666(SlaveStation):
    # 控制寄存器列表
    __regs = \
        { \
            0x0000 : D0000(), 0x0001 : D0001(),
            # 电能清零
            0x0002 : D0002(),
            # 协议及地址
            0x0005 : D0005(), 0x0006 : D0006(),
            # 变比
            0x0007 : D0007(), 0x0008 : D0008(),
            # 波特率
            0x000C : D000C(),
            0x000D : D000D(),
            # 时间设置
            0x000E : D000E(), 0x000F : D000F(), 0x0010 : D0010(),

            # 电压与电流
            0x2000 : D2000(), 0x2002 : D2002(),
            # 功率相关参数
            0x2004 : D2004(), 0x2006 : D2006(), 0x2008 : D2008(), 0x200A : D200A(),
            # 频率
            0x200E : D200E(),

            # 有功总电能
            0x4000 : D4000(),
        }
       
    # 定义初始化函数
    def __init__(self, name, address = 0x01):
        # 调用父函数初始化
        SlaveStation.__init__(self, name, address)
        # 设置寄存器列表
        SlaveStation.__setregs__(self, self.__regs)
        # 设置串口参数
        # 需要与设备设置保持一致
        self._set_port(9600, serial.EIGHTBITS,
            serial.PARITY_NONE, serial.STOPBITS_TWO)

    # 读取状态
    def read_info(self):
        # 打印信息
        if (self.debug) : \
            print("DDSU666.read_info : begin !")
        # 读取数据
        # 地址从0x0000开始
        # 设备描述信息寄存器共17个
        buffer = SlaveStation.read_regs(self, 0x0000, 17)
        # 检查结果
        if buffer is None or len(buffer) != 34:
            # 打印信息
            if (self.debug) : \
                print("DDSU666.read_info : fail to read !")
            return False
        # 设备描述信息寄存器
        # 编程密码
        if not self[0x0000].unpack(buffer[0 : 2]): return False
        # 软件版本号
        if not self[0x0001].unpack(buffer[2 : 4]): return False
        # 当前协议
        if not self[0x0005].unpack(buffer[10 : 12]): return False
        # 当前协议
        if not self[0x0006].unpack(buffer[12 : 14]): return False
        # 电压变比
        if not self[0x0007].unpack(buffer[14 : 16]): return False
        # 电流变比
        if not self[0x0008].unpack(buffer[16 : 18]): return False
        # 波特率
        if not self[0x000C].unpack(buffer[24 : 26]): return False
        # 开关量输出
        if not self[0x000D].unpack(buffer[26 : 28]): return False
        # 年月
        if not self[0x000E].unpack(buffer[28 : 30]): return False
        # 天时
        if not self[0x000F].unpack(buffer[30 : 32]): return False
        # 分秒
        if not self[0x0010].unpack(buffer[32 : 34]): return False
        return True
        
    # 读取状态
    def read_status(self):
        # 打印信息
        if (self.debug) : \
            print("DDSU666.read_status : begin !")
        # 读取数据
        # 地址从0x0000开始
        # 设备描述信息寄存器共20个
        buffer = SlaveStation.read_regs(self, 0x2000, 18)
        # 检查结果
        if buffer is None or len(buffer) != 36:
            # 打印信息
            if (self.debug) : \
                print("DDSU666.read_status : fail to read !")
            return False
        # 设备状态信息寄存器
        # A相电压
        if not self[0x2000].unpack(buffer[0 : 4]): return False
        # A相电流
        if not self[0x2002].unpack(buffer[4 : 8]): return False
        # 瞬时总有功功率
        if not self[0x2004].unpack(buffer[8 : 12]): return False
        # 瞬时总无功功率
        if not self[0x2006].unpack(buffer[12 : 16]): return False
        # 瞬时总视在功率
        if not self[0x2008].unpack(buffer[16 : 20]): return False
        # 总功率因素
        if not self[0x200A].unpack(buffer[20 : 24]): return False
        # 电网频率
        if not self[0x200E].unpack(buffer[28 : 32]): return False
        return True
    
    # 读取电能计数
    def get_power(self):
        # 读取电能计数
        if not self.read_reg(0x4000):
            #print("DDSU666.get_power : fail to read R[4000] !")
            return -1
        return self[0x4000].get()
    
    # 清零电能计数
    def clear_power(self):
        # 设置数值
        self[0x0002].set(1)
        # 写寄存器
        if not self.write_reg(0x4000):
            print("DDSU666.clear_power : fail to write R[4000] !")
            return False
        return True

# 定义主函数
def main():  
    # 创建设备
    myDevice = DDSU666("/dev/ttyUSB0", 0x01)

    # 读取数据
    myDevice.read_info()
    myDevice.read_status()
    #myDevice.read_items()
    
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
        print("DDSU666:__main__ :", str(e))
        print("DDSU666:__main__ : unexpected exit !")
