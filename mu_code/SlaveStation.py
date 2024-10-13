# -*- coding: utf-8 -*

from Modbus import Modbus

class SlaveStation(Modbus):
    # 控制寄存器列表
    __regs = {}
    # 从站地址
    address = 0x00
        
    def __init__(self, name, address):
        # 调用父对象初始化
        Modbus.__init__(self, name)    
        # 设置从站地址
        self.address = address
        # 检查设备名
        if address < 0 or address > 127:
            # 打印信息
            print("SlaveStation:__init__ : invalid address(%d) !"%address)
        return

    # 设置寄存器
    def __setregs__(self, regs):
        # 设置寄存器
        self.__regs = regs
        
    # 删除寄存器
    def __delitem__(self, index):
        # 删除寄存器
        del self.__regs[index]

    # 获得寄存器
    def __getitem__(self, index):
        # 返回寄存器数值
        return self.__regs[index]
        
    # 设置寄存器
    def __setitem__(self, index, register):
        # 设置寄存器数值
        self.__regs[index] = register 

    # 按名称查询对象
    def get_item(self, name):
        # 遍历字典
        for value in self.__regs.values():
            if name is value.name: return value

    def read_regs(self, start, count):
        # 调用父对象函数
        return super(SlaveStation, self).read_raw(self.address, start, count)
    
    def write_regs(self, start, buffer):
        # 调用父对象函数
        return super(SlaveStation, self).write_raw(self.address, start, buffer)

    # 打印所有寄存器
    # None 表明没有任何可用数据
    # 读写模式[寄存器16进制索引](中文名称) = 数值|单位 (注释)]
    def print_items(self):
        # 打印信息
        print("SlaveStation.print_items : begin !")
        # 遍历字典
        for value in self.__regs.values(): print("\t%s"%value)

    # 读取所有寄存器
    # 通过单个寄存器读取实现
    # 需要多次通讯过程，效率较低
    def read_items(self):
        # 打印信息
        print("SlaveStation.read_items : begin !")
        # 遍历字典
        for value in self.__regs.values():
            if not self.read_reg(value.ind): return False
            print("\t%s"%value)
        # 返回结果
        return True

    # 读取单个寄存器
    def read_reg(self, index):
        # 打印信息
        if (self.debug) : \
            print("SlaveStation.read_reg : begin !")
        # 检查模式
        if not self[index].readable:
            # 打印信息
            if (self.debug) : \
                print("SlaveStation.read_reg : not readable !")
            return True
        # 读取数据
        # 按字节计算长度
        buffer = self.read_regs(self[index].ind, self[index].len // 2)
        # 检查结果
        if buffer is None or len(buffer) != self[index].len:
            # 打印信息
            if (self.debug) : \
                print("SlaveStation.read_reg : fail to read !")
            return False
        # 解包
        if not self[index].unpack(buffer):
            # 打印信息
            if (self.debug) : \
                print("SlaveStation.read_reg : fail to unpack(R%04X) !"%index)
            return False
        #返回结果
        return True
    
    # 写入寄存器
    def write_reg(self, index, count = 1):
        # 打印信息
        if (self.debug) : \
            print("SlaveStation.write_reg : begin !")
        # 数据
        buffer = bytes()
        # 循环处理
        for i in range(index, index + count):
            # 打印数据
            if (self.debug) : \
                print("\t%s"%self[i])
            # 检查模式
            if not self[i].writable:
                # 打印信息
                if (self.debug) : \
                    print("SlaveStation.write_reg : not writable !")
                return False
            # 检查数据有效性
            if not self[i].valid:
                # 打印信息
                if (self.debug) : \
                    print("SlaveStation.write_reg : invalid value !")
                return False
            # 检查是否存在该key
            if i not in self.__regs:
                # 数据补0
                buffer += [0x00, 0x00]
                # 打印信息
                if (self.debug) : \
                    print("SlaveStation.write_reg : skip R[%04X] !"%i)
                continue
            # 打包
            output = self[i].pack()
            # 检查结果
            if output is None:
                # 打印信息
                if (self.debug) : \
                    print("SlaveStation.write_reg : fail to pack !")
                return False
            # 检查长度
            if len(output) != self[i].len:
                # 打印信息
                if (self.debug) : \
                    print("SlaveStation.write_reg : invalid buffer !")
                return False
            # 增加数据包长度
            buffer += output
        # 写入数据
        if not self.write_regs(index, buffer):
            # 打印信息
            if (self.debug) : \
                print("SlaveStation.write_reg : fail to write !")
            return False
        # 返回结果
        return True
