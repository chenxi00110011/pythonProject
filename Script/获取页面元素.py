from xrs_app import MobieProject,get_element_data
from environment_variable import cmri_excel_element_dict


def save_element_to_excel():
    # 存储每个页面的元素到excel，用于判断当前所属页面
    project = MobieProject('和家亲')
    # 获取 app 页面元素列表
    while True:
        vertex_name = input("请确定页面是否跳转成功后，输入页面名称:")
        elements = project.driver.find_elements_by_xpath("//*")
        # 输出元素数量
        print("页面元素数量为：", len(elements))
        # 保存到excel
        for element in elements:
            if element.get_attribute('resource-id') or element.text:
                get_element_data(element, cmri_excel_element_dict, vertex_name)



save_element_to_excel()