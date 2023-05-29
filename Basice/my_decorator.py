# -*- coding: utf-8 -*-
import functools
import xrs_time
import logging as log
import threading
import schedule
import time
import xrs_adb
from functools import wraps

log.basicConfig(filename=f'C:\\Users\\Administrator\\Desktop\\logs\\{xrs_time.today()}.log', level=log.INFO)
'''
1、运行花费时间，返回函数或方法的执行时间
2、打印函数的执行时的时间
3、打印函数的返回值
4、保存日志
'''
error_dict = {
    '未找到页面元素': 'selenium.common.exceptions.NoSuchElementException: Message: An element could not be located on the page using the given search parameters.',
    '': ''
}


def run_time(func):
    # 运行花费时间，打印函数或方法的执行时间
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print("运行时间：%0.6f秒" % (end_time - start_time))
        return func(*args)

    return wrapper


def print_current_time(func):
    # 打印函数的执行时间
    def wrapper(*args, **kwargs):
        print(xrs_time.get_current_time(), f"开始执行函数{func.__name__}")
        func(*args, **kwargs)

    return wrapper


def print_return(func):
    # 打印函数的返回值
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(res)

    return wrapper


def save_log(func):
    # 保存函数的返回值到日志，带时间戳
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        log.info('\t' + xrs_time.get_current_time() + '\n' + res)

    return wrapper


def thread_decorator(func):
    # 实现装饰器开启多线程
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


def timed_executor(t):
    def decorator(func):
        def run_threaded(func, *args, **kwargs):
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()
            return thread

        def wrapper(*args, **kwargs):
            schedule.clear()
            schedule.every().day.at(t).do(run_threaded, func, *args, **kwargs)
            while True:
                schedule.run_pending()

        return wrapper

    return decorator


def exception_handler(func):
    # 抛出异常后，再次执行
    def inner_function(*args, **kwargs):
        try:
            # print(f'kwargs{kwargs}')
            func(*args, **kwargs)
        except Exception as e:
            print(f"{xrs_time.get_current_time()}{func.__name__}\t{e}")
            time.sleep(30)
            func(*args, **kwargs)

    return inner_function


def retry(retries=2, delay=8):
    """
    装饰器：函数执行失败后会尝试多次重试

    :param retries: 重试次数，默认为3次
    :param delay: 重试延迟时间，单位为秒，默认为1秒

    使用示例：

    @retry(retries=5, delay=2)
    def my_function():
        # 进行一些操作
        pass

    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f'{func.__name__} failed with error: {str(e)}')
                    if i < retries - 1:
                        time.sleep(delay * (i + 1))  # 每次等待时间与异常次数成线性关系
                    else:
                        raise Exception(F"尝试{retries}次重新执行后，仍然运行异常！")
            return None

        return wrapper

    return decorator


def repeat(num_repeats):
    # 装饰器，用于多次执行，且含异常检查
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(num_repeats):
                print(f"{xrs_time.get_current_time()}\tRunning {i + 1}/{num_repeats}...")
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}")
                    try:
                        xrs_adb.start_app('com.zwcode.p6slite', '.activity.SplashActivity')
                        continue
                    except Exception as e:
                        print(f"Error: {e}")
                        xrs_adb.start_app('com.zwcode.p6slite', '.activity.SplashActivity')
                        continue
                time.sleep(1)

        return wrapper

    return decorator


if __name__ == '__main__':
    pass
