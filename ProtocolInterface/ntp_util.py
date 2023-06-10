import time

import ntplib
from time import strftime, gmtime, mktime, strptime

def get_ntp_time(ntp_server):
    """
    获取NTP服务器的当前时间

    :param ntp_server: NTP服务器地址
    :return: 当前时间（时间戳形式）
    """
    try:
        client = ntplib.NTPClient()
        response = client.request(ntp_server)
        return response.tx_time
    except:
        return None


def get_ntp_timestamp(ntp_server="pool.ntp.org", int_val=None):
    """
    获取NTP服务器的当前时间，返回格式为时间戳

    :param int_val: 标记结果是否取整
    :param ntp_server: NTP服务器地址
    :return: 当前时间（时间戳形式）
    """
    ntp_time = get_ntp_time(ntp_server)
    for i in range(3):
        if ntp_time:
            if int_val is None:
                return int(ntp_time)
            else:
                return ntp_time
        else:
            time.sleep(3)
            ntp_time = get_ntp_time(ntp_server)


def get_formatted_ntp_time(ntp_server):
    """
    获取NTP服务器的当前时间，返回格式化后的日期字符串

    :param ntp_server: NTP服务器地址
    :return: 当前时间的格式化字符串
    """
    ntp_time = get_ntp_time(ntp_server)
    if ntp_time:
        dt = gmtime(ntp_time)  # 转换为UTC时间
        return strftime("%Y-%m-%d %H:%M:%S", dt)  # 格式化输出
    else:
        return None


def str_time_to_timestamp(time_str, format="%Y-%m-%d %H:%M:%S"):
    """
    将时间字符串转换为时间戳形式

    :param time_str: 时间字符串
    :param format: 时间字符串的格式，默认为 "%Y-%m-%d %H:%M:%S"
    :return: 时间戳
    """
    time_tuple = strptime(time_str, format)
    return mktime(time_tuple)


if __name__ == "__main__":

    print(str_time_to_timestamp('2023-06-09 15:11:59'),len('2023-06-09 15:11:59'))
