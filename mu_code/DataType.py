# -*- coding: utf-8 -*

from enum import Enum, unique

@unique
class DataType(Enum):
    # Null
    null = 0
    # Byte
    int8 = 1
    uint8 = 2
    hint8 = 3
    # Short
    int16 = 4
    uint16 = 5
    hint16 = 6
    # Integer
    int32 = 7
    uint32 = 8
    hint32 = 9
    # Float
    float32 = 10
    # Array
    array8 = 11
    # String
    string8 = 12
    
    # 有效性
    def is_valid(type):
        return type >= 0 and type <= 12
        
    # 检查是否为字节型
    def is_array(type):
        return type in \
        (DataType.array8, DataType.string8)

    # 检查是否有符号
    def is_signed(type):
        return type in \
        (DataType.int8, DataType.int16, DataType.int32)
                
    # 检查是否为8bits
    def is_8bits(type):
        return type in \
        (DataType.int8, DataType.uint8, DataType.hint8)

    # 检查是否为16bits
    def is_16bits(type):
        return type in \
        (DataType.int16, DataType.uint16, DataType.hint16)

    # 检查是否为32bits
    def is_32bits(type):
        return type in \
        (DataType.int32, DataType.uint32, DataType.hint32)
        
    # 检查是否为整数
    def is_integer(type):
        return type in \
        (DataType.int8, DataType.int16, DataType.int32, \
            DataType.uint8, DataType.uint16, DataType.uint32, \
                DataType.hint8, DataType.hint16, DataType.hint32)

    # 注释信息
    def info(type):
        if type == DataType.null: return "null"
        elif type == DataType.int8: return "int8"
        elif type == DataType.uint8: return "uint8"
        elif type == DataType.hint8: return "hint8"
        elif type == DataType.int16: return "int16"
        elif type == DataType.uint16: return "uint16"
        elif type == DataType.hint16: return "hint16"
        elif type == DataType.int32: return "int32"
        elif type == DataType.uint32: return "uint32"
        elif type == DataType.hint32: return "hint32"
        elif type == DataType.float32: return "float32"
        elif type == DataType.array8: return "array8"
        elif type == DataType.string8: return "string8"
        else: return "undefined"
