# -*- coding: utf-8 -*

import tkinter
from tkinter import ttk
from tkinter import messagebox

from MainWindow import *
from EnergySensor import *
from VehicleConfig import *

class EnergyFrame:
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
        self.portName = self.__mainWindow.config.get_port(2, "/dev/ttyUSB0")
        self.pnEditor.insert('insert', self.portName)

        # 地址配置
        tkinter.Label(frame, text = "设备地址：").\
            grid(row = 0, column = 3, sticky = tkinter.E)
        self.addrEditor = tkinter.Text(frame, height = 1, width = 5)
        self.addrEditor.grid(row = 0, column = 4, sticky = tkinter.W)
        # 获得地址配置
        self.devAddress = self.__mainWindow.config.get_address(2, 0x01)
        self.addrEditor.insert('insert', str(self.devAddress))
                        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 1, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)
            
        # 信息按钮
        self.infoButton = tkinter.Button(frame, \
            text = "基本信息", command = self.infoAction)
        self.infoButton.grid(row = 2, column = 0, sticky = tkinter.E)
        
        # 编程密码
        tkinter.Label(frame, text = "编程密码：").\
            grid(row = 2, column = 1, sticky = tkinter.E)
        self.pwdEditor = tkinter.Text(frame, height = 1, width = 15, bg = "lightgrey")
        self.pwdEditor.bind("<KeyPress>", lambda f : "break")
        self.pwdEditor.grid(row = 2, column = 2, sticky = tkinter.W)

        # 软件版本
        tkinter.Label(frame, text = "软件版本：").\
            grid(row = 2, column = 3, sticky = tkinter.E)
        self.verEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.verEditor.bind("<KeyPress>", lambda f : "break")
        self.verEditor.grid(row = 2, column = 4, sticky = tkinter.W)
        
        # 设备地址
        tkinter.Label(frame, text = "设备地址：").\
            grid(row = 2, column = 5, sticky = tkinter.E)
        self.daddrEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.daddrEditor.bind("<KeyPress>", lambda f : "break")
        self.daddrEditor.grid(row = 2, column = 6, sticky = tkinter.W)
        
        # 波特率
        tkinter.Label(frame, text = "波特率：").\
            grid(row = 2, column = 7, sticky = tkinter.E)
        self.baudEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.baudEditor.bind("<KeyPress>", lambda f : "break")
        self.baudEditor.grid(row = 2, column = 8, sticky = tkinter.W)
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 3, column = 0, rowspan = 1, columnspan = 9, sticky = "EW", padx = 5, pady = 5)
            
        # 信息按钮
        self.statusButton = tkinter.Button(frame, \
            text = "状态信息", command = self.statusAction)
        self.statusButton.grid(row = 4, column = 0, sticky = tkinter.E)

        # 有功总电能
        tkinter.Label(frame, text = "有功总电能(KWH)：").\
            grid(row = 4, column = 1, sticky = tkinter.E)
        self.epEditor = tkinter.Text(frame, height = 1, width = 15, bg = "yellow")
        self.epEditor.bind("<KeyPress>", lambda f : "break")
        self.epEditor.grid(row = 4, column = 2, sticky = tkinter.W)

        # A相电压
        tkinter.Label(frame, text = "A相电压(V)：").\
            grid(row = 4, column = 3, sticky = tkinter.E)
        self.vEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.vEditor.bind("<KeyPress>", lambda f : "break")
        self.vEditor.grid(row = 4, column = 4, sticky = tkinter.W)

        # A相电流
        tkinter.Label(frame, text = "A相电流(A)：").\
            grid(row = 4, column = 5, sticky = tkinter.E)
        self.iEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.iEditor.bind("<KeyPress>", lambda f : "break")
        self.iEditor.grid(row = 4, column = 6, sticky = tkinter.W)
        
        # 电网频率
        tkinter.Label(frame, text = "电网频率(Hz)：").\
            grid(row = 4, column = 7, sticky = tkinter.E)
        self.freqEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.freqEditor.bind("<KeyPress>", lambda f : "break")
        self.freqEditor.grid(row = 4, column = 8, sticky = tkinter.W)
        
        # 总功率因素
        tkinter.Label(frame, text = "总功率因素：").\
            grid(row = 5, column = 1, sticky = tkinter.E)
        self.pfEditor = tkinter.Text(frame, height = 1, width = 15, bg = "lightgrey")
        self.pfEditor.bind("<KeyPress>", lambda f : "break")
        self.pfEditor.grid(row = 5, column = 2, sticky = tkinter.W)
        
        # 瞬时总有功功率
        tkinter.Label(frame, text = "瞬时总有功功率：").\
            grid(row = 5, column = 3, sticky = tkinter.E)
        self.pEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.pEditor.bind("<KeyPress>", lambda f : "break")
        self.pEditor.grid(row = 5, column = 4, sticky = tkinter.W)
        
        # 瞬时总无功功率 
        tkinter.Label(frame, text = "瞬时总无功功率：").\
            grid(row = 5, column = 5, sticky = tkinter.E)
        self.qEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.qEditor.bind("<KeyPress>", lambda f : "break")
        self.qEditor.grid(row = 5, column = 6, sticky = tkinter.W)
        
        # 瞬时总视在功率 
        tkinter.Label(frame, text = "瞬时总视在功率：").\
            grid(row = 5, column = 7, sticky = tkinter.E)
        self.sEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.sEditor.bind("<KeyPress>", lambda f : "break")
        self.sEditor.grid(row = 5, column = 8, sticky = tkinter.W)
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 6, column = 0, rowspan = 1, columnspan = 9, sticky = "EW", padx = 5, pady = 5)
            
        # 状态按钮
        self.resetButton = tkinter.Button(frame, \
            text = "电能清零", command = self.resetAction)
        self.resetButton.grid(row = 7, column = 0, sticky = tkinter.E)
        
    # 读取状态
    def resetAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 清零电能计数
                if self.device.clear_power():
                    # 提示窗口
                    messagebox.showinfo("提示信息", "计数已清零！")
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "无法清零计数！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("EnergyFrame.resetAction :", str(e))
            print("EnergyFrame.resetAction : unexpected exit !")
            
    # 读取状态
    def statusAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 读取电能值
                power = self.device.get_power()
                # 检查结果
                if power > 0:
                    # 删除所有文本
                    self.epEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.epEditor.insert('insert', str(power))
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "无法读取状态！")
                    return
                
                # 读取状态
                if self.device.read_status():
                    # 删除所有文本
                    self.vEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.vEditor.insert('insert', \
                        str(self.device.get_reg(0x2000)))

                    # 删除所有文本
                    self.iEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.iEditor.insert('insert', \
                        str(self.device.get_reg(0x2002)))

                    # 删除所有文本
                    self.pEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.pEditor.insert('insert', \
                        str(self.device.get_reg(0x2004)))

                    # 删除所有文本
                    self.qEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.qEditor.insert('insert', \
                        str(self.device.get_reg(0x2006)))

                    # 删除所有文本
                    self.sEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.sEditor.insert('insert', \
                        str(self.device.get_reg(0x2008)))

                    # 删除所有文本
                    self.pfEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.pfEditor.insert('insert', \
                        str(self.device.get_reg(0x200A)))

                    # 删除所有文本
                    self.freqEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.freqEditor.insert('insert', \
                        str(self.device.get_reg(0x200E)))
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "无法读取状态！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("EnergyFrame.statusAction :", str(e))
            print("EnergyFrame.statusAction : unexpected exit !")

    # 提取信息
    def infoAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 读取信息
                if self.device.read_info():
                    # 信息
                    # 删除所有文本
                    self.pwdEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.pwdEditor.insert('insert', \
                        hex(self.device.get_reg(0x0000)))
                    
                    # 删除所有文本
                    self.verEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.verEditor.insert('insert', \
                        hex(self.device.get_reg(0x0001)))
                    
                    # 删除所有文本
                    self.daddrEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.daddrEditor.insert('insert', \
                        str(self.device.get_reg(0x0006)))

                    # 删除所有文本
                    self.baudEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.baudEditor.insert('insert', \
                        str(self.device.reg_info(0x000C)))
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "无法读取设备信息！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("EnergyFrame.infoAction :", str(e))
            print("EnergyFrame.infoAction : unexpected exit !")

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
                self.device = EnergySensor(portName, int(devAddress))
                # 修改按钮名称
                self.connTxt.set("断开设备")
                # 保留参数值
                self.portName = portName
                self.devAddress = int(devAddress)
                
        except Exception as e:
            traceback.print_exc()
            print("EnergyFrame.connAction :", str(e))
            print("EnergyFrame.connAction : unexpected exit !")
