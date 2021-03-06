# encoding: utf-8
"""
@author: dawinia
@time: 2020/4/17 下午4:28
@file: debug.py
@desc: 
"""
import random
import re
import redis


def get_minute(time: str):
    """
    根据给定时间表达式（固定格式）返回分钟数
    :param time: 时间表达式，格式为 PTaHbM， a为小时数，b为分钟数
    :return: 返回分钟数
    """
    time_list = re.findall('\d+', time)
    time_num = len(time_list)
    ans = 0
    for t in time_list:
        ans += int(t) * (60 ** (time_num - 1))
        time_num -= 1
    return ans


print(get_minute('PT1H36M'))

con = redis.StrictRedis(host='localhost', port=6379, password='movie')


# con.set('hello', 'world')
# if not con.sadd('movieInfo', '27663743'):
#     print(f"existed -- {con.smembers('movieInfo')}")
# else:
#     print(f"success")

def test():
    def ty(name):
        for i in []:
            print(f"{name}: {i}")
            yield i

    # for i in range(1, 4):
    #     next(ty(i))
    for i in range(5):
        for j in ty(i):
            pass


test()


def tt():
    x = yield
    print('x=', x)
    yield


gen = tt()
gen.send(None)
gen.send(11)
print('--------')
gen.close()
