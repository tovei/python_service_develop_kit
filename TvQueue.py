#!/usr/bin/python
import Queue
import threading
import time
import redis
from inspect import isfunction


class TvQueue(object):

    def __init__(self, subscriber_func, consumer_func, consumer_num):
        if not isfunction(subscriber_func):
            raise Exception('subscriber_func is not a function')
        if not isfunction(consumer_func):
            raise Exception('consumer_func is not a function')
        if not isinstance(consumer_num, (int,)) or consumer_num <= 0:
            raise Exception('consumer_num is invalid')
        self.subscriber_func = subscriber_func
        self.consumer_func = consumer_func
        self.consumer_num = consumer_num
        self.consumer_threadings = []
        self.queue = Queue.Queue()

        while True:
            task = self.subscriber_func()
            if task:
                self.queue.put(task)
            time.sleep(0.1)

        def _consumer_func(run_func):
            while True:
                if not self.queue.empty():
                    task = self.queue.pop()
                    run_func(task)

        for i in range(consumer_num):
            self.consumer_threadings.append(threading.Thread(
                target=_consumer_func, args=(self.consumer_func,)))

    def start():
        for consumer in self.consumer_threadings:
            consumer.start()


redis_client = redis.Redis(host='localhost', port=6379, db=0)


def subscriber():
    task = redis_client.lpop('test')
    if task:
        return task
    return None


def consumer(task):
    print task


queue = TvQueue(
    subscriber_func=subscriber,
    consumer_func=consumer,
    consumer_num=4)
queue.start()

for i in range(5):
    redis_client.lpush('task'+str(i))
