# -*- coding: utf-8 -*

import traceback

import tkinter

from MainMenu import *
from MainFrame import *
from VehicleConfig import *

class MainWindow:    
    # 窗口句柄
    __root = None
    
    def __init__(self):
        # 设置窗口
        # 主动选择屏幕名
        self.__root = tkinter.Tk(screenName = ':0')
        self.__root.title("设备操作测试工具")
        # 初始化全屏模式
        self.__initFullScreen()
        #print("MainWindow.__init__ : 初始化全屏模式！")
        
        # 初始化配置模块
        self.config = VehicleConfig()
        # 初始化菜单
        self.mainMenu = MainMenu(self, self.__root)
        # 初始化视图
        self.mainFrame = MainFrame(self, self.__root)
        
    # 执行主循环
    def mainloop(self):
        # 执行循环
        self.__root.mainloop()
        
    # 退出窗口
    def exit_window(self):
        # 销毁窗口
        self.__root.destroy()
        # 检查设备
        if self.mainFrame.motorFrame.device is not None:
            # 停止设备
            self.mainFrame.motorFrame.device.stop_motor()
            # 停止线程
            self.mainFrame.motorFrame.device.stop_thread()
        # 检查设备
        if self.mainFrame.vehicleFrame.vehicle is not None:
            # 停止设备
            self.mainFrame.vehicleFrame.vehicle.stop_motor()
            # 停止线程
            self.mainFrame.vehicleFrame.vehicle.stop_thread()
            
    # 初始化全屏模式
    def __initFullScreen(self):
        # 设置一个全屏窗口
        self.__root.attributes('-fullscreen', True)
        self.fullScreenState = False
        self.__root.bind("<F11>", self.toggleFullScreen)
        self.__root.bind("<Escape>", self.quitFullScreen)
        # 获得屏幕大小
        self.screen_width = self.__root.winfo_screenwidth()
        self.screen_height = self.__root.winfo_screenheight()

    # 切换全屏状态
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.__root.attributes("-fullscreen", self.fullScreenState)
        
    # 关闭全屏状态
    def quitFullScreen(self, event):
        self.__fullScreenState = False
        self.__root.attributes("-fullscreen", self.__fullScreenState)
        
    # 设置配置文件
    def loadConfigFile(self, fileName):
        # 读取配置文件
        self.config.load_conf(fileName)
        # 打开文件
        with open(file = fileName, mode = 'r+', encoding = 'utf-8') as file:
            fileText = file.read()
        # 删除所有文本
        self.mainFrame.iniText.delete('1.0', 'end')
        # 插入现有文本
        self.mainFrame.iniText.insert('insert', fileText)
        
    # 保存配置文件
    def saveConfigFile(self, fileName):
        # 获得文本内容
        fileText = self.mainFrame.iniText.get('0.0', 'end')
        # 检查结果
        if fileText is None or len(fileText) <= 0:
            # 提示窗口
            messagebox.showinfo("无效内容", "不符合要求的文件内容！")
            return
        # 保存配置文件
        with open(fileName, "w", encoding = "utf-8") as file:
            file.write(fileText)
        # 重新加载配置文件
        self.config.load_conf(fileName)
        
# 定义主函数
def main():

    # 创建控制器
    myWindow = MainWindow()

    # 执行主循环
    myWindow.mainloop()

    # 删除控制器
    del myWindow

if __name__ == '__main__':
    try:
        # 调用主函数
        main()
    except Exception as e:
        traceback.print_exc()
        print("MotorController.__main__ :", str(e))
        print("MotorController.__main__ : unexpected exit !")