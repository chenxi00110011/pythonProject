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


def setup_environmentV1():
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
        # 判断app是否启动
        if project.pwd() == '首页':
            return project
        else:
            setup_environmentV1()
    except Exception as e:
        print(e)
        setup_environment()


def clean_my_resource(project):
    """运行过程中用于启动app"""
    if project.pwd() != '首页':
        xrs_adb.start_app('com.zwcode.p6slite', '.activity.SplashActivity')


did_list = ['IOTDBB-065896-UXLYD']


# did_list = ['IOTDAA-733849-MGVRF']


@pytest.mark.run(order=1)
@pytest.mark.bind
@pytest.mark.smoke
@pytest.mark.repeat(2)
@pytest.mark.flaky(reruns=5, reruns_delay=1)
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


definitions = {'超清': [(2560, 1440), (2304, 1296)],
               '高清': [(800, 448)],
               '标清': [(640, 368), (640, 364), (640, 360)]}


@pytest.mark.run(order=2)
@pytest.mark.live
@pytest.mark.smoke
@pytest.mark.repeat(1)
@pytest.mark.parametrize("definition", definitions.keys())
@pytest.mark.flaky(reruns=5, reruns_delay=10)
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
    assert arguments['分辨率'] in definitions[definition]  # 检查分辨率是否符合要求
    assert arguments['视频帧率'] > 11  # 检查帧率是否大于11
    assert arguments['平均码率'] <= 3000  # 检查平均码率
    assert arguments['码率控制方式'] == 'VBR'  # 检查码率控制方式


@pytest.mark.run(order=3)
@pytest.mark.live_dela
@pytest.mark.smoke
@pytest.mark.repeat(1)
@pytest.mark.parametrize("definition", definitions.keys())
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_live_delay(definition, setup_environment: MobieProject):
    screenshotDirPath = environment_variable.adb_download + 'screenshot\\'
    project = setup_environment
    project.goto('直播页')
    project.clickControl('画质', 'text')
    os.system(xrs_adb.command_dict['清空睿博士截图'])
    xrs_adb.remove_path(screenshotDirPath)
    project.clickControl('截图', 'text')
    time_stamp = ntp_util.get_ntp_timestamp(int_val=1)  # 先获取ntp时间，再截图
    project.clickControl(definition, 'text')
    os.system(xrs_adb.command_dict['下载睿博士截图'])
    dev_time_stamp = image_properties.image_timestamp(screenshotDirPath)[0]
    print(time_stamp - dev_time_stamp)
    assert time_stamp - dev_time_stamp <= 4


@pytest.mark.run(order=100)
@pytest.mark.status
@pytest.mark.smoke
@pytest.mark.repeat(1)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
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
    assert int(end_time - start_time) <= 150  # 检查离线状态刷新时间是否小于等于60秒

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


@pytest.mark.run(order=99)
@pytest.mark.share
@pytest.mark.smoke
@pytest.mark.repeat(1)
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_share_feature(setup_environment: MobieProject):
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
    project.driver.quit()


@pytest.mark.run(order=5)
@pytest.mark.network
@pytest.mark.smoke
@pytest.mark.repeat(1)
@pytest.mark.flaky(reruns=1, reruns_delay=1)
def test_4G_data_query(setup_environment: MobieProject):
    """此处编写测试代码，查询4G流量的结果是否与实际情况一致"""
    project = setup_environment
    project.goto('4G流量查询页')
    if project.is_element_exist('请联系卖家客服进行充值'):
        return
    project.goto('4G流量详情页')
    pattern = r'\d+\.\d+'
    assert project.is_element_exist('正使用')  # 检查卡状态
    assert project.is_element_exist(f'已用：{pattern}GB剩余：无限量')  # 检查流量
    project.driver.quit()


@pytest.mark.run(order=2)
@pytest.mark.audio
# @pytest.mark.smoke
@pytest.mark.repeat(1)
@pytest.mark.flaky(reruns=1, reruns_delay=1)
def test_intercom(setup_environment: MobieProject):
    """测试对讲，目前仅通过APP端进行验证"""
    project = setup_environment
    text1 = xrs_adb.get_audio_logs()
    assert ('type:android.media.AudioTrack' not in text1)  # 检查是否播放过音频
    assert ('src:MIC pack:com.zwcode.p6slite' not in text1)  # 检查是否采集声音
    project.goto('直播页')
    project.clickControl('声音', 'text')
    time.sleep(10)
    project.clickControl('声音', 'text')
    text2 = xrs_adb.get_audio_logs()
    assert ('type:android.media.AudioTrack' in text2)  # 检查是否播放过音频
    project.long_press_element_by_uiautomator('对讲', 5000)
    text3 = xrs_adb.get_audio_logs()
    assert ('src:MIC pack:com.zwcode.p6slite' in text3)  # 检查是否采集声音
    project.driver.quit()


