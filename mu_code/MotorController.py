# -*- coding: utf-8 -*
import threading
from threading import Thread

from AQMD6040BLS import *
from WheelSensor import *

class MotorController:
    # 设备句柄
    __device = None
    # 异常状态
    __error = 0
    # 中断标志
    __loop = False

    # 传感器
    __sensor = None
    # 相对位置
    # 0 - 脉冲数
    # 1 - 当前位置 （0x7FFFFFFF：无效地址)
    # 2 - 目标位置 （0x7FFFFFFF：无效地址)
    __positions = [0, 0x7FFFFFFF, 0x7FFFFFFF]

    # 线程
    __thread = None
    # 同步锁
    __lock = threading.Lock()

    # 已学习线序
    study = False
    # 额定功率(W)
    power = 800
    # 前进指示
    forward = -1
    # 最低转速(%)
    duty_ratio = 12
    # 启动时长(秒)
    skip_time = 2.0
    # 最低换向频率(Hz)
    reverse_freq = 100

    #析构方法
    #当对象被删除时，会自动被调用,然后释放内存
    def __del__(self):
        # 停止线程
        self.stop_thread()
        # 删除设备
        if self.__device is not None :
            del self.__device

    # 定义初始化函数
    def __init__(self, port, address):
        # 生成设备
        self.__device = AQMD6040BLS(port, address)
        
    # 清理错误
    def clear_error(self):
        # 自动锁
        self.__error = 0         
                
    # 是否错误
    def get_error(self):
        # 自动锁
        return self.__error

    # 设置错误
    def set_error(self, error):
        # 自动锁
        self.__error = error
                
    # 错误信息
    def error_info(self):
        if self.__error == 0x00:
            return "无错误"
        elif self.__error == 0x10:
            return "无法读取状态"
        elif self.__error == 0x11:
            return "无效的功率值"
        elif self.__error == 0x12:
            return "已到目标位置"
        elif self.__error == 0x13:
            return "超出额定功率"
        elif self.__error == 0x14:
            return "检测线程停止"
        elif self.__error == 0x15:
            return "无法读取当前位置"
        elif self.__error == 0x21:
            return "电机正转堵转"
        elif self.__error == 0x22:
            return "电机反转堵转"
        elif self.__error == 0x31:
            return "尚未学习"
        elif self.__error == 0x32:
            return "堵转停止"
        elif self.__error == 0x33:
            return "霍尔错误"
        elif self.__error == 0x34:
            return "达不到目标速度"
        elif self.__error == 0x35:
            return "线圈错误"                    
        elif self.__error == 0x36:
            return "过流关断"
        elif self.__error == 0x37:
            return "过热关断"
        elif self.__error == 0x38:
            return "过压关断"
        elif self.__error == 0x39:
            return "欠压关断"
        return "未定义"
                                
    # 设置距离函数
    def set_sensor(self, sensor):
        # 清理位置
        self.clear_abspos()
        # 设置传感器
        self.__sensor = sensor    
        
    # 读取信息
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

    # 获得输入电压
    def get_voltage(self):
        # 返回数值
        return self.get_reg(0x0038) * 0.1
    
    # 获得实时电流
    def get_current(self):
        # 返回数值
        return self.get_reg(0x0021) * 0.01

    # 获得实时功率
    def get_power(self):
        # 返回数值
        return self.get_voltage() * self.get_current()
        
    # 清理相对位置设置
    def clear_pos(self):
        # 清理位置
        self.__positions[0] = 0
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device.clear_pos()

    # 设置目标相对位置
    def set_pos(self, pos):
        # 设置位置
        self.__positions[0] = pos
        # 自动锁
        with self.__lock:
            # 设置相对位置
            return self.__device.set_pos(pos, 1)

    # 设置绝对位置
    def set_abspos(self, curr, dest):
        # 设置当前地址
        self.__positions[1] = curr
        # 设置目标地址
        self.__positions[2] = dest            

    # 清理绝对位置设置
    def clear_abspos(self):
        # 设置无效地址
        self.set_abspos(0x7FFFFFFF, 0x7FFFFFFF)

    # 获得绝对位置
    def get_abspos(self):
        # 自动锁
        with self.__lock:
            # 检查传感器
            if self.__sensor is not None:
                # 读取数值
                pos = self.\
                    __sensor.get_pos()
                # 检查结果
                if pos is not None: return pos * 1000.0
            return None

    # 停止设备
    def stop_motor(self, mode = 0):
        # 自动锁
        with self.__lock:
            # 返回数值
            return self.__device.stop_motor(mode)

    # 设置PWM
    # 设置后电机会产生相应动作！
    def set_pwm(self, pwm):
        # 设置PWM控制参数
        self.set_reg(0x0042, pwm)
        # 自动锁
        with self.__lock:
            # 设置数值
            return self.__device.write_reg(0x0042)
    
    # 设置目标和频率
    def set_freq(self, freq):
        # 设置换向频率(0.1Hz)
        self.set_reg(0x0044, freq * 10)
        # 自动锁
        with self.__lock:
            # 设置数值
            return self.__device.write_reg(0x0044, 1)

    # 向前运行直至到头（堵转）
    def move_forward(self, pwm = 0):
        # 返回结果数值
        return self.move(+1, pwm)

    # 向前运行直至到头（堵转）
    def move_backward(self, pwm = 0):
        # 返回结果数值
        return self.move(-1, pwm)

    # 运行到某个相对位置
    # 基于PWM
    def move(self, pos, pwm = 0):
        # 检查数值
        if pwm > 0 and abs(pwm) <= 100:
            # 计算PWM控制参数
            pwm = int(pwm * self.forward / 0.1)
        else:
            # 计算PWM控制参数
            pwm = int(self.duty_ratio * self.forward / 0.1)
        # 检查位置符号
        if pos < 0: pwm = - pwm

        # 清理错误
        self.clear_error()
        print("MotorController.move : 清除错误标志！")

        # 清理绝对位置
        self.clear_abspos()
        # 清理位置计数器
        if not self.clear_pos():
            print("MotorController.move : 位置无法清零！")
            return False
        print("MotorController.move : 位置已经清零！")

        # 设置相对位置
        self.__positions[0] = pos
        print("MotorController.move : 相对位置(%.2f)！"% pos)
        
        # 设置PWM控制参数
        if not self.set_pwm(pwm):
            print("MotorController.move : 无法设置占空比！")
            return False
        # 打印信息
        print("MotorController.move : 占空比已经设置！")
        return True

    # 运行到某个相对位置
    # 基于换向频率
    def moveTo(self, pos, freq = 0):
        # 检查数值
        if freq <= 0 or freq > 1000:
            # 计算PWM控制参数
            freq = self.reverse_freq

        # 清理错误
        self.clear_error()
        print("MotorController.moveTo : 清除错误标志！")

        # 清理绝对位置
        self.clear_abspos()
        # 清理位置计数器
        if not self.clear_pos():
            print("MotorController.moveTo : 位置无法清零！")
            return False
        print("MotorController.moveTo : 位置已经清零！")
        
        # 设置相对位置模式
        if not self.set_pos(pos * self.forward):
            print("MotorController.move : 无法设置相对位置！")
            return False
        print("MotorController.move : 相对位置已设置！")
        
        # 设置控制参数
        if not self.set_freq(freq):
            print("MotorController.moveTo : 无法设置频率！")
            return False
        # 打印信息
        print("MotorController.moveTo : 频率已经设置！")
        return True

    # 运动到某个绝对位置
    # 基于PWM (单位：毫米)
    def moveAbs(self, pos, pwm = 0):
        # 获得当前位置
        curr_pos = self.get_abspos()
        # 检查结果
        if curr_pos is None:
            print("MotorController.moveAbs : 无法读取当前位置！")
            return False
        # 打印信息
        print("MotorController.moveAbs : 当前位置(%f)毫米，目标位置(%f)毫米！"% \
            (curr_pos, pos))
        # 距离
        distance = pos - curr_pos
        # 检查距离
        if abs(distance) < 10:
            print("MotorController.moveAbs : 已在当前位置！")
            return True
                    
        # 清理错误
        self.clear_error()
        print("MotorController.moveAbs : 清除错误标志！")
        
        # 设置绝对位置
        self.set_abspos(curr_pos, pos)
        print("MotorController.moveAbs : 绝对位置已经设置！")

        # 设置相对位置
        self.__positions[0] = \
            +1 if distance > 0 else -1
        print("MotorController.moveAbs : 运动方向已经设置！")
        
        # 检查数值
        if pwm > 0 and abs(pwm) <= 100:
            # 计算PWM控制参数
            pwm = int(pwm * self.forward / 0.1)
        else:
            # 计算PWM控制参数
            pwm = int(self.duty_ratio * self.forward / 0.1)
        # 检查位置符号
        if self.__positions[0] < 0: pwm = - pwm
        # 设置PWM控制参数
        if not self.set_pwm(pwm):
            print("MotorController.moveAbs : 无法设置占空比！")
            return False
        # 打印信息
        print("MotorController.moveAbs : 占空比已经设置！")
        return True
    
    # 是否处于活动状态
    def is_alive(self):
        # 检查参数
        if self.__thread is None:
            return False
        # 返回结果
        return self.__thread.is_alive()
        
    # 停止线程
    def stop_thread(self):
        # 检查参数
        if self.__thread is not None:
            # 设置标记位
            self.__loop = True
            # 等待结束
            self.__thread.join()
        # 清理线程
        self.__thread = None
        # 打印信息
        print("MotorController.stop_thread : 线程已经停止 !")

    # 开启线程
    def start_thread(self):
        # 检查参数
        if self.__thread is not None:
            # 检查线程活性
            if self.__thread.is_alive():
                # 打印信息
                print("MotorController.start_thread : 处于活动状态 !")
                return True
            # 清理线程
            self.__thread = None
        # 检查线程
        if self.__thread is None:
            # 创建线程
            thread = Thread(target = self.__run, args = ())
            # 启动线程
            thread.start()
            # 设置线程
            self.__thread = thread
        # 打印信息
        print("MotorController.start_thread : 线程已经启动 !")
        # 返回结果
        return True
           
    # 运行函数
    def __run(self):
        # 执行函数
        try:
            # 实时功率
            power = 0
            # 计数器
            timeout = 0
            # 清理中断标志
            self.__loop = False
            # 开始检测设备功率
            while not self.__loop:
                # 等待一段时间
                time.sleep(0.01)
                # 错误标记
                error = 0
                # 读取设备状态
                if not self.read_status():
                    # 设置错误
                    error = 0x10
                    # 打印信息
                    print("MotorController.__run : 无法读取设备状态！")
                # 读取设备功率
                power = self.get_power()
                # 检查功率
                if power < self.power:
                    # 计数器清零
                    timeout = 0
                else:
                    # 计数器加一
                    timeout = timeout + 1
                # 检查功率
                if power < 0:
                    # 设置标记位
                    error = 0x11
                    # 打印信息
                    print("MotorController.__run : 无效的功率数值！")
                # 读取堵转状态
                if self.get_reg(0x0032) != 0:
                    # 设置标记位
                    error = 0x20 | (self.get_reg(0x0032) & 0x0F)
                    # 打印信息
                    print("MotorController.__run : %s !"% self.reg_info(0x0032))                    
                # 读取错误状态
                if self.get_reg(0x0033) != 0:
                    # 设置标记位
                    error = 0x30 | (self.get_reg(0x0033) & 0x0F)
                    # 打印信息
                    print("MotorController.__run : %s ！"% self.reg_info(0x0033))
                # 检查超时
                if timeout > 10 * self.skip_time:
                    # 设置标记位
                    error = 0x13
                    # 打印信息
                    print("MotorController.__run : 实时功率(%dW)超出额定功率！"% power)
                # 检查位置
                if self.__sensor is None or \
                    abs(self.__positions[1]) > 100000 or \
                        abs(self.__positions[2]) > 100000:
                    # 绝对位置设置无效，则凭相对位置判断
                    if abs(self.__positions[0]) > 1 and \
                        abs(self.get_reg(0x0024)) >= abs(self.__positions[0]):
                        # 设置标记位
                        error = 0x12
                        # 清理位置标记
                        self.__positions[0] = 0
                        # 打印信息
                        print("MotorController.__run : 已到达相对目标位！")
                else:
                    # 获得当前位置
                    curr_pos = self.get_abspos()
                    # 检查结果
                    if curr_pos is None:
                        # 设置错误数值
                        error = 0x15
                        # 打印信息
                        print("MotorController.__run : 无法读取当前位置！")
                    else:
                        # 计算当前距离
                        curr_dist = self.__positions[2] - curr_pos 
                        # 计算距离
                        distance = self.__positions[2] - self.__positions[1]
                        #打印数据
                        #print("MotorController.__run : x=%.2fmm，Δ=%.2fmm，δ=%.2fmm"% (curr_pos, distance, curr_dist))
                        # 检查结果
                        if distance * curr_dist <= 0:
                            # 设置标记位
                            error = 0x12
                            # 清理位置标记
                            self.clear_abspos()
                            # 打印信息
                            print("MotorController.__run : 已到达绝对目标位！")
                # 检查标记位
                if error != 0:
                    # 设置错误
                    self.set_error(error)
                    # 停止执行
                    if not self.stop_motor():
                        # 打印信息
                        print("MotorController.__run : 无法停止设备！")
                    # 打印信息
                    print("MotorController.__run : 检测到错误状态！")
                    print("\terror = %s (%s)"% (hex(error), self.error_info()))          
        # 处理异常
        except Exception as e:
            # 设置错误
            self.set_error(0x14)
            # 打印错误
            traceback.print_exc()
            print("MotorController.__run :", str(e))
            print("MotorController.__run : unexpected exit !")          

        # 打印信息
        print("MotorController.__run : 线程已经停止！")

    # 初始化设备
    def init_device(self, force = False):
        
        # 读取设备信息
        if not self.read_info():
            print("MotorController.init_device : 无法读取设备信息！")
            return False
        
        # 读取设备状态
        if not self.read_status():
            print("MotorController.init_device : 无法读取设备状态！")
            return False
            
        # 获得输入电压
        voltage = self.get_voltage()
        # 检查结果
        if voltage < 0:
            print("MotorController.init_device : 无效的输入电压！")
            return False
        # 打印结果
        print("MotroController.init_device : 输入电压%fV"%voltage)

        # 获得实时电流
        current = self.get_current()
        # 检查结果
        if current < 0:
            print("MotorController.init_device : 无效的实时电流！")
            return False
        # 打印结果
        print("MotroController.init_device : 实时电流%fA"%current)
            
        # 初始化电机
        if not self.__device.init_motor(force) :
            print("MotorController.init_device : 未能初始化电机 !")
            return False
        
        # 电机成功初始化
        print("MotorController.init_device : 电机成功初始化 !")

        # 发送停止指令
        # 正常停止
        if not self.stop_motor():
            # 打印信息
            print("MotorController.init_device : 未能停止电机 !")
            return False

        # 返回结果
        return True

# 定义主函数
def main():

    # 创建控制器
    myController = MotorController("/dev/ttyUSB0", 0x05)

    # 检查设备是否存在
    if myController.read_info():
        # 打印信息
        print("MotorController.main : 设备存在 !")
        # 初始化设备
        if myController.init_device():
            # 打印信息
            print("MotorController.main : 设备初始化成功！")
        else:
            # 打印信息
            print("MotorController.main : 设备初始化失败！")        
    else:
        # 打印信息
        print("MotorController.main : 设备不存在 !")

    # 删除控制器
    del myController

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("MotorController.__main__ :", str(e))
        print("MotorController.__main__ : unexpected exit !")