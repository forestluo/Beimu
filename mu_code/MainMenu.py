# -*- coding: utf-8 -*

import serial
import serial.tools
import serial.tools.list_ports

import binascii

from crcmod import mkCrcFun

import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

class MainMenu:
    # 窗口句柄
    __mainWindow = None
    
    def __init__(self, mainWindow, root):
        # 设置窗口
        self.__mainWindow = mainWindow
        # 初始化菜单
        self.__initMenu(root)
        
    # 初始化菜单
    def __initMenu(self, root):
        # 主菜单
        self.topMenu = tkinter.Menu(root)
        # 增加菜单项目
        
        # 增加文件菜单
        fileMenu = tkinter.Menu(self.topMenu)
        self.topMenu.add_cascade(label = "文件", menu = fileMenu)
        fileMenu.add_command(label = "打开", \
            command = self.openConfigFile, accelerator = 'Ctrl+N')
        fileMenu.add_command(label = "保存", \
            command = self.saveConfigFile, accelerator = 'Ctrl+S')
        fileMenu.add_separator()
        fileMenu.add_command(label = "退出", \
            command = self.__mainWindow.exit_window, accelerator = 'Ctrl+Alt')
        
        # 增加工具菜单
        toolMenu = tkinter.Menu(self.topMenu)
        self.topMenu.add_cascade(label = "工具", menu = toolMenu)
        toolMenu.add_command(label = "列举串口", \
            command = self.listPorts, accelerator = 'Ctrl+L')
        toolMenu.add_separator()
        toolMenu.add_command(label = "CRC16工具", \
            command = self.crc16Tool)
        toolMenu.add_command(label = "Modbus工具")
        
        # 配置菜单
        root.config(menu = self.topMenu)
        
    # 打开配置文件
    def openConfigFile(self):
        # 打开文件
        fileName = filedialog.askopenfilename\
            (title = "打开配置文件", \
                defaultextension = ".ini", \
                filetypes=[("INI", ".ini"), ("TXT", ".txt")])
        # 打印信息
        if fileName is None or len(fileName) <= 0:
            print("MainMenu.openConfigFile : no file choosed !")
            return
        # 打印文件名
        print("MainMenu.openConfigFile : %s"% fileName)
        # 设置文本
        self.__mainWindow.loadConfigFile(fileName)
        
    # 保存配置文件
    def saveConfigFile(self):
        # 打开文件
        fileName = filedialog.asksaveasfilename\
            (title = "保存配置文件", \
                defaultextension = ".ini", \
                filetypes=[("INI", ".ini"), ("TXT", ".txt")])
        # 打印信息
        if fileName is None or len(fileName) <= 0:
            print("MainMenu.saveConfigFile : no file specified !")
            return
        # 打印文件名
        print("MainMenu.saveConfigFile : %s"% fileName)
        # 保存配置文件
        self.__mainWindow.saveConfigFile(fileName)

    # 显示所有串口名称
    def listPorts(self):
        # 列举设备
        portList = \
            list(serial.tools.list_ports.comports())
        # 检查结果
        if len(portList) <= 0:
            # 提示窗口
            messagebox.showinfo("列举串口", "没有找到串口！")
            return
        
        # 信息
        portsInfo = ""
        # 循环
        for i in range(0, len(portList)):
            # 增加名称
            portsInfo += str(portList[i]) + "\n"
        # 提示窗口
        messagebox.showinfo("列举串口", portsInfo)
            
    # CRC16计算工具
    def crc16Tool(self):
        # 开启一个对话框
        input = simpledialog.askstring(title = 'CRC16工具', \
            prompt = '请输入16进制字符串：', initialvalue = '0123456789ABCDEF')
        # 检查结果
        if input is None or len(input) <= 0:
            # 提示窗口
            messagebox.showinfo("无效信息", "输入值不符合要求！")
            return
        # 打印信息
        print("MainWindow.crc16Tool : %s" % input)
        # 转binary
        result = binascii.unhexlify(input)
        # 计算CRC16结果
        crc16 = mkCrcFun(0x18005, rev = True,
                initCrc = 0xFFFF, xorOut = 0x0000)
        result = crc16(result)
        # 提示窗口
        messagebox.showinfo("CRC16结果", "mkCrcFun(%s) = %s " % (input, hex(result)))   
