# -*- coding: utf-8 -*
import tkinter
from tkinter import ttk
from tkinter import messagebox

from MotorFrame import *
from WheelFrame import *
from EnergyFrame import *
from WeightFrame import *
from VehicleFrame import *

from VehicleConfig import *

class MainFrame:
    # 窗口句柄
    __mainWindow = None

    def __init__(self, mainWindow, root):
        # 设置窗口
        self.__mainWindow = mainWindow
        # 初始化菜单
        self.__initFrame(root)
        
    # 初始化标签窗口
    def __initFrame(self, root):
        # 生成Notebook
        notebook = ttk.Notebook(root)
        
        # 生成框架
        self.iniFrame = tkinter.Frame()
        self.wheelFrame = tkinter.Frame()
        self.motorFrame = tkinter.Frame()
        self.energyFrame = tkinter.Frame()
        self.weightFrame = tkinter.Frame()
        self.vehicleFrame = tkinter.Frame()
        
        # 加入框架
        notebook.add(self.iniFrame, text = "配置文件")
        notebook.add(self.motorFrame, text = "后桥驱动器")
        notebook.add(self.weightFrame, text = "称重传感器")
        notebook.add(self.wheelFrame, text = "计米器")
        notebook.add(self.energyFrame, text = "电能表")
        notebook.add(self.vehicleFrame, text = "自动上料车")
        
        # 初始化配置窗口
        self.__initIniFrame()
        # 初始化后桥电机窗口
        self.motorFrame = MotorFrame(self.__mainWindow, self.motorFrame)
        # 初始化计米器窗口
        self.wheelFrame = WheelFrame(self.__mainWindow, self.wheelFrame)
        # 初始化电能表窗口
        self.energyFrame = EnergyFrame(self.__mainWindow, self.energyFrame)
        # 初始化称重传感器窗口
        self.weightFrame = WeightFrame(self.__mainWindow, self.weightFrame)
        # 初始化自动上料车
        self.vehicleFrame = VehicleFrame(self.__mainWindow, self.vehicleFrame)

        # 打包
        notebook.pack(padx = 5, pady = 5, fill = tkinter.BOTH, expand = True)
        
    # 初始化配置窗口
    def __initIniFrame(self):
        # 生成配置文件编辑器
        self.iniText = tkinter.Text(self.iniFrame)

        # 检查配置文件是否存在
        if not self.__mainWindow.config.exists():
            # 信息提示
            messagebox.showinfo("配置文件","无法找到配置文件，将重新生成！")
            # 生成一个缺省文件
            self.__mainWindow.config.save_conf()
        # 加载配置文件
        self.__mainWindow.config.load_conf()
        # 打开文件
        with open(file = 'config.ini', mode = 'r+', encoding = 'utf-8') as file:
            fileText = file.read()
        # 插入到编辑器中
        self.iniText.insert('insert', fileText) 
        # 禁止编辑
        #iniText.config(state = tkinter.DISABLED)
        # 打包
        self.iniText.pack(padx = 5, pady = 5, fill = tkinter.BOTH, expand = True)
