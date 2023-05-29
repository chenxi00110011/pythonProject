import xrs_time
from xrs_app import MobieProject
from xrs_log import log_info
import xrs_adb


def initialized(appName):
    ruiboshi = MobieProject(appName)
    return ruiboshi


def share():
    obj = MobieProject('睿博士')
    for i in range(20):
        exception_count = 0
        log_info(f"\t第{i + 1}次运行")
        try:
            obj.goto('账户管理页')
            if obj.is_element_exist('13638601129'):
                obj.goto('登录页')
                obj.goto('首页', '18086409233', 'cx123456')
            obj.goto('分享设置页')
            obj.enterTo('请输入手机号或邮箱', '13638601129', 'text')
            obj.clickControl('分享', 'text')
            obj.goto('登录页')
            obj.goto('首页', '13638601129', 'cx123456')
            if not obj.is_element_exist('在线'):
                obj.goto('待处理信息页')
            obj.goto('更多页')
            obj.goto('登录页')
        except Exception as e:
            log_info(f"{xrs_time.get_current_time()}\t{e}")
            exception_count += 1
            if not xrs_adb.appIsRunning('com.zwcode.p6slite') or exception_count > 2:
                obj = MobieProject('睿博士')
                i -= 1
            continue


def share1():
    project = MobieProject('睿博士')
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

if __name__ == "__main__":
    share1()
