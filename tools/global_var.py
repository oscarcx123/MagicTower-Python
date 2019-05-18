# global_var 的作用是提供一个全局变量字典以供其它模块使用

def _init():
    global _global_dict
    _global_dict = {}
 
# 定义一个全局变量
def set_value(key,value):
    _global_dict[key] = value
 
# 获得一个全局变量,不存在则返回默认值
def get_value(key,defValue=None):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
