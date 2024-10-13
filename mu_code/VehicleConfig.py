import os
import binascii
import traceback
import configparser

class VehicleConfig:
    # 配置文件
    __config = None
    # 区划配置
    __sections = \
        [\
            "Vehicle", \
            "Wheel Sensor", \
            "Charge Sensor", \
            "Weight Sensor", \
            "Motor Controller"]

    #析构方法
    #当对象被删除时，会自动被调用,然后释放内存
    def __del__(self):
        # 删除配置
        if self.__config is not None:
            del self.__config

    # 定义初始化函数
    def __init__(self):
        # 初始化
        self.__config = configparser.ConfigParser()

    # 检查是否存在
    def exists(self, fileName = 'config.ini'):
        # 检查配置文件是否存在
        if not os.path.exists(fileName):
            print("VehicleConfig.exists : 无法找到配置文件 !")
            return False
        # 读取配置文件
        self.__config.read(fileName, encoding = "utf-8")
        return True

    # 增加区域
    def add_section(self, ind):
        self.__config.add_section(self.__sections[ind])

    # 检查区域
    def has_section(self, ind):
        # 返回结果
        return self.__config.has_section(self.__sections[ind])
    
    # 检查选项
    def has_option(self, ind, name):
        # 返回结果
        return self.__config.has_option(self.__sections[ind], name)

    # 设置选项
    def set_option(self, ind, name, value):
        # 设置数值
        self.__config.set(self.__sections[ind], name, str(value))
        
    # 获得Port参数
    def get_port(self, ind, default):
        # 检查参数
        if not self.has_option(ind, "port"):
            self.set_option(ind, "port", default)
            return default
        # 读取参数
        port = self.__config.get(self.__sections[ind], "port")
        # 检查参数
        if port.find("/dev/tty") != 0:
            self.set_option(ind, "port", default)
            return default
        # 返回数值
        return port
    
    # 获得Address参数
    def get_address(self, ind, default):
        # 检查参数
        if not self.has_option(ind, "address"):
            self.set_option(ind, "address", default)
            return default
        # 读取参数
        address = self.__config.getint(self.__sections[ind], "address")
        # 检查参数
        if address < 0 or address > 127:
            self.set_option(ind, "address", default)
            return default
        # 返回数值
        return address

    # 获得LeaveCount参数
    def get_leave_count(self, default):
        # 检查参数
        if not self.has_option(0, "leave_count"):
            self.set_option(0, "leave_count", default)
            return default
        # 读取参数
        count = self.__config.getint(self.__sections[0], "leave_count")
        # 检查参数
        if count <= 0 or count > 100:
            self.set_option(0, "leave_count", default)
            return default
        # 返回数值
        return count
                
    # 设置PulseCount参数
    def set_pulse_count(self, value):
         # 检查参数
        if value > 1000 and value < 100000:
            self.set_option(0, "pulse_count", value)

    # 获得PulseCount参数
    def get_pulse_count(self, default):
        # 检查参数
        if not self.has_option(0, "pulse_count"):
            self.set_option(0, "pulse_count", default)
            return default
        # 读取参数
        count = self.__config.getint(self.__sections[0], "pulse_count")
        # 检查参数
        if count <= 1000 or count > 100000:
            self.set_option(0, "pulse_count", default)
            return default
        # 返回数值
        return count
    
    # 设置RailDist参数
    def set_rail_dist(self, value):
         # 检查参数
        if value > 0 and value < 100000:
            self.set_option(0, "rail_dist", value)
        
    # 获得RailDist参数
    def get_rail_dist(self, default):
        # 检查参数
        if not self.has_option(0, "rail_dist"):
            self.set_option(0, "rail_dist", default)
            return default
        # 读取参数
        return self.__config.getint(self.__sections[0], "rail_dist")    

    # 获得Study参数
    def get_study(self, default):
         # 检查参数
        if not self.has_option(4, "study"):
            self.set_option(4, "study", default)
            return default
        # 读取参数
        return self.__config.getboolean(self.__sections[4], "study")

    # 获得Power参数
    def get_power(self, default):
         # 检查参数
        if not self.has_option(4, "power"):
            self.set_option(4, "power", default)
            return default
        # 读取参数
        power = self.__config.getint(self.__sections[4], "power")
        # 检查结果
        if power < 100 or power > 5000:
            self.set_option(4, "power", default)
            return default
        # 返回数值
        return power
       
    # 获得Forward参数
    def get_forward(self, default):
        # 检查参数
        if not self.has_option(4, "forward"):
            self.set_option(4, "forward", default)
            return default
        # 读取参数
        forward = self.__config.getint(self.__sections[4], "forward")
        # 检查结果
        if not forward in [-1, +1]:
            self.set_option(4, "forward", default)
            return default
        # 返回数值
        return forward
    
    # 获得DutyRatio参数
    def get_duty_ratio(self, default):
        # 检查参数
        if not self.has_option(4, "duty_ratio"):
            self.set_option(4, "duty_ratio", default)
            return default
        # 读取参数
        duty_ratio = self.__config.getfloat(self.__sections[4], "duty_ratio")
        # 检查结果
        if duty_ratio < -100 or duty_ratio > +100:
            self.set_option(4, "duty_ratio", default)
            return default
        # 返回数值
        return duty_ratio
    
    # 获得SkipTime参数
    def get_skip_time(self, default):
        # 检查参数
        if not self.has_option(4, "skip_time"):
            self.set_option(4, "skip_time", default)
            return default
        # 读取参数
        skip_time = self.__config.getfloat(self.__sections[4], "skip_time")
        # 检查结果
        if skip_time < 0 or skip_time > 15:
            self.set_option(4, "skip_time", default)
            return default
        # 返回数值
        return skip_time
    
    # 获得ReverseFreq参数
    def get_reverse_freq(self, default):
        # 检查参数
        if not self.has_option(4, "reverse_freq"):
            self.set_option(4, "reverse_freq", default)
            return default
        # 读取参数
        reverse_freq = self.__config.getfloat(self.__sections[4], "reverse_freq")
        # 检查结果
        if reverse_freq <= 0 or reverse_freq > 1000:
            self.set_option(4, "reverse_freq", default)
            return default
        # 返回数值
        return reverse_freq

    # 加载配置
    def load_conf(self, fileName = 'config.ini'):
        # 检查配置文件是否存在
        if not self.exists(fileName = 'config.ini'):
            print("VehicleConfig.load_conf : 无法找到配置文件 !")
            return False

        for i in range(0, len(self.__sections)):
            # 检查区划，并增加区划
            if not self.has_section(i): self.add_section(i)                

        # Vehicle
        self.get_rail_dist(3020)
        self.get_leave_count(300)
        self.get_pulse_count(1039)

        # 计米器
        self.get_port(1, "/dev/ttyUSB0")
        self.get_address(1, 0x03)
        
        # 电能表
        self.get_port(2, "/dev/ttyUSB0")
        self.get_address(2, 0x01)

        # 称重传感器
        self.get_port(3, "/dev/ttyUSB1")
        self.get_address(3, 0x01)

        # 电机控制器
        self.get_port(4, "/dev/ttyUSB0")
        self.get_address(4, 0x05)
        # 电机控制器参数
        self.get_study(False)
        self.get_power(800)
        self.get_forward(-1)
        self.get_duty_ratio(12)
        self.get_skip_time(2.0)
        self.get_reverse_freq(20)

        # 返回结果
        return True
    
    # 保存配置
    def save_conf(self, fileName = 'config.ini'):
        # 保存配置文件
        with open(fileName, "w", encoding = "utf-8") as file:
            self.__config.write(file)

# 定义主函数
def main():

    # 创建小车
    myConfig = VehicleConfig()
    # 加载配置文件
    myConfig.load_conf()

    # 保存配置文件
    myConfig.save_conf()
    # 删除小车
    del myConfig

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("Vehicle:__main__ :", str(e))
        print("Vehicle:__main__ : unexpected exit !")