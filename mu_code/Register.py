# -*- coding: utf-8 -*

import struct

from DataType import *

class Register:
    # 数值
    __value = None

    # 读写属性
    __mode = "RW"
    # 索引
    __ind = -1
    # 长度
    __len = 0
    # 名称
    __name = None   
    # 类型
    __type = DataType.null
   
    # 定义构造函数
    def __init__(self, ind, name, type, len = 0):
        self.__ind = ind
        self.__len = len
        self.__name = name
        self.__type = type
        # 检查长度
        assert(self.__len >= 0 and self.__len % 2 == 0)
        # 检查类型，并设置长度
        if type == DataType.float32: self.__len = 4
        elif DataType.is_16bits(type): self.__len = 2
        elif DataType.is_32bits(type): self.__len = 4
        elif DataType.is_array(type): assert(self.__len >= 2)
        
    # 索引
    @property
    def ind(self):
        return self.__ind
    
    # 长度
    @property
    def len(self):
        return self.__len

    # 类型
    @property
    def type(self):
        return self.__type
    
    # 名称
    @property
    def name(self):
        return self.__name

    # 检查合理性
    @property
    def valid(self):
        return True
    
    # 注释信息
    @property
    def info(self):
        return "未定义" \
            if self.get() is None \
            else DataType.info(self.type)

    # 设置模式
    def mode(self, value):
        self.__mode = value

    # 可读
    @property
    def readable(self):
        return self.__mode == "R" or self.__mode == "RW"
    
    # 可写
    @property
    def writable(self):
        return self.__mode == "W" or self.__mode == "RW"
               
    # 获得数值
    def get(self):
        # 检查模式
        '''
        if self.__mode == "W":
            print("[0x%04X].get : write only !"%self.__ind)
            return None
        '''
        # 返回缺省值
        return self.__value
    
    # 设置数值
    def set(self, value):
        # 检查模式
        if self.__mode == "R":
            print("[0x%04X].set : read only !"%self.__ind)
            return False
        # 设置数值
        self.__value = value
        # 检查结果
        if self.valid: return True
        # 打印信息
        print("[0x%04X].set : invalid value(%d) !"%(self.__ind, value))
        return False

    # 打包
    def pack(self):
        # 检查数据
        if self.__value is None:
            # 打印信息
            print("Register.pack : value is None")
            return None
        # 检查类型
        if self.__type == DataType.float32:
            # 转换成浮点数
            return struct.pack("!f", self.__value)
        elif DataType.is_array(self.__type):
            # 字符串
            if self.__type == DataType.string8:
                # 转换成字符串
                return str.encode(self.__value)
            # 返回数据值
            return self.__value
        # 检查类型
        elif DataType.is_8bits(self.__type):
            # 返回结果
            return struct.pack("!B", int(self.__value) & 0xFF)
        # 检查类型
        elif DataType.is_16bits(self.__type):
            # 返回结果
            return struct.pack("!H", int(self.__value) & 0xFFFF)
        # 检查类型
        elif DataType.is_32bits(self.__type):
            # 返回结果
            return struct.pack("!I", int(self.__value) & 0xFFFFFFFF)
        else:
            # 打印信息
            print("Register.unpack : invalid type(%d) !"%self.__type)
        return None
        
    # 解析
    def unpack(self, buffer):
        # 确保长度
        assert(len(buffer) == self.__len)
        # 检查类型
        if self.__type == DataType.float32:
            # 转换成浮点数
            self.__value = struct.unpack("!f", buffer)[0]
        elif DataType.is_array(self.__type):
            # 按照字符串处理
            self.__value = buffer
            # 字符串
            if self.__type == DataType.string8:
                # 转换成字符串
                self.__value = bytes.decode(buffer)
        # 检查类型
        elif DataType.is_16bits(self.__type):
            # 短整数
            self.__value = struct.unpack("!H", buffer)[0]
            # 根据符号调整
            if DataType.is_signed(self.__type):
                if (self.__value & 0x8000) != 0: self.__value -= 0x10000
        # 检查类型
        elif DataType.is_32bits(self.__type):
            # 整数
            self.__value = struct.unpack("!I", buffer)[0]
            # 根据符号调整
            if DataType.is_signed(self.__type):
                if (self.__value & 0x80000000) != 0: self.__value -= 0x100000000
        else:
            # 打印信息
            print("Register.unpack : invalid type(%d) !"%self.__type)
            return False
        return True
       
    # 字符化
    def __str__(self):
        return self.__format__()
    
    # 格式化
    def __format__(self):
        # 检查数值
        if self.__value is None:
            # 返回缺省格式化
            return self.__mode + \
                    "[{:04X}]({:s}) = None". \
                    format(self.__ind, self.__name)
        # 检查类型
        if self.__type == DataType.string8:
            return self.__mode + \
                "[{:04X}]({:s}) = \"{:s}\" ({:s})". \
                format(self.__ind, self.__name, self.__value, self.info)
        if self.__type == DataType.float32:
            return self.__mode + \
                "[{:04X}]({:s}) = {:f} ({:s})". \
                format(self.__ind, self.__name, self.__value, self.info)
        if self.__type == DataType.array8:
            return self.__mode + \
                "[{:04X}]({:s}) = 0x{:s} ({:s})". \
                format(self.__ind, self.__name, self.__value.hex(), self.info)
        # 检查类型
        if DataType.is_16bits(self.__type):
            if self.__type == DataType.hint16:
                return self.__mode + \
                    "[{:04X}]({:s}) = 0x{:04x} ({:s})". \
                    format(self.__ind, self.__name, self.__value, self.info)
            return self.__mode + \
                "[{:04X}]({:s}) = {:d} ({:s})". \
                format(self.__ind, self.__name, self.__value, self.info)
        # 检查类型
        if DataType.is_32bits(self.__type):
            if self.__type == DataType.hint32:
                return self.__mode + \
                    "[{:04X}]({:s}) = 0x{:08x} ({:s})". \
                    format(self.__ind, self.__name, self.__value, self.info)
            return self.__mode + \
                "[{:04X}]({:s}) = {:d} ({:s})". \
                format(self.__ind, self.__name, self.__value, self.info)     
        # 打印信息
        print("Register.unpack : invalid type(%d) !"%self.__type)
        return None
