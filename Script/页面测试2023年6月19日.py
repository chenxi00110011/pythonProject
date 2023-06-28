import time

from xrs_app import MobieProject, get_element_data
from environment_variable import cmri_excel_element_dict


def save_element_to_excel(appName='睿博士'):
    # 存储每个页面的元素到excel，用于判断当前所属页面
    project = MobieProject(appName)
    # 获取 app 页面元素列表
    test_list = ["增值业务办理"]
    for vex1 in test_list:
        flag = input(f"当前页面为:{vex1},请确定页面是否跳转成功:")
        if flag:
            continue
        elements = project.driver.find_elements_by_xpath("//*")
        # 输出元素数量
        print("页面元素数量为：", len(elements))
        # 保存到excel
        for element in elements:
            try:
                if element.text:
                    get_element_data(element, cmri_excel_element_dict, str(vex1), sheetName='universalapp')
            except Exception as e:
                print(e)
                continue


def test_pwd():
    project = MobieProject('睿博士')
    while True:
        print(project.pwd())
        input('请按回车继续：')

if __name__ == '__main__':
    # save_element_to_excel(appName='和家亲')
    test_pwd()