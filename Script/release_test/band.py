import time
import xrs_time
from xrs_app import MobieProject
from xrs_log import log_info
import xrs_adb
from my_decorator import repeat

'''
1、同一账号绑定解绑（手动绑定）
2、两个账户互相绑定解绑
'''


def unbind(project, did):
    if project.is_element_exist('test_dev') and not project.is_element_exist(did) or \
            project.is_element_exist('在线'):
        project.goto('更多页面')
        project.goto('首页')
        log_info("设备解绑")


def bind(project, did):
    if not (project.is_element_exist('test_dev') and not project.is_element_exist(did) or
            project.is_element_exist('在线')):
        project.goto('手动添加页')
        project.goto('首页', did, 'test_dev')
        log_info("设备绑定")


def bind_again(appName, did, test_times=10):
    ruiboshi = MobieProject(appName)
    exception_count = 0
    for i in range(test_times):
        log_info(f"\t第{i + 1}次运行")
        try:
            unbind(ruiboshi, did)
            time.sleep(60)
            bind(ruiboshi, did)
        except Exception as e:
            log_info(f"{xrs_time.get_current_time()}\t{e}")
            exception_count += 1
            if not xrs_adb.is_foreground('com.zwcode.p6slite') or exception_count > 2:
                ruiboshi = MobieProject('睿博士')
                i -= 1
            continue


@repeat(100)
def bind_againV1(project, appName, did):
    if not xrs_adb.is_foreground('com.zwcode.p6slite'):
        project = MobieProject(appName)
    unbind(project, did)
    time.sleep(30)
    bind(project, did)


def two_accounts_bind(appName, did, test_times=10, current_times=None):
    # 预置条件：启动睿博士app，检查18086409233和13638601129中设备是否删除
    ruiboshi = MobieProject(appName)
    exception_count = 0
    if current_times is None:
        current_times = 0
    ruiboshi.goto('首页', '18086409233', 'cx123456')
    if ruiboshi.is_element_exist('在线') or ruiboshi.is_element_exist('设备离线啦'):
        unbind(ruiboshi, did)
    else:
        ruiboshi.goto('首页', '13638601129', 'cx123456')
        if ruiboshi.is_element_exist('在线') or ruiboshi.is_element_exist('设备离线啦'):
            unbind(ruiboshi, did)
    # 循环在两个账户，绑定解绑设备
    for i in range(current_times, test_times):
        log_info(f"\t第{i + 1}次运行")
        try:
            ruiboshi.goto('登录页')
            ruiboshi.goto('首页', '18086409233', 'cx123456')
            bind(ruiboshi, did)
            unbind(ruiboshi, did)
            ruiboshi.goto('登录页')
            ruiboshi.goto('首页', '13638601129', 'cx123456')
            time.sleep(30)
            bind(ruiboshi, did)
            unbind(ruiboshi, did)
        except Exception as e:
            log_info(f"{xrs_time.get_current_time()}\t{e}")
            exception_count += 1
            if not xrs_adb.is_foreground('com.zwcode.p6slite') or exception_count > 1:
                two_accounts_bind('睿博士', 'IOTDBB-065896-UXLYD', test_times=test_times, current_times=i)
            else:
                continue


if __name__ == "__main__":
    project = MobieProject('睿博士')
    bind_againV1(project, '睿博士', 'IOTDBB-065896-UXLYD')
