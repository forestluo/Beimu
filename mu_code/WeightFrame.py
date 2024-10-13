import tkinter
from tkinter import ttk
from tkinter import messagebox

from MainWindow import *
from WeightSensor import *
from VehicleConfig import *

class WeightFrame:
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
        self.portName = self.__mainWindow.config.get_port(3, "/dev/ttyUSB1")
        self.pnEditor.insert('insert', self.portName)

        # 地址配置
        tkinter.Label(frame, text = "设备地址：").\
            grid(row = 0, column = 3, sticky = tkinter.E)
        self.addrEditor = tkinter.Text(frame, height = 1, width = 5)
        self.addrEditor.grid(row = 0, column = 4, sticky = tkinter.W)
        # 获得地址配置
        self.devAddress = self.__mainWindow.config.get_address(3, 0x01)
        self.addrEditor.insert('insert', str(self.devAddress))
                        
        # 分隔符
        ttk.Separator(frame, orient = "horizontal").\
            grid(row = 1, column = 0, rowspan = 1, columnspan = 5, sticky = "EW", padx = 5, pady = 5)

        # 信息按钮
        self.infoButton = tkinter.Button(frame, \
            text = "读取数据", command = self.infoAction)
        self.infoButton.grid(row = 2, column = 0, sticky = tkinter.E)
        
        # 称重数据
        tkinter.Label(frame, text = "称重数值(公斤)：").\
            grid(row = 2, column = 1, sticky = tkinter.E)
        self.valueEditor = tkinter.Text(frame, height = 1, width = 15, bg = "yellow")
        self.valueEditor.bind("<KeyPress>", lambda f : "break")
        self.valueEditor.grid(row = 2, column = 2, sticky = tkinter.W)

        # 数据状态
        tkinter.Label(frame, text = "数据状态：").\
            grid(row = 2, column = 3, sticky = tkinter.E)
        self.statusEditor = tkinter.Text(frame, height = 1, width = 10, bg = "lightgrey")
        self.statusEditor.bind("<KeyPress>", lambda f : "break")
        self.statusEditor.grid(row = 2, column = 4, sticky = tkinter.W)

    # 提取信息
    def infoAction(self):
        try:
            # 检查按钮名
            if self.device is not None:
                # 读取信息
                result = self.device.get_weight()
                # 检查结果
                if result is not None :
                    # 信息
                    # 删除所有文本
                    self.valueEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.valueEditor.insert('insert', str(result[1]))
                    
                    # 删除所有文本
                    self.statusEditor.delete('1.0', 'end')
                    # 插入现有文本
                    self.statusEditor.insert('insert', str(result[0]))
                else:
                    # 提示窗口
                    messagebox.showerror("提示信息", "无法读取设备信息！")
            else:
                # 提示窗口
                messagebox.showinfo("提示信息", "设备尚未连接！")
        except Exception as e:
            traceback.print_exc()
            print("WeightFrame.infoAction :", str(e))
            print("WeightFrame.infoAction : unexpected exit !")

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
                self.device = WeightSensor(portName, int(devAddress))
                # 修改按钮名称
                self.connTxt.set("断开设备")
                # 保留参数值
                self.portName = portName
                self.devAddress = int(devAddress)
                
        except Exception as e:
            traceback.print_exc()
            print("WeightFrame.connAction :", str(e))
            print("WeightFrame.connAction : unexpected exit !")
