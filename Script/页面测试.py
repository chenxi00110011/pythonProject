import time

from xrs_app import MobieProject


def test_jump():
    project = MobieProject('睿博士')
    for vex1 in project.LinkedGraph.listVex:
        project = MobieProject('睿博士')
        print(vex1.pageName)
        try:
            print('当前页面是', project.pwd(), '即将跳转到', vex1.pageName)
            project.goto(vex1.pageName)
        except Exception as e:
            print(e)
            continue


project = MobieProject('睿博士')
while True:
    print(project.pwd())
    time.sleep(5)