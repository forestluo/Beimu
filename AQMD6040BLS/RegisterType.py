# -*- coding: utf-8 -*

from enum import Enum, unique

@unique
class RegisterType(Enum):
    # None
    Unknown = 0
    # Short
    Short = 1
    HexShort = 2
    UnsignedShort = 3
    # Integer
    Integer = 4
    HexInteger = 5
    UnsignedInteger = 6
    # Float
    Float = 7
    # Bytes
    Bytes = 8
    # String
    String = 9
    
    # 有效性
    def is_valid(type):
        return type >= 0 and type <= 9        
        
    # 检查是否有符号
    def is_signed(type):
        return type == RegisterType.Short \
                or \
                type == RegisterType.Integer
                
    # 检查是否为字节型
    def is_bytes(type):
        return type == RegisterType.Float \
                or \
                type == RegisterType.Bytes \
                or \
                type == RegisterType.String

    # 检查是否为短整型
    def is_short(type):
        return type == RegisterType.Short \
                or \
                type == RegisterType.HexShort \
                or \
                type == RegisterType.UnsignedShort

    # 检查是否为整型
    def is_integer(type):
        return type == RegisterType.Integer \
                or \
                type == RegisterType.HexInteger \
                or \
                type == RegisterType.UnsignedInteger

    # 注释信息
    def info(type):
        if type == RegisterType.Unknown: return "None"
        
        elif type == RegisterType.Float: return "Float"
        elif type == RegisterType.Bytes: return "Bytes"
        elif type == RegisterType.String: return "String"
        
        elif type == RegisterType.Short: return "Short"
        elif type == RegisterType.HexShort: return "Hex Short"
        elif type == RegisterType.UnsignedShort: return "Unsigned Short"
        
        elif type == RegisterType.Integer: return "Integer"
        elif type == RegisterType.HexInteger: return "Hex Integer"
        elif type == RegisterType.UnsignedInteger: return "Unsigned Integer"
        else: return "Unknown"
