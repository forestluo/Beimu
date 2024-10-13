# -*- coding: utf-8 -*

import tkinter
from tkinter import ttk
from tkinter import messagebox

from SD76C import *
from MainWindow import *
from WheelSensor import *
from VehicleConfig import *

class WheelFrame:
    # 窗口句柄
    __mainWindow = None

    def __init__(self, mainWindow, frame):
        # 设置缺省值
        self.device = None
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
        tkinter.Label(frame, text = "串口名称：").\
            grid(row = 0, column = 1, sticky = tkinter.E)
        self.pnEditor = tkinter.Text(frame, height = 1, width = 15)
        self.pnEditor.grid(row = 0, column = 2, sticky = tkinter.W)
        # 获得端口配置
        self.portName = self.__mainWindow.config.get_port(1, "/dev/ttyUSB0")
        self.pnEditor.insert('insert', self.portName)

        # 地址配置
        tkinter.Label(frame, text = "设备地址：").\
            grid(row = 0, column = 3, sticky = tkinter.E)
        self.addrEditor = tkinter.Text(frame, height = 1, width = 5)
        self.addrEditor.grid(row = 0, column = 4, sticky = tkinter.W)
        # 获得地址配置
        self.devAddress = self.__mainWindow.config.get_address(1, 0x03)
        self.addrEditor.insert('insert', str(self.devAddress))
                        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 1, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)

        # 信息按钮
        self.infoButton = tkinter.Button(frame, \
            text = "基本信息", command = self.infoAction)
        self.infoButton.grid(row = 2, column = 0, sticky = tkinter.E)

        # 工作模式
        tkinter.Label(frame, text = "工作模式：").\
            grid(row = 2, column = 1, sticky = tkinter.E)
        self.modeEditor = tkinter.Text(frame, height = 1, width = 15, bg = "lightgrey")
        self.modeEditor.bind("<KeyPress>", lambda f : "break")
        self.modeEditor.grid(row = 2, column = 2, sticky = tkinter.W)
        
        # 仪表暂停中
        tkinter.Label(frame, text = "仪表暂停中：").\
            grid(row = 2, column = 3, sticky = tkinter.E)
        self.pauseEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.pauseEditor.bind("<KeyPress>", lambda f : "break")
        self.pauseEditor.grid(row = 2, column = 4, sticky = tkinter.W)
        
        # AL1报警
        tkinter.Label(frame, text = "AL1报警：").\
            grid(row = 3, column = 1, sticky = tkinter.E)
        self.al1aEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.al1aEditor.bind("<KeyPress>", lambda f : "break")
        self.al1aEditor.grid(row = 3, column = 2, sticky = tkinter.W)

        # AL2报警
        tkinter.Label(frame, text = "AL2报警：").\
            grid(row = 3, column = 3, sticky = tkinter.E)
        self.al2aEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.al2aEditor.bind("<KeyPress>", lambda f : "break")
        self.al2aEditor.grid(row = 3, column = 4, sticky = tkinter.W)
        
        # AL1继电器闭合
        tkinter.Label(frame, text = "AL1继电器闭合：").\
            grid(row = 3, column = 5, sticky = tkinter.E)
        self.al1rEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.al1rEditor.bind("<KeyPress>", lambda f : "break")
        self.al1rEditor.grid(row = 3, column = 6, sticky = tkinter.W)
        
        # AL2继电器闭合
        tkinter.Label(frame, text = "AL2继电器闭合：").\
            grid(row = 3, column = 7, sticky = tkinter.E)
        self.al2rEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.al2rEditor.bind("<KeyPress>", lambda f : "break")
        self.al2rEditor.grid(row = 3, column = 8, sticky = tkinter.W)
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 4, column = 0, rowspan = 1, columnspan = 9, sticky = "EW", padx = 5, pady = 5)

        # 状态按钮
        self.statusButton = tkinter.Button(frame, \
            text = "读取状态", command = self.statusAction)
        self.statusButton.grid(row = 5, column = 0, sticky = tkinter.E)
        
        # 实际数值
        tkinter.Label(frame, text = "实际数值(米)：").\
            grid(row = 5, column = 1, sticky = tkinter.E)
        self.meterEditor = tkinter.Text(frame, height = 1, width = 10, bg = "yellow")
        self.meterEditor.bind("<KeyPress>", lambda f : "break")
        self.meterEditor.grid(row = 5, column = 2, sticky = tkinter.W)

        # 上排浮点值
        tkinter.Label(frame, text = "上排数码管浮点值：").\
            grid(row = 5, column = 3, sticky = tkinter.E)
        self.upfEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.upfEditor.bind("<KeyPress>", lambda f : "break")
        self.upfEditor.grid(row = 5, column = 4, sticky = tkinter.W)

        # 下排浮点值
        tkinter.Label(frame, text = "下排数码管浮点值：").\
            grid(row = 5, column = 5, sticky = tkinter.E)
        self.downfEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.downfEditor.bind("<KeyPress>", lambda f : "break")
        self.downfEditor.grid(row = 5, column = 6, sticky = tkinter.W)

        # 上排显示小数点
        tkinter.Label(frame, text = "上排显示小数点：").\
            grid(row = 6, column = 1, sticky = tkinter.E)
        self.uppEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.uppEditor.bind("<KeyPress>", lambda f : "break")
        self.uppEditor.grid(row = 6, column = 2, sticky = tkinter.W)

        # 下排显示小数点
        tkinter.Label(frame, text = "下排显示小数点：").\
            grid(row = 6, column = 3, sticky = tkinter.E)
        self.downpEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.downpEditor.bind("<KeyPress>", lambda f : "break")
        self.downpEditor.grid(row = 6, column = 4, sticky = tkinter.W)
        
        # 上排数码管整数值
        tkinter.Label(frame, text = "上排数码管整数值：").\
            grid(row = 6, column = 5, sticky = tkinter.E)
        self.upiEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.upiEditor.bind("<KeyPress>", lambda f : "break")
        self.upiEditor.grid(row = 6, column = 6, sticky = tkinter.W)

        # 下排数码管整数值
        tkinter.Label(frame, text = "下排数码管整数值：").\
            grid(row = 6, column = 7, sticky = tkinter.E)
        self.downiEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.downiEditor.bind("<KeyPress>", lambda f : "break")
        self.downiEditor.grid(row = 6, column = 8, sticky = tkinter.W)

        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 7, column = 0, rowspan = 1, columnspan = 9, sticky = "EW", padx = 5, pady = 5)

        # 状态按钮
        self.resetButton = tkinter.Button(frame, \
            text = "设置零点", command = self.resetAction)
        self.resetButton.grid(row = 8, column = 0, sticky = tkinter.E)

    # 读取状态
    def resetAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 执行指令
                if self.device.reset():
                    # 提示窗口
                    messagebox.showinfo("提示信息", "设置零点成功！")
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "设置零点失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("WheelFrame.resetAction :", str(e))
            print("WheelFrame.resetAction : unexpected exit !")

    # 读取状态
    def statusAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 发送指令
                value = self.device.get_pos()
                # 检查结果
                if value is not None:
                    # 删除所有文本
                    self.meterEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.meterEditor.insert('insert', str(value))

                    # 删除所有文本
                    self.upfEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.upfEditor.insert('insert', str(self.device.get_reg(0x0025)))

                    # 删除所有文本
                    self.downfEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.downfEditor.insert('insert', str(self.device.get_reg(0x0027)))
                    
                    # 删除所有文本
                    self.uppEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.uppEditor.insert('insert', str(self.device.get_reg(0x0020) & 0x0F))
                    
                    # 删除所有文本
                    self.downpEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.downpEditor.insert('insert', str((self.device.get_reg(0x0020) >> 8) & 0x0F))

                    # 删除所有文本
                    self.upiEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.upiEditor.insert('insert', str(self.device.get_reg(0x0021)))
                    
                    # 删除所有文本
                    self.downiEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.downiEditor.insert('insert', str(self.device.get_reg(0x0023)))

                else:
                    # 提示窗口
                    messagebox.showinfo("提示信息", "读取状态失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("WheelFrame.statusAction :", str(e))
            print("WheelFrame.statusAction : unexpected exit !")

    # 提取信息
    def infoAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 发送指令
                if self.device.read_status():
                    # 获得状态值
                    value = self.device.get_reg(0x0000)
                    # 获得工作模式
                    mode = SD76C.work_mode((value >> 8) & 0x0F)
                    # 删除所有文本
                    self.modeEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.modeEditor.insert('insert', hex((value >> 8) & 0x0F) + ":" + mode)
                    
                    # 获得报警值
                    value = value & 0x0F
                    # 检查结果
                    # 删除所有文本
                    self.pauseEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.pauseEditor.insert('insert', "是" if ((value & 0x10) != 0) else "否")
                    
                    # 删除所有文本
                    self.al1aEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.al1aEditor.insert('insert', "是" if ((value & 0x01) != 0) else "否")                           
                    
                    # 删除所有文本
                    self.al2aEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.al2aEditor.insert('insert', "是" if ((value & 0x02) != 0) else "否")                           

                    # 删除所有文本
                    self.al1rEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.al1rEditor.insert('insert', "是" if ((value & 0x04) != 0) else "否")                           

                    # 删除所有文本
                    self.al2rEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.al2rEditor.insert('insert', "是" if ((value & 0x08) != 0) else "否")                           
                else:
                    # 提示窗口
                    messagebox.showinfo("提示信息", "读取信息失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("WheelFrame.infoAction :", str(e))
            print("WheelFrame.infoAction : unexpected exit !")

    # 连接设备
    def connAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 删除设备
                del self.device
                # 清空设备
                self.device = None
                # 修改按钮名称
                self.connTxt.set("连接设备")            
            else:
                # 获得串口名
                portName = self.pnEditor.get('0.0', 'end').strip()
                # 获得设备地址
                devAddress = self.addrEditor.get('0.0', 'end').strip()
                # 创建设备
                self.device = WheelSensor(portName, int(devAddress))
                # 保留参数值
                self.portName = portName
                self.devAddress = int(devAddress)
                
                # 调用函数
                self.infoAction()
                self.statusAction()
                # 修改按钮名称
                self.connTxt.set("断开设备")
                # 提示窗口
                messagebox.showinfo("提示信息", "设备已经连接！")                

        except Exception as e:
            traceback.print_exc()
            print("WheelFrame.connAction :", str(e))
            print("WheelFrame.connAction : unexpected exit !")
