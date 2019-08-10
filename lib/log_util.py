import logging

logging.basicConfig(level = logging..DEBUG,format = '[%(asctime)s][%(name)s][%(threadName)s][%(funcName)s][%(levelname)s] - %(message)s')

"""
日志处理
"""


def getLogger(name=None):
    """
    初始化日志
    """
    return logging.getLogger(__name__ if name is None else name)