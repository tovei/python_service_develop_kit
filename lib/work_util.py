#!/usr/bin/python
# encoding: utf-8
import Queue
import threading
import time
from log_util import getLogger

logger = getLogger('公共任务处理类@')

# 公共任务处理类
class WorkerUtil(object):

    def __init__(self, customer_func, customer_limit, receiver_func, receiver_limit, shutdown_func = None):
        """
        入参校验
        """
        if not callable(customer_func):
            raise TypeError('customer func must be function')

        if not isinstance(customer_limit, (int,)) or customer_limit < 1:
            raise TypeError('customer limit is not valid')

        if not callable(receiver_func):
            raise TypeError('receiver func must be function')

        if not isinstance(receiver_limit, (int,)) or receiver_limit < 1:
            raise TypeError('receiver limit is not valid')

        if shutdown_func is not None and not callable(shutdown_func):
            raise TypeError('shutdown func must be function')

        """
        类变量初始化
        """
        # 消费者方法
        self.customer_func = customer_func
        # 消费者数量
        self.customer_limit = customer_limit
        # 接受者方法
        self.receiver_func = receiver_func
        # 接受者数量
        self.receiver_limit = receiver_limit
        # 关闭任务方法
        self.shutdown_func = shutdown_func

        # 任务队列 -- 任务临时中转站
        self.task_queue = Queue.Queue(maxsize=customer_limit)
        # 线程计数器 -- 防止内存激增
        self.semaphore = threading.Semaphore(customer_limit)

    def is_shutdown(self):
        """
        是否关闭服务
        """
        if callable(self.shutdown_func):
            return self.shutdown_func()
    
        return False

    def start(self):
        """
        启动服务
        """
        print 'service start',threading.current_thread().getName()
        def receiver_wraper():
            """
            接受者任务容器
            """
            while True:
                if self.is_shutdown():
                    break

                time.sleep(0.1)

                if not self.semaphore.acquire(blocking=False):
                    continue

                task = self.receiver_func()
                if task:
                    self.task_queue.put(task)
                else:
                    self.semaphore.release()

                

        def customer_wraper():
            """
            消费者任务容器
            """
            while True:
                if self.is_shutdown():
                    break

                time.sleep(0.1)

                if self.task_queue.empty():
                    continue

                task = self.task_queue.get()

                self.customer_func(task)

                self.semaphore.release()

        # 接受者初始化
        threads = []
        for i in range(self.receiver_limit):
            t = threading.Thread(target=receiver_wraper)
            threads.append(t)

        # 消费者初始化
        for i in range(self.customer_limit):
            t = threading.Thread(target=customer_wraper)
            threads.append(t)
            
        for t in threads:
            t.start()

        for t in threads:
            t.join()
        

