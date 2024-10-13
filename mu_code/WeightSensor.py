# -*- coding: utf-8 -*

from YP353 import *

import threading
from threading import Thread

class WeightSensor:
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
        self.__device = YP353(port, address)
   
    # 读取重量计数
    def get_weight(self):
        # 自动锁
        with self.__lock:
            # 返回结果
            return self.__device.get_weight()

# 定义主函数
def main():

    # 创建传感器
    mySensor = WeightSensor("/dev/ttyUSB1", 0x01)

    # 检查传感器
    if mySensor.get_weight() is not None:
        (status, value) = mySensor.get_weight()
        print("称重计数：%d"% value)
        print("计数状态：0x%04x"% status)
    else:
        print("WeightSensor.main : sensor not exists !")

    # 删除传感器
    del mySensor

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("WeightSensor.__main__ :", str(e))
        print("WeightSensor.__main__ : unexpected exit !")