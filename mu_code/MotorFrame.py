# -*- coding: utf-8 -*

import tkinter
from tkinter import ttk
from tkinter import messagebox

from threading import Thread

from MainWindow import *
from VehicleConfig import *
from MotorController import *

class MotorFrame:
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
        self.portName = self.__mainWindow.config.get_port(4, "/dev/ttyUSB0")
        self.pnEditor.insert('insert', self.portName)

        # 地址配置
        tkinter.Label(frame, text = "设备地址：").\
            grid(row = 0, column = 3, sticky = tkinter.E)
        self.addrEditor = tkinter.Text(frame, height = 1, width = 5)
        self.addrEditor.grid(row = 0, column = 4, sticky = tkinter.W)
        # 获得地址配置
        self.devAddress = self.__mainWindow.config.get_address(4, 0x05)
        self.addrEditor.insert('insert', str(self.devAddress))
                        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 1, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)
        
        # 信息按钮
        self.infoButton = tkinter.Button(frame, \
            text = "基本信息", command = self.infoAction)
        self.infoButton.grid(row = 2, column = 0, sticky = tkinter.E)

        # 设备标识
        tkinter.Label(frame, text = "设备标识：").\
            grid(row = 2, column = 1, sticky = tkinter.E)
        self.idEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.idEditor.bind("<KeyPress>", lambda f : "break")
        self.idEditor.grid(row = 2, column = 2, sticky = tkinter.W)

        # 设备版本号
        tkinter.Label(frame, text = "设备版本：").\
            grid(row = 2, column = 3, sticky = tkinter.E)
        self.verEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.verEditor.bind("<KeyPress>", lambda f : "break")
        self.verEditor.grid(row = 2, column = 4, sticky = tkinter.W)
        
        # 设备名称
        tkinter.Label(frame, text = "设备名称：").\
            grid(row = 2, column = 5, sticky = tkinter.E)
        self.nameEditor = tkinter.Text(frame, height = 1, width = 15, bg = "lightgrey")
        self.nameEditor.bind("<KeyPress>", lambda f : "break")
        self.nameEditor.grid(row = 2, column = 6, sticky = tkinter.W)        
        
        # PWM分辨率
        tkinter.Label(frame, text = "PWM分辨率：").\
            grid(row = 3, column = 1, sticky = tkinter.E)
        self.resEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.resEditor.bind("<KeyPress>", lambda f : "break")
        self.resEditor.grid(row = 3, column = 2, sticky = tkinter.W)
        
        # PWM频率
        tkinter.Label(frame, text = "PWM频率：").\
            grid(row = 3, column = 3, sticky = tkinter.E)
        self.freqEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.freqEditor.bind("<KeyPress>", lambda f : "break")
        self.freqEditor.grid(row = 3, column = 4, sticky = tkinter.W)
        
        # 最大输出电流
        tkinter.Label(frame, text = "最大输出电流：").\
            grid(row = 3, column = 5, sticky = tkinter.E)
        self.mcEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.mcEditor.bind("<KeyPress>", lambda f : "break")
        self.mcEditor.grid(row = 3, column = 6, sticky = tkinter.W)
        
        # 电流分辨率
        tkinter.Label(frame, text = "电流分辨率：").\
            grid(row = 3, column = 7, sticky = tkinter.E)
        self.cresEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.cresEditor.bind("<KeyPress>", lambda f : "break")
        self.cresEditor.grid(row = 3, column = 8, sticky = tkinter.W)
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 4, column = 0, rowspan = 1, columnspan = 9, sticky = "EW", padx = 5, pady = 5)
            
        # 配置按钮
        self.infoButton = tkinter.Button(frame, \
            text = "更新参数", command = self.configAction)
        self.infoButton.grid(row = 5, column = 0, sticky = tkinter.E)
        
        # 额定功率
        tkinter.Label(frame, text = "额定功率(W)：").\
            grid(row = 5, column = 1, sticky = tkinter.E)
        self.powerEditor = tkinter.Text(frame, height = 1, width = 10)
        self.powerEditor.grid(row = 5, column = 2, sticky = tkinter.W)
        
        # 学习状态
        tkinter.Label(frame, text = "学习状态：").\
            grid(row = 5, column = 3, sticky = tkinter.E)
        self.studyEditor = tkinter.Text(frame, height = 1, width = 10)
        self.studyEditor.grid(row = 5, column = 4, sticky = tkinter.W)

        # 前进标识
        tkinter.Label(frame, text = "前进标识：").\
            grid(row = 5, column = 5, sticky = tkinter.E)
        self.forwardEditor = tkinter.Text(frame, height = 1, width = 10)
        self.forwardEditor.grid(row = 5, column = 6, sticky = tkinter.W)

        # 超功率时长
        tkinter.Label(frame, text = "超功率时长(秒)：").\
            grid(row = 6, column = 1, sticky = tkinter.E)
        self.stEditor = tkinter.Text(frame, height = 1, width = 10)
        self.stEditor.grid(row = 6, column = 2, sticky = tkinter.W)

        # 最低占空比
        tkinter.Label(frame, text = "最低占空比(%)：").\
            grid(row = 6, column = 3, sticky = tkinter.E)
        self.mpEditor = tkinter.Text(frame, height = 1, width = 10)
        self.mpEditor.grid(row = 6, column = 4, sticky = tkinter.W)
        
        # 最低换向频率
        tkinter.Label(frame, text = "最低频率(Hz)：").\
            grid(row = 6, column = 5, sticky = tkinter.E)
        self.mfEditor = tkinter.Text(frame, height = 1, width = 10)
        self.mfEditor.grid(row = 6, column = 6, sticky = tkinter.W)

        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 7, column = 0, rowspan = 1, columnspan = 7, sticky = "EW", padx = 5, pady = 5)
            
        # 状态按钮
        self.statusButton = tkinter.Button(frame, \
            text = "读取状态", command = self.statusAction)
        self.statusButton.grid(row = 8, column = 0, sticky = tkinter.E)
        
        # 内部温度
        tkinter.Label(frame, text = "内部温度(°C)：").\
            grid(row = 8, column = 1, sticky = tkinter.E)
        self.tmpEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.tmpEditor.bind("<KeyPress>", lambda f : "break")
        self.tmpEditor.grid(row = 8, column = 2, sticky = tkinter.W)

        # 实时电流
        tkinter.Label(frame, text = "实时电流(A)：").\
            grid(row = 8, column = 3, sticky = tkinter.E)
        self.rcEditor = tkinter.Text(frame, height = 1, width = 10, bg = "yellow")
        self.rcEditor.bind("<KeyPress>", lambda f : "break")
        self.rcEditor.grid(row = 8, column = 4, sticky = tkinter.W)
        
        # 堵转状态
        tkinter.Label(frame, text = "堵转状态：").\
            grid(row = 8, column = 5, sticky = tkinter.E)
        self.blockedEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.blockedEditor.bind("<KeyPress>", lambda f : "break")
        self.blockedEditor.grid(row = 8, column = 6, sticky = tkinter.W)
    
        # 错误状态
        tkinter.Label(frame, text = "错误状态：").\
            grid(row = 8, column = 7, sticky = tkinter.E)
        self.errorEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.errorEditor.bind("<KeyPress>", lambda f : "break")
        self.errorEditor.grid(row = 8, column = 8, sticky = tkinter.W)
        
        # 电源电压
        tkinter.Label(frame, text = "电源电压(V)：").\
            grid(row = 9, column = 1, sticky = tkinter.E)
        self.svEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.svEditor.bind("<KeyPress>", lambda f : "break")
        self.svEditor.grid(row = 9, column = 2, sticky = tkinter.W)
        
        # 位置完成状态
        tkinter.Label(frame, text = "位置完成状态：").\
            grid(row = 9, column = 3, sticky = tkinter.E)
        self.pfEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        # 禁止编辑
        self.pfEditor.bind("<KeyPress>", lambda f : "break")
        self.pfEditor.grid(row = 9, column = 4, sticky = tkinter.W)
        
        # 电机实时位置
        tkinter.Label(frame, text = "实时位置(脉冲数)：").\
            grid(row = 9, column = 5, sticky = tkinter.E)
        self.posEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.posEditor.bind("<KeyPress>", lambda f : "break")
        self.posEditor.grid(row = 9, column = 6, sticky = tkinter.W)
        
        # 剩余完成时间
        tkinter.Label(frame, text = "剩余时间(毫秒)：").\
            grid(row = 9, column = 7, sticky = tkinter.E)
        self.ltEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.ltEditor.bind("<KeyPress>", lambda f : "break")
        self.ltEditor.grid(row = 9, column = 8, sticky = tkinter.W)
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 10, column = 0, rowspan = 1, columnspan = 9, sticky = "EW", padx = 5, pady = 5)
            
        # 正常停止
        tkinter.Button(frame, \
            text = "正常停止", command = self.stopAction0). \
                grid(row = 11, column = 0, sticky = tkinter.E)
        
        # 紧急停止
        tkinter.Label(frame, text = "紧急制动：").\
            grid(row = 11, column = 1, sticky = tkinter.E)
        tkinter.Button(frame, \
            text = "发送指令", command = self.stopAction1). \
                grid(row = 11, column = 2, sticky = tkinter.W)

        # 自由停止
        tkinter.Label(frame, text = "自由停止：").\
            grid(row = 11, column = 3, sticky = tkinter.E)
        tkinter.Button(frame, \
            text = "发送指令", command = self.stopAction2). \
                grid(row = 11, column = 4, sticky = tkinter.W)

        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 12, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)
            
        # Move
        tkinter.Button(frame, \
            text = "Move", command = self.moveAction). \
                grid(row = 13, column = 0, sticky = tkinter.E)
        
        # 目标位置
        tkinter.Label(frame, text = "目标位置(脉冲数)：").\
            grid(row = 13, column = 1, sticky = tkinter.E)
        self.pposEditor0 = tkinter.Text(frame, height = 1, width = 10)
        self.pposEditor0.grid(row = 13, column = 2, sticky = tkinter.W)
        self.pposEditor0.insert('insert', "200")
        
        # PWM占空比
        tkinter.Label(frame, text = "PWM占空比(%)：").\
            grid(row = 13, column = 3, sticky = tkinter.E)
        self.pwmEditor = tkinter.Text(frame, height = 1, width = 10)
        self.pwmEditor.grid(row = 13, column = 4, sticky = tkinter.W)
        self.pwmEditor.insert('insert', "20")
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 14, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)
            
        # MoveTo
        self.pmButton = tkinter.Button(frame, \
            text = "MoveTo", command = self.moveToAction)
        self.pmButton.grid(row = 15, column = 0, sticky = tkinter.E)
        
        # 目标位置
        tkinter.Label(frame, text = "目标位置(脉冲数)：").\
            grid(row = 15, column = 1, sticky = tkinter.E)
        self.pposEditor1 = tkinter.Text(frame, height = 1, width = 10)
        self.pposEditor1.grid(row = 15, column = 2, sticky = tkinter.W)
        self.pposEditor1.insert('insert', "200")
        
        # 目标位置
        tkinter.Label(frame, text = "换向频率(Hz)：").\
            grid(row = 15, column = 3, sticky = tkinter.E)
        self.freqEditor1 = tkinter.Text(frame, height = 1, width = 10)
        self.freqEditor1.grid(row = 15, column = 4, sticky = tkinter.W)
        self.freqEditor1.insert('insert', "100")
        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 16, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)
            
        # 学习线序
        tkinter.Button(frame, \
            text = "学习线序", command = self.studyAction). \
                grid(row = 17, column = 0, sticky = tkinter.E)
                
        # 清零位置
        tkinter.Label(frame, text = "清零位置：").\
            grid(row = 17, column = 1, sticky = tkinter.E)
        tkinter.Button(frame, \
            text = "发送指令", command = self.clearAction). \
                grid(row = 17, column = 2, sticky = tkinter.W)

        # 向前移动
        tkinter.Label(frame, text = "向前移动：").\
            grid(row = 17, column = 3, sticky = tkinter.E)
        self.forwardButton = tkinter.Button(frame, \
            text = "发送指令", command = self.forwardAction)
        self.forwardButton.grid(row = 17, column = 4, sticky = tkinter.W)
                
        # 向后移动
        tkinter.Label(frame, text = "向后移动：").\
            grid(row = 17, column = 5, sticky = tkinter.E)
        self.backwardButton = tkinter.Button(frame, \
            text = "发送指令", command = self.backwardAction)
        self.backwardButton.grid(row = 17, column = 6, sticky = tkinter.W)

    # 移动指令
    def moveAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 获得占空比
                pwm = int(self.pwmEditor.get('0.0', 'end').strip())
                # 获得位置
                pos = int(self.pposEditor0.get('0.0', 'end').strip())                
                # 发送指令
                if self.device.move(pos, pwm):
                    # 启动线程
                    self.device.start_thread()
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
            if self.device is not None:
                # 获得位置
                pos = int(self.pposEditor1.get('0.0', 'end').strip())                
                # 获得频率
                freq = int(self.freqEditor1.get('0.0', 'end').strip())
                # 发送指令
                if self.device.moveTo(pos, freq):
                    # 启动线程
                    self.device.start_thread()
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
            if self.device is not None:
                # 发送指令
                if self.device.move_backward():
                    # 启动线程
                    self.device.start_thread()
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
            print("MotorFrame.backwardAction :", str(e))
            print("MotorFrame.backwardAction : unexpected exit !")

    # 向前移动
    def forwardAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 发送指令
                if self.device.move_forward():
                    # 启动线程
                    self.device.start_thread()
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
            print("MotorFrame.forwardAction :", str(e))
            print("MotorFrame.forwardAction : unexpected exit !")
        
    # 清零位置
    def clearAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 发送指令
                if self.device.clear_pos():
                    # 提示窗口
                    messagebox.showinfo("清理位置", "清理位置成功！")
                else:
                    # 提示窗口
                    messagebox.showerror("清理位置", "清理位置失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.clearAction :", str(e))
            print("MotorFrame.clearAction : unexpected exit !")

    # 电机学习
    def studyAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 检查配置
                if self.device.study: 
                    # 提示窗口
                    messagebox.showinfo("电机学习", "电机已经学习！")
                    return
                # 发送指令
                if self.device.init_device(True):
                    # 提示窗口
                    messagebox.showinfo("电机学习", "电机学习成功！")
                    # 设置参数值
                    self.device.study = True
                    # 删除所有文本
                    self.studyEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.studyEditor.insert('insert', str(self.device.study))
                else:
                    # 提示窗口
                    messagebox.showerror("电机学习", "电机学习失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.studyAction :", str(e))
            print("MotorFrame.studyAction : unexpected exit !")

    # 正常停止
    def stopAction0(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 发送指令
                if self.device.stop_motor(0):
                    # 停止线程
                    self.device.stop_thread()
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
            print("MotorFrame.stopAction0 :", str(e))
            print("MotorFrame.stopAction0 : unexpected exit !")

    # 紧急停止
    def stopAction1(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 发送指令
                if self.device.stop_motor(1):
                    # 停止线程
                    self.device.stop_thread()
                    # 提示窗口
                    messagebox.showinfo("紧急停止", "指令已发送！")
                else:
                    # 提示窗口
                    messagebox.showerror("紧急停止", "指令发送失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.stopAction1 :", str(e))
            print("MotorFrame.stopAction1 : unexpected exit !")

    # 自由停止
    def stopAction2(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 发送指令
                if self.device.stop_motor(2):
                    # 停止线程
                    self.device.stop_thread()
                    # 提示窗口
                    messagebox.showinfo("自由停止", "指令已发送！")
                else:
                    # 提示窗口
                    messagebox.showerror("自由停止", "指令发送失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.stopAction2 :", str(e))
            print("MotorFrame.stopAction2 : unexpected exit !")

    # 连接设备
    def connAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 停止线程
                self.device.stop_thread()
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
                self.device = MotorController(portName, int(devAddress))                
                # 保留参数值
                self.portName = portName
                self.devAddress = int(devAddress)
                
                # 删除所有文本
                self.powerEditor.delete('1.0', 'end')
                # 插入现有文本
                self.powerEditor.insert('insert', self.device.power)
                
                # 删除所有文本
                self.studyEditor.delete('1.0', 'end')
                # 插入现有文本
                self.studyEditor.insert('insert', str(self.device.study))
                
                # 删除所有文本
                self.forwardEditor.delete('1.0', 'end')
                # 插入现有文本
                self.forwardEditor.insert('insert', str(self.device.forward))

                # 删除所有文本
                self.stEditor.delete('1.0', 'end')
                # 插入现有文本
                self.stEditor.insert('insert', str(self.device.skip_time))

                # 删除所有文本
                self.mpEditor.delete('1.0', 'end')
                # 插入现有文本
                self.mpEditor.insert('insert', str(self.device.duty_ratio))

                # 删除所有文本
                self.mfEditor.delete('1.0', 'end')
                # 插入现有文本
                self.mfEditor.insert('insert', str(self.device.reverse_freq))
                
                self.infoAction()
                self.statusAction()
                # 修改按钮名称
                self.connTxt.set("断开设备")
                # 提示窗口
                messagebox.showinfo("提示信息", "设备已经连接！")

        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.connAction :", str(e))
            print("MotorFrame.connAction : unexpected exit !")

    # 读取信息
    def infoAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 读取信息
                if self.device.read_info():
                    # 信息
                    # 删除所有文本
                    self.idEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.idEditor.insert('insert', \
                        hex(self.device.get_reg(0x0000)))
        
                    # 删除所有文本
                    self.verEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.verEditor.insert('insert', \
                        hex(self.device.get_reg(0x0001)))
                            
                    # 删除所有文本
                    self.nameEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.nameEditor.insert('insert', \
                        str(self.device.get_reg(0x0002)))
        
                    # 删除所有文本
                    self.resEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.resEditor.insert('insert', \
                        "1/" + str(self.device.get_reg(0x000A)))
                            
                    # 删除所有文本
                    self.freqEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.freqEditor.insert('insert', \
                        str(self.device.get_reg(0x000B)) + "Hz")
        
                    # 删除所有文本
                    self.mcEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.mcEditor.insert('insert', \
                        str(self.device.get_reg(0x000C) * 0.01) + "A")
                                                
                    # 删除所有文本
                    self.cresEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.cresEditor.insert('insert', \
                        str(self.device.get_reg(0x000C) / 1000) + "A")
                else:
                    # 提示窗口
                    messagebox.showinfo("提示信息", "读取信息失败！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.infoAction :", str(e))
            print("MotorFrame.infoAction : unexpected exit !")
            
    # 更新参数
    def configAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 获得额定功率
                power = int(self.powerEditor.get('0.0', 'end').strip())
                # 检查数据
                if power <= 0 or power >= 5000:
                    # 提示窗口
                    messagebox.showinfo("无效数据", "功率设置不正确！")
                    return
                # 设置数值
                self.device.power = power
                
                # 获得学习状态
                self.device.study = self.studyEditor.\
                    get('0.0', 'end').strip().lower() in ("yes", "true", "t", "1")
                
                # 获得前进指示
                forward = int(self.forwardEditor.get('0.0', 'end').strip())
                # 检查数据
                if forward == 0:
                    # 提示窗口
                    messagebox.showinfo("无效数据", "前进标识设置不正确！")
                    return
                # 设置数值
                self.device.forward = 1 if forward > 0 else -1
                
                # 获得超功率时长
                skip_time = float(self.stEditor.get('0.0', 'end').strip())
                # 检查数据
                if skip_time <= 0 or skip_time > 10:
                    # 提示窗口
                    messagebox.showinfo("无效数据", "超功率时长不正确！")
                    return
                # 设置数值
                self.device.skip_time = skip_time
                
                # 获得最低占空比
                duty_ratio = int(self.mpEditor.get('0.0', 'end').strip())
                # 检查数值
                if duty_ratio <= 0 or duty_ratio > 100:
                    # 提示窗口
                    messagebox.showinfo("无效数据", "最低占空比设置不正确")
                    return
                # 设置数值
                self.device.duty_ratio = duty_ratio
                
                # 获得最低换向频率
                reverse_freq = int(self.mfEditor.get('0.0', 'end').strip())
                # 检查数值
                if reverse_freq <= 0 or reverse_freq > 100:
                    # 提示窗口
                    messagebox.showinfo("无效数据", "最低换向频率设置不正确")
                    return
                # 设置数值
                self.device.reverse_freq = reverse_freq
                
                # 打印数据
                print("MotorFrame.configAction : 最终配置结果！")
                print("\tpower = %dW"% self.device.power)
                print("\tstudy = %s"% str(self.device.study))
                print("\tforward = %d"% self.device.forward)
                print("\tskip_time = %.2f秒"% self.device.skip_time)
                print("\tduty_ratio = %d%%"% self.device.duty_ratio)
                print("\treverse_freq = %dHz"% self.device.reverse_freq)
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")            
        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.configAction :", str(e))
            print("MotorFrame.configAction : unexpected exit !")
            
    # 读取状态
    def statusAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 检查活动状态
                if not self.device.is_alive():
                    # 读取活动状态
                    if not self.device.read_status():
                        # 提示窗口
                        messagebox.showerror("提示信息", "读取设备状态失败！")
                        return

                # 删除所有文本
                self.tmpEditor.delete('1.0', 'end')
                # 插入现有文本
                self.tmpEditor.insert('insert', \
                    str(self.device.get_reg(0x0037) * 0.1))

                # 删除所有文本
                self.rcEditor.delete('1.0', 'end')
                # 插入现有文本
                self.rcEditor.insert('insert', \
                    str(self.device.get_reg(0x0021) * 0.01))

                # 删除所有文本
                self.blockedEditor.delete('1.0', 'end')
                # 插入现有文本
                self.blockedEditor.insert('insert', \
                    str(self.device.get_reg(0x0032)) + ":" + self.device.reg_info(0x0032))
                
                # 删除所有文本
                self.errorEditor.delete('1.0', 'end')
                # 插入现有文本
                self.errorEditor.insert('insert', \
                    str(self.device.get_reg(0x0033)) + ":" + self.device.reg_info(0x0033))
                
                # 删除所有文本
                self.pfEditor.delete('1.0', 'end')
                # 插入现有文本
                self.pfEditor.insert('insert', \
                    str(self.device.get_reg(0x0023)) + ":" + self.device.reg_info(0x0023))
                
                # 删除所有文本
                self.svEditor.delete('1.0', 'end')
                # 插入现有文本
                self.svEditor.insert('insert', \
                    str(self.device.get_reg(0x0038) * 0.1))
                
                # 删除所有文本
                self.posEditor.delete('1.0', 'end')
                # 插入现有文本
                self.posEditor.insert('insert', \
                    str(self.device.get_reg(0x0024)))

                # 删除所有文本
                self.ltEditor.delete('1.0', 'end')
                # 插入现有文本
                self.ltEditor.insert('insert', \
                    str(self.device.get_reg(0x0026)))
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")            
        except Exception as e:
            traceback.print_exc()
            print("MotorFrame.statusAction :", str(e))
            print("MotorFrame.statusAction : unexpected exit !")       