def test_camera_rotation():
    # 云台转动，目前不方便检查转动的结果
    # 测试摄像头转动的代码写在这里
    pass


def test_camera_position_memory():
    # 场景记忆
    # 测试记住摄像头当前位置的代码写在这里
    pass


def test_cruise_control():
    # 测试巡航的代码写在这里
    pass


def test_human_tracking():
    # 测试追踪功能的代码写在这里
    pass


resolutionDict = {'超清': [(2560, 1440), (2304, 1296)],
                  '高清': [(800, 448)],
                  '标清': [(640, 368), (640, 364), (640, 360)]}


@pytest.mark.run(order=6)
@pytest.mark.screenshot
@pytest.mark.smoke
@pytest.mark.repeat(1)
@pytest.mark.parametrize("definition", resolutionDict.keys())
@pytest.mark.flaky(reruns=1, reruns_delay=1)
def test_screenshot(definition, setup_environment: MobieProject):
    # 测试截图的代码写在这里
    folder_path = environment_variable.adb_download + 'screenshot'
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # 删除pc端存储截图的文件夹
    project = setup_environment
    project.goto('直播页')
    os.system(xrs_adb.command_dict['清空睿博士截图'])
    project.clickControl('画质', 'text')
    project.clickControl(definition, 'text')
    project.clickControl('截图', 'text')
    os.system(xrs_adb.command_dict['下载睿博士截图'])
    image_properties_list = image_properties.get_all_image_properties(folder_path)  # 获取pc存储截图目录下的所有图片参数，返回列表
    print(resolutionDict[definition], image_properties_list[0]['size'])
    assert image_properties_list[0]['size'] in resolutionDict[definition]  # 断言，检查截图分辨率
    project.driver.quit()


@pytest.mark.run(order=11)
@pytest.mark.card
@pytest.mark.smoke
@pytest.mark.repeat(1)
@pytest.mark.flaky(reruns=5, reruns_delay=1)
def test_dash_cam_recording(setup_environment: MobieProject):
    """检查卡录像断点"""
    time_stamp = ntp_util.get_ntp_timestamp()
    t1 = ntp_util.get_formatted_ntp_time(dateTimeStr='%H:%M', timestamp=time_stamp - 3900)
    t2 = ntp_util.get_formatted_ntp_time(dateTimeStr='%H:%M', timestamp=time_stamp - 300)
    project = setup_environment
    project.goto('回放页')
    assert project.check_sdcard_recording_breakpoint((t1, t2))
    project.driver.quit()


@pytest.mark.run(order=12)
@pytest.mark.download_dashcam
@pytest.mark.smoke
@pytest.mark.repeat(1)
@pytest.mark.flaky(reruns=1, reruns_delay=1)
def test_download_dashcam_video(setup_environment: MobieProject):
    """下载卡录像，并检查参数"""
    os.system(xrs_adb.command_dict['清空睿博士录像'])
    os.system(xrs_adb.command_dict['清空睿博士截图'])
    project = setup_environment
    project.goto('录像列表页')

    # 选择第一个录像文件下载
    project.clickControl('com.zwcode.p6slite:id/iv_download', 'resource_id')
    project.clickControl('录像下载', 'text')

    # 等待下载完成，并跳转到相册
    while project.is_element_exist('正在下载'):
        time.sleep(10)
    project.clickControl('跳转到相册', 'text')

    # 断言存在录像文件
    assert project.is_element_exist('com.zwcode.p6slite:id/item_album_pic_iv')

    dir = adb_download + 'videos\\'
    shutil.rmtree(dir)
    os.system(xrs_adb.command_dict['下载睿博士录像'])
    fileName = os.listdir(dir)[0]
    arguments = getMp4Information(dir + fileName)
    print(arguments)
    assert arguments['分辨率'] in definitions['超清']  # 检查分辨率是否符合要求
    assert arguments['视频帧率'] > 11  # 检查帧率是否大于11
    assert arguments['平均码率'] <= 3000  # 检查平均码率
    assert arguments['码率控制方式'] == 'VBR'  # 检查码率控制方式


