#!/usr/bin/python
# -*- coding: UTF-8 -*- 
from lib.common import redis_client
from lib.work_util import WorkerUtil
import threading
import time
from lib.log_util import getLogger

logger = getLogger('test case')

if __name__ == "__main__":

    def customer(task):
        print task, threading.current_thread().getName()
        time.sleep(1)

    def receiver():
        return redis_client.lpop('test')

    def is_shutdown():
        return redis_client.get('bye')

    # worker = WorkerUtil(customer_func=customer, customer_limit=3,
    #                     receiver_func=receiver, receiver_limit=1, shutdown_func=is_shutdown)
    # worker.start()
    def test():
        logger.debug('This is a debug message')
        logger.info('This is an info message')
        logger.warning('This is a warning message')
        logger.error('This is an error message')
        logger.critical('This is a critical message')
        try:
            a = 3/0
        except Exception as e:
            logger.exception('This is a exception message')
            pass
    test()

