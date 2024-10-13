# -*- coding: utf-8 -*

from threading import *

from VehicleConfig import *

from WheelSensor import *
from EnergySensor import *
from WeightSensor import *
from MotorController import *

class Vehicle:  
    # 配置文件
    config = None
    # 配置参数
    rail_dist = 1039
    leave_count = 100
    pulse_count = 3020

    # 位置传感器
    __wheelSensor = None
    # 电能表设备
    __energySensor = None
    # 称重传感器
    __weightSensor = None
    # 后桥电机控制器
    __motorController = None
    
    # 定义初始化函数
    def __init__(self):
        # 生成缺省配置
        self.config = VehicleConfig()

    # 获得电机
    def get_motor(self):
        return self.__motorController
    
    # 重置原点
    def set_origin(self):
        # 返回指令执行结果
        return self.__wheelSensor.reset()
    
    # 返回当前位置
    def get_abspos(self):
        # 返回指令执行结果
        return self.__wheelSensor.get_pos()

    # 返回称重值
    def get_weight(self):
        # 返回指令执行结果
        return self.__weightSensor.get_weight()

    # 返回电能之
    def get_power(self):
        # 返回指令执行结果
        return self.__energySensor.get_power()

    # 中断指令
    def stop_motor(self):
        # 返回指令执行结果
        return self.__motorController.stop_motor()
        
    # 运动到某个绝对位置
    # 基于PWM (单位：毫米)
    def moveAbs(self, pos, pwm = 0):
        # 返回执行结果
        return self.__motorController.moveAbs(pos, pwm)

    # 前进直至堵转
    # 基于配置文件的PWM设置
    def move_forward(self, pwm = 0):
        # 返回指令执行结果
        return self.__motorController.move_forward(pwm)
    
    # 后退直至堵转
    # 基于配置文件的PWM设置
    def move_backward(self, pwm = 0):
        # 返回指令执行结果
        return self.__motorController.move_backward(pwm)

    # 运动到某个相对位置
    # 基于PWM (单位：毫米)
    def move(self, pos, pwm = 0):
        # 将位置从毫米换算成脉冲数
        pulse = int(pos * self.pulse_count / self.rail_dist)
        # 打印信息
        print("Vehicle.move : 脉冲数(%d)！"% pulse)
        # 执行移动指令
        return self.__motorController.\
            move(pulse, pwm) * self.rail_dist / self.pulse_count

    # 运动到某个相对位置
    # 基于换向频率 (单位：毫米)
    def moveTo(self, pos, freq = 0):
        # 将位置从毫米换算成脉冲数
        pulse = int(pos * self.pulse_count / self.rail_dist)
        # 打印信息
        print("Vehicle.moveTo : 脉冲数(%d)！"% pulse)
        # 执行移动指令
        return self.__motorController.\
            moveTo(pulse, freq) * self.rail_dist / self.pulse_count
            
    # 开启线程
    def stop_thread(self):
        # 返回执行结果
        return self.__motorController.stop_thread()        

    # 开启线程
    def start_thread(self):
        # 返回执行结果
        return self.__motorController.start_thread()

    # 创建设备
    def init_Vehicle(self):
        # 加载配置
        self.config.load_conf()
        
        # 设置参数
        self.rail_dist = self.config.\
            get_rail_dist(self.rail_dist)
        self.leave_count = self.config.\
            get_leave_count(self.leave_count)
        self.pulse_count = self.config.\
            get_pulse_count(self.pulse_count)
        
        # 创建设备
        self.__wheelSensor = WheelSensor(\
            self.config.get_port(1, "dev/ttyUSB0"),\
                self.config.get_address(1, 0x03))

        # 创建设备
        self.__energySensor = EnergySensor(\
            self.config.get_port(2, "/dev/ttyUSB0"),\
                self.config.get_address(2, 0x01))
        
        # 创建设备
        self.__weightSensor = WeightSensor(\
            self.config.get_port(3, "/dev/ttyUSB1"),\
                self.config.get_address(3, 0x03))
        
        # 创建设备
        self.__motorController = MotorController(\
            self.config.get_port(4, "/dev/ttyUSB0"),\
                self.config.get_address(4, 0x05))
        # 设置传感器
        self.__motorController.set_sensor(self.__wheelSensor)
        # 设置学习标志
        self.__motorController.study = \
            self.config.get_study(self.__motorController.study)
        # 设置额定功率
        self.__motorController.power = \
            self.config.get_power(self.__motorController.power)
        # 设置前进方向
        self.__motorController.forward = \
            self.config.get_forward(self.__motorController.forward)
        # 设置运行速度
        self.__motorController.duty_ratio = \
            self.config.get_duty_ratio(self.__motorController.duty_ratio)
        # 设置启动时长
        self.__motorController.skip_time = \
            self.config.get_skip_time(self.__motorController.skip_time)
        # 设置换向频率
        self.__motorController.reverse_freq = \
            self.config.get_reverse_freq(self.__motorController.reverse_freq)
            
        # 检查学习标志
        if not self.__motorController.study:
            # 初始化设备
            if not self.__motorController.init_device():
                print("Vehicle.init_device : 无法初始化设备！")
                return False
            # 设置标记位
            self.config.set_option(4, "study", "1")

        # 停止电机
        if not self.__motorController.stop_motor():
            # 打印信息
            print("Vehicle.init_device : 无法停止后桥电机！")
            return False
        # 返回结果
        return True

    # 移动至自动充电
    # 基于配置文件的PWM设置    
    def moveto_charger(self):
        # 读取电能设备
        power = self.__energySensor.get_power()
        # 检查结果
        if power > 0:
            print("Vehicle.moveto_charger : 已经在充电！")
            return True

        # 退回设备
        position = self.move_backward()
        # 检查结果
        if position < 0:
            print("Vehicle.moveto_charger : 无法移动小车！")
            return False
        
        print("Vehicle.moveto_charger : 等待延迟开关！")
        # 等待一段时间
        time.sleep(5)

        print("Vehicle.moveto_charger : 等待电能表启动！")
        # 等待一段时间
        time.sleep(5)

        # 读取电能设备
        power = self.__energySensor.get_power()
        # 检查结果
        if power < 0:
            print("Vehicle.moveto_charger : 充电装置异常！")
            return False
        # 返回结果
        return True

    # 离开自动充电装置
    # 基于配置文件的PWM设置    
    def leave_charger(self):
        # 读取电能设备
        power = self.__energySensor.get_power()
        # 检查结果
        if power < 0:
            print("Vehicle.leave_charger : 已经离开！")
            return True
        # 循环处理
        while power > 0:
            # 移动一小段距离
            if not self.move(self.leave_count):
                print("Vehicle.leave_charger : 无法前进！")
                return False
            # 再次读取电表数值
            power = self.__energySensor.get_power()
        # 检查结果
        if power < 0:
            print("Vehicle.leave_charger : 已经离开！")
            return True
        return False

# 定义主函数
def main():

    # 创建小车
    myVechile = Vehicle()

    # 创建设备
    if myVechile.init_Vehicle():

        # 设置原点
        myVechile.set_origin()
        # 测量比例
        #myVechile.set_scale(1000)

    else:
        print("Vehicle.main : 无法初始化设备！")
            
    # 删除小车
    del myVechile

    # 等待键盘消息
    #input("Vehicle.main : 按下Enter键结束当前程序！\r\n")

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("Vehicle:__main__ :", str(e))
        print("Vehicle:__main__ : unexpected exit !")