@pytest.mark.run(order=7)
@pytest.mark.devices
# @pytest.mark.smoke
def test_device_info(setup_environment: MobieProject):
    # 检查设备信息的代码写在这里
    device_dict = read_excel_to_dict(environment_variable.ruiboshi_excel, '设备详情', 'IOTDBB-065896-UXLYD', 3)
    project = setup_environment
    project.goto('设备信息查询页')
    for key, val in device_dict.items():
        assert project.is_element_exist(key)
        val[0] = str(val[0])
        assert project.is_element_exist(val[0])
        print(key, project.is_element_exist(key))
        print(val[0], project.is_element_exist(val[0]))


@pytest.mark.run(order=8)
@pytest.mark.timezone
@pytest.mark.smoke
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_timezone(setup_environment: MobieProject):
    """检查ntp对时误差"""
    project = setup_environment
    project.goto('时间设置页')
    element = project.driver.find_element_by_id('com.zwcode.p6slite:id/dev_time_systemtime_time')
    devices_time = element.get_attribute('text')
    print(devices_time)
    device_timestamp = ntp_util.str_time_to_timestamp(devices_time)
    ntp_timestamp = ntp_util.get_ntp_timestamp()
    assert device_timestamp < ntp_timestamp + 1 or device_timestamp > ntp_timestamp - 1
    project.driver.quit()


@pytest.mark.run(order=9)
@pytest.mark.sleep_mode
@pytest.mark.smoke
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_sleep_mode(setup_environment: MobieProject):
    project = setup_environment
    if project.is_element_exist('立即唤醒'):
        project.clickControl('立即唤醒', 'text')
    project.goto('立即睡眠')
    project.goto('首页')
    assert project.is_element_exist('睡眠中')
    assert project.is_element_exist('立即唤醒')
    project.clickControl('立即唤醒', 'text')
    assert not project.is_element_exist('睡眠中')
    assert project.is_element_exist('在线')
    project.driver.quit()


def test_reset_to_defaults():
    # 执行恢复出厂设置的操作，示例代码：
    pass


parameterStore = ['移动', '人形']


@pytest.mark.run(order=10)
@pytest.mark.event
@pytest.mark.smoke
@pytest.mark.repeat(2)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
@pytest.mark.parametrize("parameter", parameterStore)
def test_event_reported(parameter: str, setup_environment: MobieProject):
    # 执行事件上报，示例代码：
    project = setup_environment
    project.goto('报警管理页')
    attribute = {'resource_id': 'com.zwcode.p6slite:id/param_switch'}
    element = project.find_nearest_element(attribute, parameter + '侦测报警')
    time.sleep(3)
    t1 = ntp_util.get_ntp_timestamp()
    if project.is_element_checkable(element):
        element.click()  # 关闭侦测使能
    if not project.is_element_checkable(element):
        element.click()  # 打开侦测使能
    while True:
        project.goto('首页')
        project.goto('消息查询页')

        # 　检查消息通知功能是否开启
        if project.is_element_exist('消息通知功能未开启'):
            project.clickControl('立即开启', 'text')
            project.clickControl('确定', 'text')
            project.goto('消息查询页')

        #  检查超时时间
        assert ntp_util.get_ntp_timestamp() - t1 <= 300

        #  检查是否出现事件
        if not project.is_element_exist(parameter):
            time.sleep(15)
            continue

        # 找到对应的事件名称
        if parameter == '人形':
            parameter = '人形检测'
        elif parameter == '移动':
            parameter = '移动侦测'

        # 找到第一条事件对应的时间戳
        attribute = {'text': parameter}
        motion_element = project.find_nearest_element(attribute, '全部时间')
        attribute = {'resource_id': 'com.zwcode.p6slite:id/push_tv_time'}
        motion_element = project.find_nearest_element(attribute, motion_element)
        time_value = motion_element.get_attribute('text')
        motion_event_timestamp = ntp_util.str_time_to_timestamp(time_value)

        # 比较时间戳，如果是在打开使能之后，则退出循环，反之则继续循环
        if motion_event_timestamp < t1:
            time.sleep(10)
            continue

        if motion_event_timestamp > t1:
            break
    project.driver.quit()


def test_volume():
    # 检查音量的代码写在这里
    pass
