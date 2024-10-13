# -*- coding: utf-8 -*

from DDSU666 import *

import threading
from threading import Thread

class EnergySensor:
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
        self.__device = DDSU666(port, address)
   
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
    
    # 读取状态
    def read_info(self):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device.read_info()

    # 读取状态
    def read_status(self):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device.read_status()
    
    # 读取电能计数
    def get_power(self):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device.get_power()

    # 清零电能计数
    def clear_power(self):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device.clear_power()

# 定义主函数
def main():

    # 创建传感器
    mySensor = EnergySensor("/dev/ttyUSB0", 0x01)

    # 检查传感器
    if mySensor.get_power() >= 0:
        print("电能计数：%fKW"% mySensor.get_power())
    else:
        print("EnergySensor.main : sensor not exists !")

    # 删除传感器
    del mySensor

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("EnergySensor.__main__ :", str(e))
        print("EnergySensor.__main__ : unexpected exit !")