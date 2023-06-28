# 模块名称：test_recording
# 模块内容：基于appium的自动化测试，主要用于睿博士的卡录像功能
# 作者: 陈 熙
# -*- coding: utf-8 -*-
import os
import time
import shutil
import pytest
from imports import MobieProject, pytest, xrs_adb, getMp4Information, read_excel_to_dict, ntp_util
from imports import adb_download, serial_bitstream, image_properties, environment_variable


@pytest.fixture(scope="function")
def setup_environment():
    """初始化测试环境"""
    # 在这里进行测试环境的初始化操作
    try:
        project = MobieProject('睿博士')
        project.goto('个人管理页')
        # 判断设备是否使用18086409233账户登录
        if not project.is_element_exist('18086409233'):
            project.goto('登录页')
            project.goto('首页', '18086409233', 'cx123456')
        else:
            project.goto('首页', '18086409233', 'cx123456')

        # 检查设备是否离线、网络异常、不在线
        while project.is_element_exist('通讯异常') or project.is_element_exist('离线') or project.is_element_exist('连接中'):
            time.sleep(10)

        # 判断app是否启动
        if project.pwd() == '首页':
            return project
        else:
            setup_environment()

    except Exception as e:
        print(e)
        setup_environment()


def setup_module():
    print("初始化测试环境")
    serial_bitstream('COM36', '上电', 1)  # 设备上电
    os.system("adb shell settings put global adb_enabled 1")
    os.system("adb reboot")  # 重启手机
    time.sleep(60)
    xrs_adb.wakeUpScreen()  # 点亮屏幕
    os.system(xrs_adb.command_dict['滑屏解锁'])  # 解锁
    while not xrs_adb.check_device_connection():
        time.sleep(10)
    os.system("adb shell input tap 100 100")  # 取消提示弹窗


def pytest_sessionstart(session):
    """会话开始时执行一次，用于初始化测试环境"""
    print("初始化测试环境")
    serial_bitstream('COM36', '上电', 1)  # 设备上电
    os.system("adb shell settings put global adb_enabled 1")
    os.system("adb reboot")  # 重启手机
    time.sleep(60)
    xrs_adb.wakeUpScreen()  # 点亮屏幕
    os.system(xrs_adb.command_dict['滑屏解锁'])  # 解锁
    while not xrs_adb.check_device_connection():
        time.sleep(10)
    os.system("adb shell input tap 100 100")  # 取消提示弹窗


def pytest_sessionfinish(session, exitstatus):
    print("[pytest_sessionfinish] Finishing test session")

    # 执行一些全局的清理操作
    # ...