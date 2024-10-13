import tkinter
from tkinter import ttk
from tkinter import messagebox

from MainWindow import *
from Vehicle import *
from VehicleConfig import *

class VehicleFrame:
    # 窗口句柄
    __mainWindow = None

    def __init__(self, mainWindow, frame):
        # 设置缺省值
        self.vehicle = None
        # 设置窗口
        self.__mainWindow = mainWindow
        # 初始化菜单
        self.__initFrame(frame)
        
    # 初始化标签窗口
    def __initFrame(self, frame):
        # 连接按钮
        self.connTxt = tkinter.StringVar()
        self.connTxt.set("连接设备")
        self.connButton = tkinter.Button(frame, \
            textvariable = self.connTxt, command = self.connAction)
        self.connButton.grid(row = 0, column = 0, sticky = tkinter.E)

        # 串口配置
        tkinter.Label(frame, text = "后桥电机串口：").\
            grid(row = 0, column = 1, sticky = tkinter.E)
        self.pnEditor4 = tkinter.Text(frame, height = 1, width = 15, bg = "lightgrey")
        self.pnEditor4.grid(row = 0, column = 2, sticky = tkinter.W)
        self.pnEditor4.bind("<KeyPress>", lambda f : "break")

        # 地址配置
        tkinter.Label(frame, text = "后桥电机地址：").\
            grid(row = 0, column = 3, sticky = tkinter.E)
        self.addrEditor4 = tkinter.Text(frame, height = 1, width = 5, bg = "lightgrey")
        self.addrEditor4.grid(row = 0, column = 4, sticky = tkinter.W)
        self.addrEditor4.bind("<KeyPress>", lambda f : "break")

        # 串口配置
        tkinter.Label(frame, text = "电能表串口：").\
            grid(row = 0, column = 5, sticky = tkinter.E)
        self.pnEditor2 = tkinter.Text(frame, height = 1, width = 15, bg = "lightgrey")
        self.pnEditor2.grid(row = 0, column = 6, sticky = tkinter.W)
        self.pnEditor2.bind("<KeyPress>", lambda f : "break")

        # 地址配置
        tkinter.Label(frame, text = "电能表地址：").\
            grid(row = 0, column = 7, sticky = tkinter.E)
        self.addrEditor2 = tkinter.Text(frame, height = 1, width = 5, bg = "lightgrey")
        self.addrEditor2.grid(row = 0, column = 8, sticky = tkinter.W)
        self.addrEditor2.bind("<KeyPress>", lambda f : "break")
        
        # 串口配置
        tkinter.Label(frame, text = "称重传感器串口：").\
            grid(row = 1, column = 1, sticky = tkinter.E)
        self.pnEditor3 = tkinter.Text(frame, height = 1, width = 15, bg = "lightgrey")
        self.pnEditor3.grid(row = 1, column = 2, sticky = tkinter.W)
        self.pnEditor3.bind("<KeyPress>", lambda f : "break")

        # 地址配置
        tkinter.Label(frame, text = "称重传感器地址：").\
            grid(row = 1, column = 3, sticky = tkinter.E)
        self.addrEditor3 = tkinter.Text(frame, height = 1, width = 5, bg = "lightgrey")
        self.addrEditor3.grid(row = 1, column = 4, sticky = tkinter.W)
        self.addrEditor3.bind("<KeyPress>", lambda f : "break")
        
        # 串口配置
        tkinter.Label(frame, text = "计米器串口：").\
            grid(row = 1, column = 5, sticky = tkinter.E)
        self.pnEditor1 = tkinter.Text(frame, height = 1, width = 15, bg = "lightgrey")
        self.pnEditor1.grid(row = 1, column = 6, sticky = tkinter.W)
        self.pnEditor1.bind("<KeyPress>", lambda f : "break")

        # 地址配置
        tkinter.Label(frame, text = "计米器地址：").\
            grid(row = 1, column = 7, sticky = tkinter.E)
        self.addrEditor1 = tkinter.Text(frame, height = 1, width = 5, bg = "lightgrey")
        self.addrEditor1.grid(row = 1, column = 8, sticky = tkinter.W)
        self.addrEditor1.bind("<KeyPress>", lambda f : "break")
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 2, column = 0, rowspan = 1, columnspan = 9, sticky = "EW", padx = 5, pady = 5)
            
        # 配置按钮
        self.infoButton = tkinter.Button(frame, \
            text = "小车参数", command = self.configAction)
        self.infoButton.grid(row = 5, column = 0, sticky = tkinter.E)
        
        # 边距
        tkinter.Label(frame, text = "边距(脉冲数)：").\
            grid(row = 5, column = 1, sticky = tkinter.E)
        self.bridgeEditor = tkinter.Text(frame, height = 1, width = 10)
        #self.bridgeEditor.bind("<KeyPress>", lambda f : "break")
        self.bridgeEditor.grid(row = 5, column = 2, sticky = tkinter.W)

        # 轨道总长
        tkinter.Label(frame, text = "轨道总长(毫米)：").\
            grid(row = 5, column = 3, sticky = tkinter.E)
        self.railEditor = tkinter.Text(frame, height = 1, width = 10)
        #self.railEditor.bind("<KeyPress>", lambda f : "break")
        self.railEditor.grid(row = 5, column = 4, sticky = tkinter.W)

        # 总脉冲数
        tkinter.Label(frame, text = "总脉冲数：").\
            grid(row = 5, column = 5, sticky = tkinter.E)
        self.pulseEditor = tkinter.Text(frame, height = 1, width = 10)
        #self.pulseEditor.bind("<KeyPress>", lambda f : "break")
        self.pulseEditor.grid(row = 5, column = 6, sticky = tkinter.W)
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 6, column = 0, rowspan = 1, columnspan = 7, sticky = "EW", padx = 5, pady = 5)

        # 配置按钮
        self.statusButton = tkinter.Button(frame, \
            text = "小车状态", command = self.statusAction)
        self.statusButton.grid(row = 7, column = 0, sticky = tkinter.E)
        
        # 计米器
        tkinter.Label(frame, text = "计米器(毫米)：").\
            grid(row = 7, column = 1, sticky = tkinter.E)
        self.meterEditor = tkinter.Text(frame, height = 1, width = 15, bg = "yellow")
        self.meterEditor.bind("<KeyPress>", lambda f : "break")
        self.meterEditor.grid(row = 7, column = 2, sticky = tkinter.W)

        # 称重传感器
        tkinter.Label(frame, text = "称重数值(公斤)：").\
            grid(row = 7, column = 3, sticky = tkinter.E)
        self.weightEditor = tkinter.Text(frame, height = 1, width = 10, bg = "yellow")
        self.weightEditor.bind("<KeyPress>", lambda f : "break")
        self.weightEditor.grid(row = 7, column = 4, sticky = tkinter.W)

        # 电能表
        tkinter.Label(frame, text = "有功总电能(KWH)：").\
            grid(row = 7, column = 5, sticky = tkinter.E)
        self.epEditor = tkinter.Text(frame, height = 1, width = 15, bg = "yellow")
        self.epEditor.bind("<KeyPress>", lambda f : "break")
        self.epEditor.grid(row = 7, column = 6, sticky = tkinter.W)

        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 8, column = 0, rowspan = 1, columnspan = 7, sticky = "EW", padx = 5, pady = 5)

        # 后桥参数
        self.miButton = tkinter.Button(frame, \
            text = "后桥参数", command = self.configAction)
        self.miButton.grid(row = 9, column = 0, sticky = tkinter.E)
        
        # 额定功率
        tkinter.Label(frame, text = "额定功率(W)：").\
            grid(row = 9, column = 1, sticky = tkinter.E)
        self.powerEditor = tkinter.Text(frame, height = 1, width = 10)
        self.powerEditor.grid(row = 9, column = 2, sticky = tkinter.W)
        
        # 学习状态
        tkinter.Label(frame, text = "学习状态：").\
            grid(row = 9, column = 3, sticky = tkinter.E)
        self.studyEditor = tkinter.Text(frame, height = 1, width = 10)
        self.studyEditor.grid(row = 9, column = 4, sticky = tkinter.W)

        # 前进标识
        tkinter.Label(frame, text = "前进标识：").\
            grid(row = 9, column = 5, sticky = tkinter.E)
        self.forwardEditor = tkinter.Text(frame, height = 1, width = 10)
        self.forwardEditor.grid(row = 9, column = 6, sticky = tkinter.W)

        # 超功率时长
        tkinter.Label(frame, text = "超功率时长(秒)：").\
            grid(row = 10, column = 1, sticky = tkinter.E)
        self.stEditor = tkinter.Text(frame, height = 1, width = 10)
        self.stEditor.grid(row = 10, column = 2, sticky = tkinter.W)

        # 最低占空比
        tkinter.Label(frame, text = "最低占空比(%)：").\
            grid(row = 10, column = 3, sticky = tkinter.E)
        self.mpEditor = tkinter.Text(frame, height = 1, width = 10)
        self.mpEditor.grid(row = 10, column = 4, sticky = tkinter.W)
        
        # 最低换向频率
        tkinter.Label(frame, text = "最低频率(Hz)：").\
            grid(row = 10, column = 5, sticky = tkinter.E)
        self.mfEditor = tkinter.Text(frame, height = 1, width = 10)
        self.mfEditor.grid(row = 10, column = 6, sticky = tkinter.W)

        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 11, column = 0, rowspan = 1, columnspan = 7, sticky = "EW", padx = 5, pady = 5)
            
        # 状态按钮
        self.msButton = tkinter.Button(frame, \
            text = "后桥状态", command = self.motorAction)
        self.msButton.grid(row = 12, column = 0, sticky = tkinter.E)
        
        # 内部温度
        tkinter.Label(frame, text = "内部温度(°C)：").\
            grid(row = 12, column = 1, sticky = tkinter.E)
        self.tmpEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.tmpEditor.bind("<KeyPress>", lambda f : "break")
        self.tmpEditor.grid(row = 12, column = 2, sticky = tkinter.W)

        # 实时电流
        tkinter.Label(frame, text = "实时电流(A)：").\
            grid(row = 12, column = 3, sticky = tkinter.E)
        self.rcEditor = tkinter.Text(frame, height = 1, width = 10, bg = "yellow")
        self.rcEditor.bind("<KeyPress>", lambda f : "break")
        self.rcEditor.grid(row = 12, column = 4, sticky = tkinter.W)
        
        # 堵转状态
        tkinter.Label(frame, text = "堵转状态：").\
            grid(row = 12, column = 5, sticky = tkinter.E)
        self.blockedEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.blockedEditor.bind("<KeyPress>", lambda f : "break")
        self.blockedEditor.grid(row = 12, column = 6, sticky = tkinter.W)
    
        # 错误状态
        tkinter.Label(frame, text = "错误状态：").\
            grid(row = 12, column = 7, sticky = tkinter.E)
        self.errorEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.errorEditor.bind("<KeyPress>", lambda f : "break")
        self.errorEditor.grid(row = 12, column = 8, sticky = tkinter.W)
        
        # 电源电压
        tkinter.Label(frame, text = "电源电压(V)：").\
            grid(row = 13, column = 1, sticky = tkinter.E)
        self.svEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.svEditor.bind("<KeyPress>", lambda f : "break")
        self.svEditor.grid(row = 13, column = 2, sticky = tkinter.W)
        
        # 位置完成状态
        tkinter.Label(frame, text = "位置完成状态：").\
            grid(row = 13, column = 3, sticky = tkinter.E)
        self.pfEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        # 禁止编辑
        self.pfEditor.bind("<KeyPress>", lambda f : "break")
        self.pfEditor.grid(row = 13, column = 4, sticky = tkinter.W)
        
        # 电机实时位置
        tkinter.Label(frame, text = "实时位置(脉冲数)：").\
            grid(row = 13, column = 5, sticky = tkinter.E)
        self.posEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.posEditor.bind("<KeyPress>", lambda f : "break")
        self.posEditor.grid(row = 13, column = 6, sticky = tkinter.W)
        
        # 剩余完成时间
        tkinter.Label(frame, text = "剩余时间(毫秒)：").\
            grid(row = 13, column = 7, sticky = tkinter.E)
        self.ltEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.ltEditor.bind("<KeyPress>", lambda f : "break")
        self.ltEditor.grid(row = 13, column = 8, sticky = tkinter.W)
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 14, column = 0, rowspan = 1, columnspan = 9, sticky = "EW", padx = 5, pady = 5)
            
        # 正常停止
        tkinter.Button(frame, \
            text = "正常停止", command = self.stopAction). \
                grid(row = 15, column = 0, sticky = tkinter.E)
        
        # 向前移动
        tkinter.Label(frame, text = "向前移动：").\
            grid(row = 15, column = 1, sticky = tkinter.E)
        self.forwardButton = tkinter.Button(frame, \
            text = "发送指令", command = self.forwardAction)
        self.forwardButton.grid(row = 15, column = 2, sticky = tkinter.W)
                
        # 向后移动
        tkinter.Label(frame, text = "向后移动：").\
            grid(row = 15, column = 3, sticky = tkinter.E)
        self.backwardButton = tkinter.Button(frame, \
            text = "发送指令", command = self.backwardAction)
        self.backwardButton.grid(row = 15, column = 4, sticky = tkinter.W)

        # 设置原点
        tkinter.Label(frame, text = "设置原点：").\
            grid(row = 15, column = 5, sticky = tkinter.E)
        self.backwardButton = tkinter.Button(frame, \
            text = "发送指令", command = self.originAction)
        self.backwardButton.grid(row = 15, column = 6, sticky = tkinter.W)
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 16, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)
            
        # Move
        tkinter.Button(frame, \
            text = "Move", command = self.moveAction). \
                grid(row = 17, column = 0, sticky = tkinter.E)
        
        # 目标位置
        tkinter.Label(frame, text = "相对位置(毫米)：").\
            grid(row = 17, column = 1, sticky = tkinter.E)
        self.pposEditor0 = tkinter.Text(frame, height = 1, width = 10)
        self.pposEditor0.grid(row = 17, column = 2, sticky = tkinter.W)
        self.pposEditor0.insert('insert', "200")
        
        # PWM占空比
        tkinter.Label(frame, text = "PWM占空比(%)：").\
            grid(row = 17, column = 3, sticky = tkinter.E)
        self.pwmEditor = tkinter.Text(frame, height = 1, width = 10)
        self.pwmEditor.grid(row = 17, column = 4, sticky = tkinter.W)
        self.pwmEditor.insert('insert', "20")
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 18, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)
            
        # MoveTo
        tkinter.Button(frame, \
            text = "MoveTo", command = self.moveToAction) \
                .grid(row = 19, column = 0, sticky = tkinter.E)
        
        # 目标位置
        tkinter.Label(frame, text = "相对位置(毫米)：").\
            grid(row = 19, column = 1, sticky = tkinter.E)
        self.pposEditor1 = tkinter.Text(frame, height = 1, width = 10)
        self.pposEditor1.grid(row = 19, column = 2, sticky = tkinter.W)
        self.pposEditor1.insert('insert', "200")
        
        # 目标位置
        tkinter.Label(frame, text = "换向频率(Hz)：").\
            grid(row = 19, column = 3, sticky = tkinter.E)
        self.freqEditor1 = tkinter.Text(frame, height = 1, width = 10)
        self.freqEditor1.grid(row = 19, column = 4, sticky = tkinter.W)
        self.freqEditor1.insert('insert', "100")
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 20, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)
            
        # Move
        tkinter.Button(frame, \
            text = "MoveAbs", command = self.moveAbsAction). \
                grid(row = 21, column = 0, sticky = tkinter.E)
        
        # 目标位置
        tkinter.Label(frame, text = "绝对位置(毫米)：").\
            grid(row = 21, column = 1, sticky = tkinter.E)
        self.apposEditor = tkinter.Text(frame, height = 1, width = 10)
        self.apposEditor.grid(row = 21, column = 2, sticky = tkinter.W)
        self.apposEditor.insert('insert', "2000")
        
        # PWM占空比
        tkinter.Label(frame, text = "PWM占空比(%)：").\
            grid(row = 21, column = 3, sticky = tkinter.E)
        self.apwmEditor = tkinter.Text(frame, height = 1, width = 10)
        self.apwmEditor.grid(row = 21, column = 4, sticky = tkinter.W)
        self.apwmEditor.insert('insert', "20")

        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 22, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)

    # 更新参数
    def configAction(self):
        try:
            # 检查设备
            if self.vehicle is not None:
                # 获得边距
                leave_count = int(self.bridgeEditor.get('0.0', 'end').strip())
                # 检查数据
                if leave_count <= 0 or leave_count > 1000:
                    # 提示窗口
                    messagebox.showinfo("无效数据", "边距数值不正确！")
                    return
                # 设置数值
                self.vehicle.leave_count = leave_count
                
                # 获得轨道总长
                rail_dist = int(self.railEditor.get('0.0', 'end').strip())
                # 检查数据
                if rail_dist <= 0 or rail_dist > 100000:
                    # 提示窗口
                    messagebox.showinfo("无效数据", "轨道总长不正确！")
                    return
                # 设置数值
                self.vehicle.rail_dist = rail_dist
                
                # 获得总脉冲数
                pulse_count = int(self.pulseEditor.get('0.0', 'end').strip())
                # 检查数据
                if pulse_count <= 0 or pulse_count > 300000:
                    # 提示窗口
                    messagebox.showinfo("无效数据", "总脉冲数不正确！")
                    return
                # 设置数值
                self.vehicle.pulse_count = pulse_count
                
                # 打印数据
                print("VehicleFrame.configAction : 最终配置结果！")
                print("\tleave_count = %d"% self.vehicle.leave_count)
                print("\trail_dist = %d"% self.vehicle.rail_dist)
                print("\tpulse_count = %d"% self.vehicle.pulse_count)

            else:
                # 提示信息
                messagebox.showerror("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("VehicleFrame.connAction :", str(e))
            print("VehicleFrame.connAction : unexpected exit !")

    # 连接设备
    def connAction(self):
        try:
            # 检查按钮名
            if self.vehicle is not None:
                # 删除设备
                del self.vehicle
                # 清空设备
                self.vehicle = None
                # 修改按钮名称
                self.connTxt.set("连接设备")
            else:                
                # 创建设备
                self.vehicle = Vehicle()
                # 初始化设备
                if self.vehicle.init_Vehicle():                    
                    # 获得端口配置
                    self.pnEditor4.delete('1.0', 'end')
                    self.pnEditor4.insert('insert', \
                        self.vehicle.config.get_port(4, "/dev/ttyUSB0"))
                    # 获得地址配置
                    self.addrEditor4.delete('1.0', 'end')
                    self.addrEditor4.insert('insert', \
                        str(self.vehicle.config.get_address(4, 0x05)))
                    # 获得端口配置
                    self.pnEditor2.delete('1.0', 'end')
                    self.pnEditor2.insert('insert', \
                        self.vehicle.config.get_port(2, "/dev/ttyUSB0"))
                    # 获得地址配置
                    self.addrEditor2.delete('1.0', 'end')
                    self.addrEditor2.insert('insert', \
                        str(self.vehicle.config.get_address(2, 0x01)))
                    # 获得端口配置
                    self.pnEditor3.delete('1.0', 'end')
                    self.pnEditor3.insert('insert', \
                        self.vehicle.config.get_port(3, "/dev/ttyUSB1"))
                    # 获得地址配置
                    self.addrEditor3.delete('1.0', 'end')
                    self.addrEditor3.insert('insert', \
                        str(self.vehicle.config.get_address(3, 0x01)))
                    # 获得端口配置
                    self.pnEditor1.delete('1.0', 'end')
                    self.pnEditor1.insert('insert', \
                        self.vehicle.config.get_port(1, "/dev/ttyUSB0"))
                    # 获得地址配置
                    self.addrEditor1.delete('1.0', 'end')
                    self.addrEditor1.insert('insert', \
                        self.vehicle.config.get_address(1, 0x03))
                    
                    # 边距
                    self.bridgeEditor.delete('1.0', 'end')
                    self.bridgeEditor.insert('insert', \
                        str(self.vehicle.leave_count))
                    
                    # 轨道总长
                    self.railEditor.delete('1.0', 'end')
                    self.railEditor.insert('insert', \
                        str(self.vehicle.rail_dist))

                    # 总脉冲数
                    self.pulseEditor.delete('1.0', 'end')
                    self.pulseEditor.insert('insert', \
                        str(self.vehicle.pulse_count))

                    # 删除所有文本
                    self.powerEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.powerEditor.insert('insert', self.vehicle.get_motor().power)
                    
                    # 删除所有文本
                    self.studyEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.studyEditor.insert('insert', str(self.vehicle.get_motor().study))
                    
                    # 删除所有文本
                    self.forwardEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.forwardEditor.insert('insert', str(self.vehicle.get_motor().forward))

                    # 删除所有文本
                    self.stEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.stEditor.insert('insert', str(self.vehicle.get_motor().skip_time))

                    # 删除所有文本
                    self.mpEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.mpEditor.insert('insert', str(self.vehicle.get_motor().duty_ratio))

                    # 删除所有文本
                    self.mfEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.mfEditor.insert('insert', str(self.vehicle.get_motor().reverse_freq))

                    # 调用函数
                    self.statusAction()
                    self.motorAction()
                    # 修改按钮名称
                    self.connTxt.set("断开设备")
                    # 提示窗口
                    messagebox.showinfo("提示信息", "设备已经连接！")
                else:
                    # 删除设备
                    del self.vehicle
                    # 清空设备
                    self.vehicle = None
                    # 提示窗口
                    messagebox.showerror("提示信息", "设备未能连接！")
        except Exception as e:
            traceback.print_exc()
            print("VehicleFrame.connAction :", str(e))
            print("VehicleFrame.connAction : unexpected exit !")

    # 读取状态
    def statusAction(self):
        try:
            # 检查按钮名
            if self.vehicle is not None:
                # 读取数据
                value = self.vehicle.get_abspos()
                # 删除所有文本
                self.meterEditor.delete('1.0', 'end')
                # 检查结果
                if value is not None:
                    # 插入现有文本
                    self.meterEditor.insert('insert', str(value * 1000.0))

                # 读取数据
                value = self.vehicle.get_weight()
                # 删除所有文本
                self.weightEditor.delete('1.0', 'end')
                # 检查结果
                if value is not None:
                    # 插入现有文本
                    self.weightEditor.insert('insert', str(value[1]))
                    
                # 读取电能表
                value = self.vehicle.get_power()
                # 检查结果
                if value >= 0:
                    # 插入现有文本
                    self.weightEditor.insert('insert', str(value))         
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")            
        except Exception as e:
            traceback.print_exc()
            print("VehicleFrame.statusAction :", str(e))
            print("VehicleFrame.statusAction : unexpected exit !")       

    # 读取状态
    def motorAction(self):
        try:
            # 检查按钮名
            if self.vehicle is not None:
                # 检查状态
                if not self.vehicle.get_motor().is_alive():
                    # 读取信息
                    if not self.vehicle.get_motor().read_status():
                        # 提示窗口
                        messagebox.showinfo("提示信息", "设备状态失败！")
                        return
                    
                # 删除所有文本
                self.tmpEditor.delete('1.0', 'end')
                # 插入现有文本
                self.tmpEditor.insert('insert', \
                    str(self.vehicle.get_motor().get_reg(0x0037) * 0.1))

                # 删除所有文本
                self.rcEditor.delete('1.0', 'end')
                # 插入现有文本
                self.rcEditor.insert('insert', \
                    str(self.vehicle.get_motor().get_reg(0x0021) * 0.01))

                # 删除所有文本
                self.blockedEditor.delete('1.0', 'end')
                # 插入现有文本
                self.blockedEditor.insert('insert', \
                    str(self.vehicle.get_motor().get_reg(0x0032)) + ":" + self.vehicle.get_motor().reg_info(0x0032))
                
                # 删除所有文本
                self.errorEditor.delete('1.0', 'end')
                # 插入现有文本
                self.errorEditor.insert('insert', \
                    str(self.vehicle.get_motor().get_reg(0x0033)) + ":" + self.vehicle.get_motor().reg_info(0x0033))
                
                # 删除所有文本
                self.pfEditor.delete('1.0', 'end')
                # 插入现有文本
                self.pfEditor.insert('insert', \
                    str(self.vehicle.get_motor().get_reg(0x0023)) + ":" + self.vehicle.get_motor().reg_info(0x0023))
                
                # 删除所有文本
                self.svEditor.delete('1.0', 'end')
                # 插入现有文本
                self.svEditor.insert('insert', \
                    str(self.vehicle.get_motor().get_reg(0x0038) * 0.1))
                
                # 删除所有文本
                self.posEditor.delete('1.0', 'end')
                # 插入现有文本
                self.posEditor.insert('insert', \
                    str(self.vehicle.get_motor().get_reg(0x0024)))

                # 删除所有文本
                self.ltEditor.delete('1.0', 'end')
                # 插入现有文本
                self.ltEditor.insert('insert', \
                    str(self.vehicle.get_motor().get_reg(0x0026)))
         
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")            
        except Exception as e:
            traceback.print_exc()
            print("VehicleFrame.statusAction :", str(e))
            print("VehicleFrame.statusAction : unexpected exit !")
            
    # 移动指令
    def moveAction(self):
        try:
            # 检查按钮名
            if self.vehicle is not None:
                # 获得占空比
                pwm = int(self.pwmEditor.get('0.0', 'end').strip())
                # 获得位置
                pos = int(self.pposEditor0.get('0.0', 'end').strip())                
                # 发送指令
                if self.vehicle.move(pos, pwm):
                    # 启动线程
                    self.vehicle.start_thread()
                    # 提示窗口
                    messagebox.showinfo("提示信息", "指令已发送！")
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "发送指令失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.moveAction :", str(e))
            print("MotorFrame.moveAction : unexpected exit !")

    # 移动指令
    def moveToAction(self):
        try:
            # 检查按钮名
            if self.vehicle is not None:
                # 获得位置
                pos = int(self.pposEditor1.get('0.0', 'end').strip())                
                # 获得频率
                freq = int(self.freqEditor1.get('0.0', 'end').strip())
                # 发送指令
                if self.vehicle.moveTo(pos, freq):
                    # 启动线程
                    self.vehicle.start_thread()
                    # 提示窗口
                    messagebox.showinfo("提示信息", "指令已发送！")
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "发送指令失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.moveToAction :", str(e))
            print("MotorFrame.moveToAction : unexpected exit !")

    # 向后移动
    def backwardAction(self):
        try:
            # 检查按钮名
            if self.vehicle is not None:
                # 发送指令
                if self.vehicle.move_backward():
                    # 启动线程
                    self.vehicle.start_thread()
                    # 提示窗口
                    messagebox.showinfo("提示信息", "指令已发送！")
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "发送指令失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("VehicleFrame.backwardAction :", str(e))
            print("VehicleFrame.backwardAction : unexpected exit !")

    # 向前移动
    def forwardAction(self):
        try:
            # 检查按钮名
            if self.vehicle is not None:
                # 发送指令
                if self.vehicle.move_forward():
                    # 启动线程
                    self.vehicle.start_thread()
                    # 提示窗口
                    messagebox.showinfo("提示信息", "指令已发送！")
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "发送指令失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("VehicleFrame.forwardAction :", str(e))
            print("VehicleFrame.forwardAction : unexpected exit !")

    # 正常停止
    def stopAction(self):
        try:
            # 检查按钮名
            if self.vehicle is not None:
                # 发送指令
                if self.vehicle.stop_motor():
                    # 停止线程
                    self.vehicle.stop_thread()
                    # 提示窗口
                    messagebox.showinfo("正常停止", "指令已发送！")
                else:
                    # 提示窗口
                    messagebox.showerror("正常停止", "指令发送失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("VehicleFrame.stopAction :", str(e))
            print("VehicleFrame.stopAction : unexpected exit !")
            
    # 设置原点
    def originAction(self):
        try:
            # 检查按钮名
            if self.vehicle is not None:
                # 发送指令
                if self.vehicle.set_origin():
                    # 提示窗口
                    messagebox.showinfo("设置原点", "指令已发送！")
                else:
                    # 提示窗口
                    messagebox.showerror("设置原点", "指令发送失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("VehicleFrame.originAction :", str(e))
            print("VehicleFrame.originAction : unexpected exit !")
            
    # 移动指令
    def moveAbsAction(self):
        try:
            # 检查按钮名
            if self.vehicle is not None:
                # 获得占空比
                pwm = int(self.apwmEditor.get('0.0', 'end').strip())
                # 获得位置
                pos = int(self.apposEditor.get('0.0', 'end').strip())
                # 发送指令
                if self.vehicle.moveAbs(pos, pwm):
                    # 启动线程
                    self.vehicle.start_thread()
                    # 提示窗口
                    messagebox.showinfo("提示信息", "指令已发送！")
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "发送指令失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.moveAbsAction :", str(e))
            print("MotorFrame.moveAbsAction : unexpected exit !")
