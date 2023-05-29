import os
import time
import shutil
import xrs_app
from xrs_serial import serial_bitstream
from xrs_mediainfo import getMp4Information
from xrs_app import MobieProject
from xrs_log import log_info
import xrs_adb
from environment_variable import adb_download

'''
1、离线/在线状态更新时间
2、直播每种画质码率
3、直播每种画质帧率
'''


def live_preview():
    obj = MobieProject('睿博士')
    obj.goto('首页')
    if obj.is_element_exist('设备离线啦', times=3, wait=5):
        log_info('设备离线啦')
    else:
        obj.goto('直播页面')
        if obj.is_element_exist('设备离线啦', times=60,wait=0.5):
            log_info('设备连接失败')


def offline_status_update_time():
    # 离线状态刷新时间
    com = 'com36'
    serial_bitstream(com, '上电', 60)
    obj = MobieProject('睿博士')
    obj.goto('首页')
    start_time = time.time()
    serial_bitstream(com, '断电', 1)
    while True:
        if obj.is_element_exist('设备离线啦', times=1, wait=0.5):
            end_time = time.time()
            break
    print(f'离线状态自动刷新时间：{int(end_time - start_time)}秒')


def online_status_update_time():
    # 在线状态刷新时间
    com = 'com36'
    serial_bitstream(com, '断电', 120)
    obj = MobieProject('睿博士')
    obj.goto('首页')
    start_time = time.time()
    serial_bitstream(com, '上电', 1)
    while True:
        if obj.is_element_exist('在线', times=1, wait=0.5):
            end_time = time.time()
            break
    print(f'在线状态自动刷新时间：{int(end_time - start_time)}秒')



def live_video_recording(definition):
    xrs_app.WAITTIME = 8
    obj = MobieProject('睿博士')
    time.sleep(10)
    obj.goto('直播页面')
    obj.clickControl('画质', 'text')
    obj.clickControl(definition, 'text')
    os.system(xrs_adb.command_dict['清空睿博士录像'])
    obj.clickControl('录像', 'text')
    time.sleep(10)
    obj.clickControl('录像', 'text')
    dir = adb_download + 'videos\\'
    shutil.rmtree(dir)
    os.system(xrs_adb.command_dict['下载睿博士录像'])
    fileName = os.listdir(dir)[0]
    print(fileName)
    arguments = getMp4Information(dir + fileName)
    print(arguments)
    return arguments


if __name__ == '__main__':
    # offline_status_update_time()  # 离线状态更新时间
    # online_status_update_time()   # 在线状态更新时间

    live_video_recording('超清')
