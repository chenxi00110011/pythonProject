# 模块名称：appium_autotest_test
# 模块内容：基于appium的自动化测试
# -*- coding: utf-8 -*-
import time, os, shutil
from imports import MobieProject, pytest, xrs_adb, xrs_app, getMp4Information
from imports import adb_download, serial_bitstream

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
    project = MobieProject('睿博士')
    project.goto('个人管理页')
    # 判断设备是否使用18086409233账户登录
    if not project.is_element_exist('18086409233'):
        project.goto('登录页')
        project.goto('首页', '18086409233', 'cx123456')
    else:
        project.goto('首页', '18086409233', 'cx123456')

    # 判断app是否启动
    if project.pwd() == '首页':
        return project
    else:
        setup_environment


def clean_my_resource(project):
    """运行过程中用于启动app"""
    if project.pwd() != '首页':
        xrs_adb.start_app('com.zwcode.p6slite', '.activity.SplashActivity')


did_list = ['IOTDBB-065896-UXLYD']


@pytest.mark.bind
@pytest.mark.smoke
@pytest.mark.repeat(2)
@pytest.mark.parametrize("did", did_list)
def test_bind_and_unbind_device(did: str, setup_environment):
    """测试绑定解绑设备"""
    # 等待时间
    time_wait = 5
    # 在这里编写测试绑定和解绑设备的代码
    project = setup_environment
    clean_my_resource(project)
    assert project.pwd() == '首页'  # 断言当前处于首页
    if project.is_element_exist('test_dev'):
        project.goto('更多页')
        project.goto('首页')
        assert not project.is_element_exist('test_dev')  # 断言设备已从设备列表删除
        time_wait = 60
    time.sleep(time_wait)
    project.goto('手动添加页')
    project.goto('首页', did, 'test_dev')
    assert project.is_element_exist('test_dev')  # 断言设备已添加到设备列表


definitions = {'超清': (2560, 1440),
               '高清': (800, 448),
               '标清': (640, 368)}


@pytest.mark.live
@pytest.mark.smoke
@pytest.mark.repeat(2)
@pytest.mark.parametrize("definition", definitions.keys())
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_live_video_params(definition, setup_environment):
    """测试视频参数，例如帧率、码率、分辨率、码率控制"""
    project = setup_environment
    project.goto('直播页')
    project.clickControl('画质', 'text')
    project.clickControl(definition, 'text')
    os.system(xrs_adb.command_dict['清空睿博士录像'])
    project.clickControl('录像', 'text')
    time.sleep(10)
    project.clickControl('录像', 'text')
    dir = adb_download + 'videos\\'
    shutil.rmtree(dir)
    os.system(xrs_adb.command_dict['下载睿博士录像'])
    fileName = os.listdir(dir)[0]
    arguments = getMp4Information(dir + fileName)
    print(arguments)
    assert arguments['分辨率'] == definitions[definition]  # 检查分辨率是否一致
    assert arguments['视频帧率'] > 11  # 检查帧率是否大于11
    assert arguments['平均码率'] <= 3000  # 检查平均码率
    assert arguments['码率控制方式'] == 'VBR'  # 检查码率控制方式


@pytest.mark.live
@pytest.mark.smoke
@pytest.mark.repeat(5)
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_online_offline_status_update_time(setup_environment):
    """测试在线离线刷新时间"""
    # 离线状态刷新时间
    serial_bitstream('com36', '上电', 1)
    project = setup_environment
    project.goto('首页')
    start_time = time.time()
    serial_bitstream('com36', '断电', 1)
    while True:
        if project.is_element_exist('设备离线啦', times=1, wait=5):
            end_time = time.time()
            break
        if project.pwd() != '首页':
            raise Exception("The app has stopped working")
    print(f'离线状态自动刷新时间：{int(end_time - start_time)}秒')
    assert int(end_time - start_time) <= 60  # 检查离线状态刷新时间是否小于等于60秒

    # 在线状态刷新时间
    start_time = time.time()
    serial_bitstream('com36', '上电', 1)
    while True:
        if project.is_element_exist('在线', times=1, wait=5):
            end_time = time.time()
            break
        if project.pwd() != '首页':
            raise Exception("The app has stopped working")
    print(f'在线状态自动刷新时间：{int(end_time - start_time)}秒')
    assert int(end_time - start_time) <= 60  # 检查在线状态刷新时间是否小于等于60秒


@pytest.mark.share
@pytest.mark.smoke
@pytest.mark.repeat(5)
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_share_feature(setup_environment):
    """
    用例名称：分享设备
    前置条件：已登录账户18086409233，设备已绑定，设备未分享
    测试步骤：
    1、先登录18086409233，分享设备给13638601129
    2、再登录13638601129，接受分享设备，并检查设备是否在线
    3、最受再解除分享
    检查点
    """
    project = setup_environment
    project.goto('登录页')
    # 登录18086409233分享设备
    project.goto('首页', '18086409233', 'cx123456')
    project.goto('分享查询页1')
    if project.is_element_exist('13638601129'):
        project.goto('访客设置页')
        project.clickControl('删除访客', 'text')
    project.goto('分享设置页')
    project.enterTo('请输入手机号或邮箱', '13638601129', 'text')
    project.clickControl('分享', 'text')

    # 登录13638601129账户，接受分享
    project.goto('登录页')
    project.goto('首页', '13638601129', 'cx123456')
    if not project.is_element_exist('test_dev'):
        project.goto('待处理信息页')
    project.goto('首页')

    # 检查设备列表是否显示该设备
    assert project.is_element_exist('test_dev')

    # 登录18086409233账户，查看分享状态
    project.goto('登录页')
    project.goto('首页', '18086409233', 'cx123456')
    project.goto('分享查询页1')

    # 检查主账户分享状态
    assert project.is_element_exist('13638601129')

    # 登录13638601129取消分享
    project.goto('登录页')
    project.goto('首页', '13638601129', 'cx123456')
    project.goto('更多页')
    project.goto('登录页')


@pytest.mark.network
@pytest.mark.repeat(1)
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_4G_data_query(setup_environment:MobieProject):
    # 此处编写测试代码，查询4G流量的结果是否与实际情况一致
    # 测试代码一般包括测试准备、测试步骤、测试断言
    project = setup_environment
    project.goto('4G流量详情页')
    pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    # project.driver.find_element_by_android_uiautomator(
    #                     f'new UiSelector().text("已用：{pattern}GB剩余：无限量")')
    assert project.is_element_exist('正使用')  # 检查卡状态
    assert project.is_element_exist(f'已用：{pattern}GB剩余：无限量')  # 检查流量

