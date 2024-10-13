# -*- coding: utf-8 -*

from SD76C import *

import threading
from threading import Thread

class WheelSensor:
    # 设备句柄
    __device = None
    # 同步锁
    __lock = threading.Lock()
    
    #析构方法
    #当对象被删除时，会自动被调用,然后释放内存
    def __del__(self):
        # 删除设备
        if self.__device is not None :
            del self.__device
            
    # 定义初始化函数
    def __init__(self, port, address):
        # 生成设备
        self.__device = SD76C(port, address)
        
    # 寄存器信息
    def reg_info(self, ind):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device[ind].info
    
    # 获得寄存器数值
    def get_reg(self, ind):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device[ind].get()
    
    # 设置寄存器数值
    def set_reg(self, ind, value):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device[ind].set(value)
    
    # 复位所有数值
    def reset(self):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device.reset()

    # 读取位置信息
    def get_pos(self):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device.get_pos()

    # 读取寄存器
    def read_status(self):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device.read_reg(0x0000)

# 定义主函数
def main():

    # 创建传感器
    mySensor = WheelSensor("/dev/ttyUSB1", 0x03)

    # 读取传感器
    pos = mySensor.get_pos()
    # 检查结果
    if pos is not None:
        print("当前位置：%f米"% pos)
    else:
        print("WheelSensor.main : sensor not exists !")

    # 删除传感器
    del mySensor

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("WheelSensor.__main__ :", str(e))
        print("WheelSensor.__main__ : unexpected exit !")