# 模块名称：appium_autotest_test
# 模块内容：基于appium的自动化测试
# -*- coding: utf-8 -*-
import time, os, shutil
import random

from imports import MobieProject, pytest, xrs_adb, getMp4Information, read_excel_to_dict, ntp_util
from imports import adb_download, serial_bitstream, image_properties, environment_variable


def setup_module():
    print("初始化测试环境")
    serial_bitstream('COM36', '上电', 1)  # 设备上电
    os.system("adb shell settings put global adb_enabled 1")
    os.system("adb reboot")  # 重启手机
    time.sleep(45)
    xrs_adb.wakeUpScreen()  # 点亮屏幕
    os.system(xrs_adb.command_dict['滑屏解锁'])  # 解锁
    time.sleep(3)
    os.system("adb shell input tap 100 100")  # 取消提示弹窗


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


# @pytest.mark.parametrize()
@pytest.mark.run(order=1)
@pytest.mark.resolution_switch
@pytest.mark.loadtest
@pytest.mark.repeat(1)
@pytest.mark.flaky(reruns=5, reruns_delay=1)
def test_resolution_switch(setup_environment: MobieProject):
    # 模拟分辨率切换并检查系统是否正确适应
    project = setup_environment
    project.goto('直播页')
    project.clickControl('画质', 'text')
    modes = ['标清', '超清', '高清']
    for i in range(20):
        random.shuffle(modes)
        print(modes)
        for resolution in ['标清', '超清', '高清']:
            project.clickControl(resolution, 'text', wait=1)
    project.driver.quit()
