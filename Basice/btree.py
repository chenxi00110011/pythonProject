import pickle
import environment_variable as env

'''
1、使用三个类，Node类用于构建树状双向链表结构，
Page类抽象页面，包含页面标志、跳转点
Element类为Page类的内部类，是构建Page类的一部分
'''


class Node:
    # 初始化一个节点
    def __init__(self, val=None):
        self.val = val  # 节点值,就是Page对象
        self.parent = None  # 父节点
        self.child = []  # 子节点列表
        # print(self.__name__)

    def addChild(self, node):
        # 添加子节点，如果该节点已被添加，则直接返回
        # print(self.child)
        node.parent = self
        for n in self.child:
            if n.val.pageName == node.val.pageName:
                return
        self.child.append(node)

    # 添加父节点
    def addParent(self, node):
        self.parent = node
        for n in node.child:
            if n.val.pageName == self.val.pageName:
                return
        node.child.append(self)

    # 添加节点数据
    def addVal(self, value):
        self.val = value

    def showAllKinsfolk(self):
        print(self, "亲属有")
        print("父节点：", self.parent)
        for node in self.child:
            print("子节点：", node)

    # 展示所有Page的名称
    def showAllPageName(self):
        print(f"页面名称：{self.val}")

    # 展示所有elem的名称
    def showAllElem(self):
        print("页面元素已添加：", end=" ")
        for e in self.val.elem:
            print(e, end='\t')
        print('')
        print("页面标志已添加：", self.val.sign)
        print("跳转点已添加：", end=" ")
        for e in self.val.springboard:
            print(e, end='\t')
        print('')
        print("返回父节点已添加：", end=" ")
        for e in self.val.toParent:
            print(e, end='\t')
        print('')

    @staticmethod
    def save(filePath, data):
        with open(filePath, 'wb+')as file:
            pickle.dump(data, file, 1)

    @staticmethod
    def load(filePath):
        with open(filePath, 'rb+')as file:
            obj = pickle.load(file)
        return obj

    def __str__(self):
        return self.val.pageName


class Page:

    def __init__(self, page_dict):
        self.pageName = page_dict['pageName']  # 页面名称
        self.appPackage = page_dict['appPackage']  # app包名
        self.appActivity = page_dict['appActivity']  # activity
        self.sign = page_dict['sign']  # 页面标志，唯一性，列表类型
        self.springboard = page_dict['springboard']  # 跳转点，用于进入当前页面，字典类型{元素ID，位置，文本，控件类型}，列表类型
        self.toParent = page_dict['toParent']  # 返回父节点，同page_dict['springboard']，列表类型
        self.elem = []  # 列表类型

    def add_elem(self, _dict: dict):
        _list = [None for i in range(len(_dict))]
        i = 0
        for k, v in _dict.items():
            _list[i] = Element(v, k)
            i += 1
        self.elem = _list

    def __str__(self):
        return self.pageName


class Element:
    def __init__(self, _dict, name):
        self.elemName = name
        self.id = _dict['resource_id']  # 元素的resource_id，可能没有
        self.bounds = _dict['bounds']  # 元素的bounds，这个是坐标点，一定有，可能对于输入框类型无效
        self.text = _dict['text']  # 元素的文本值，可能没有
        self.type = _dict['type']  # 控件类型，目前仅有button和input_box
        self.val = _dict['val']  # 输入值，当控件类型为input_box，此默认值有效

    def __str__(self):
        return self.elemName


if __name__ == "__main__":
    filePath = env.pathOfNode
    elem_d = {
        '转到添加设备页面': {'resource_id': 'com.zwcode.p6slite:id/tip_tv', 'bounds': [(540,1462)], 'text': '若未找到二维码，点击此处添加', 'type': 'button', 'val': ''},
        '回退': {'resource_id': 'com.zwcode.p6slite:id/back', 'bounds': [(64,143)], 'text': None,'type': 'button', 'val': ''}

    }
    page_dict = {
        'pageName': '扫一扫页面',
        'appPackage': 'com.zwcode.p6slite',
        'appActivity': '.activity.ScanActivity',
        'sign': [],
        'springboard': [],
        'toParent': []
    }
    # 先读取存储的节点信息
    root: Node = Node.load(filePath)
    root.showAllPageName()
    root.showAllElem()
    root.showAllKinsfolk()

    # # root.child = []
    # n1 = Node()
    # main = Page(page_dict)
    # main.add_elem(elem_d)
    # main.sign = main.elem[0]
    # n1.val = main
    # n1.showAllPageName()
    # n1.showAllElem()
    # root.addChild(n1)
    # root.showAllKinsfolk()
    # n1.showAllKinsfolk()
    Node.save(filePath, root)
    # print(root.showDomesticRelation())

    # print(root.val)
