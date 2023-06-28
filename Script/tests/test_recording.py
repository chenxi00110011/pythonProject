# 模块名称：test_recording
# 模块内容：基于appium的自动化测试，主要用于睿博士的卡录像功能
# 作者: 陈 熙
# -*- coding: utf-8 -*-
import os
import time
import shutil
from imports import MobieProject, pytest, xrs_adb, getMp4Information, read_excel_to_dict, ntp_util
from imports import adb_download, serial_bitstream, image_properties, environment_variable


def clean_my_resource(project):
    """运行过程中用于启动app"""
    if project.pwd() != '首页':
        xrs_adb.start_app('com.zwcode.p6slite', '.activity.SplashActivity')


@pytest.mark.recording
def test_card_formatting(setup_environment: MobieProject):
    """测试格式化卡"""
    project = setup_environment
    project.goto('设置页')
    project.scroll_to_element('录像与存储')
    project.goto('录像存储设置页')
    project.clickControl('格式化存储卡', 'text')
    project.clickControl('开始格式化', 'text', wait=30)
    assert project.is_element_exist('正在写入')
    assert project.is_element_exist('100%')


@pytest.mark.playback_speed
def test_playback_speed(setup_environment: MobieProject):
    """测试倍数播放"""
    time_stamp = ntp_util.get_ntp_timestamp()
    t1 = ntp_util.get_formatted_ntp_time(dateTimeStr='%H:%M', timestamp=time_stamp - 3600)
    t2 = ntp_util.get_formatted_ntp_time(dateTimeStr='%H:%M', timestamp=time_stamp - 300)
    project = setup_environment
    project.goto('回放页')
    if project.is_element_exist('卡录像') and project.is_element_exist('云录像'):
        project.clickControl('卡录像', 'text')
    project = setup_environment
    project.goto('回放页')
    assert project.check_sdcard_recording_breakpoint((t1, t2))
    project.clickControl(control=[(600, 540)], mode='bounds')


definitions = {'超清': [(2560, 1440), (2304, 1296)],
               '高清': [(800, 448)],
               '标清': [(640, 368), (640, 364), (640, 360)]}


@pytest.mark.record_and_screenshot
# @pytest.mark.parametrize("definition", definitions.keys())
def test_record_and_screenshot(setup_environment: MobieProject, definition='超清'):
    """测试卡回放录像与截图"""
    time_stamp = ntp_util.get_ntp_timestamp()
    t1 = ntp_util.get_formatted_ntp_time(dateTimeStr='%H:%M', timestamp=time_stamp - 900)
    t2 = ntp_util.get_formatted_ntp_time(dateTimeStr='%H:%M', timestamp=time_stamp - 600)

    folder_path = environment_variable.adb_download + 'screenshot'
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # 删除pc端存储截图的文件夹

    project = setup_environment
    project.goto('回放页')
    if project.is_element_exist('卡录像') and project.is_element_exist('云录像'):
        project.clickControl('卡录像', 'text')
    assert project.check_sdcard_recording_breakpoint((t1, t2))
    os.system(xrs_adb.command_dict['清空睿博士录像'])
    os.system(xrs_adb.command_dict['清空睿博士截图'])
    project.clickControl('截图', 'text')
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
    assert arguments['平均码率'] <= 1500  # 检查平均码率
    assert '音频格式' in arguments.keys()

    os.system(xrs_adb.command_dict['下载睿博士截图'])
    image_properties_list = image_properties.get_all_image_properties(folder_path)  # 获取pc存储截图目录下的所有图片参数，返回列表
    print(definitions[definition], image_properties_list[0]['size'])
    assert image_properties_list[0]['size'] in definitions[definition]  # 断言，检查截图分辨率
    project.driver.quit()


