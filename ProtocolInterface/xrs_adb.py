import os, re
import socket
import subprocess
import time

import environment_variable as env

command_dict = {
    '点亮屏幕': 'adb shell input keyevent 224',
    '下载睿博士录像': f'adb pull {env.p6slite_videos} {env.adb_download}',
    '清空睿博士录像': f"adb shell rm {env.p6slite_videos}*mp4 ",
    '下载相册': f'adb pull {env.photo_album} {env.adb_download}',
    '获取安卓版本': 'adb shell getprop ro.build.version.release',
    '获取手机分辨率': 'adb shell wm size',
    '滑屏解锁': 'adb shell input swipe 300 1000 300 500',
    '密码解锁': 'adb shell input text password'
}


def wakeUpScreen():
    # 点亮屏幕
    # os.system("adb shell input keyevent KEYCODE_POWER")
    os.system('adb shell input keyevent 224')


def unlockScreen():
    pass


def is_foreground(package_name):
    # 判断app是否为前台运行
    command = "adb shell \"dumpsys window | grep mCurrentFocus\""
    all_info = os.popen(command).readlines()
    if package_name in all_info[0]:
        return True
    return False


def popen(command):
    return os.popen(command_dict[command]).readlines()[0]


def get_screen_resolution():
    result = popen('获取手机分辨率')
    devices_name = re.findall('\d{3,4}', result, re.S)
    devices_name = (eval(devices_name[0]), eval(devices_name[1]))
    return devices_name


# 检查手机是否已连接
def check_device_connection():
    try:
        adb_devices = subprocess.check_output('adb devices', shell=True, universal_newlines=True)
        if not re.search(r'^\S+\tdevice$', adb_devices, flags=re.MULTILINE):
            return False
    except subprocess.CalledProcessError:
        return False
    return True


# 检查appuim服务器端口
def check_appium_server(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', port))
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return True
    except ConnectionRefusedError:
        return False


# 启动app
def start_app(package_name='', activity_name=''):
    # 停止应用程序
    stop_cmd = f'adb shell am force-stop {package_name}'
    subprocess.run(stop_cmd, shell=True)

    # 暂停一段时间，确保应用程序已停止
    time.sleep(2)

    # 启动应用程序
    start_cmd = f'adb shell am start -n {package_name}/{activity_name}'
    subprocess.run(start_cmd, shell=True)

    # 暂停一段时间，以确保应用程序已启动
    time.sleep(15)

    # 检查应用程序是否在前台运行
    if not is_foreground(package_name):
        # 应用程序在前台无法运行，报错退出
        raise RuntimeError(f'Failed to bring app {package_name} to foreground')

    print(f'{package_name} 启动成功！')


if __name__ == "__main__":
    start_app('com.zwcode.p6slite', '.activity.SplashActivity')
