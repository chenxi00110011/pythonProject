# 模块名称：appium_autotest_test
# 模块内容：基于appium的自动化测试
# -*- coding: utf-8 -*-
import time, os, shutil
from imports import MobieProject, pytest, xrs_adb, getMp4Information, read_excel_to_dict, ntp_util
from imports import adb_download, serial_bitstream, image_properties, environment_variable

"""
优化：
1、将邻接表和元素表合并，增加wait字段，用于控制该操作的等待时间
2、写一个定时任务的装饰器，或者使用批处理实现
"""


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


def clean_my_resource(project):
    """运行过程中用于启动app"""
    if project.pwd() != '首页':
        xrs_adb.start_app('com.zwcode.p6slite', '.activity.SplashActivity')


definitions = {'超清': [(2560, 1440), (2304, 1296)],
               '高清': [(800, 448)],
               '标清': [(640, 368), (640, 364), (640, 360)]}


did_list = ['IOTDAA-337307-XWECW']   # H695AI/9630PGM-AI/S/W


@pytest.mark.run(order=1)
@pytest.mark.fourG_product
@pytest.mark.repeat(2)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
@pytest.mark.parametrize("did", did_list)
def test_bind_and_unbind_device(did: str, setup_environment):
    """测试绑定解绑设备"""
    project = setup_environment
    clean_my_resource(project)
    if project.is_element_exist('在线'):
        project.goto('更多页')
        project.clickControl('删除设备', 'text')
        if project.is_element_exist('继续删除'):
            project.clickControl('继续删除', 'text')
        elif project.is_element_exist('确定'):
            project.clickControl('确定', 'text')
        assert not project.is_element_exist('test_dev')  # 断言设备已从设备列表删除
    project.goto('手动添加页')
    project.goto('首页', did, 'test_dev')
    assert project.is_element_exist('test_dev')  # 断言设备已添加到设备列表
    project.driver.quit()
