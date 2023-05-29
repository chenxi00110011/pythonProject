import pyautogui
import time
import xrs_serial
import arp_scan
import xrs_time
import xrs_cgi


pyautogui.PAUSE = 0.5

def get_mouse_location():
    '''
    查询显示分辨率
    查询鼠标坐标位置
    '''
    print(pyautogui.size())                   #  显示屏分辨率
    print(pyautogui.position())               #  鼠标坐标位置

easytool_location = {
    '刷新列表':(402.,42),
    '全选设备':(19,77),
    '固件升级':(1760,457),
    '登录确认': (999,610),
    '升级包01': (252,141),
    '升级包02': (252,159),
    '结果确认':(991,591),
}



def mouse_click(str):
    _tuple = easytool_location[str]
    pyautogui.click(_tuple[0],_tuple[1])

def mouse_double_click(str):
    _tuple = easytool_location[str]
    pyautogui.doubleClick(_tuple[0],_tuple[1])

def easytool_upgrade(upgrade_name, wait_time, blackout=False):
    mouse_click('登录确认')
    mouse_click('刷新列表')
    mouse_click('全选设备')
    mouse_click('固件升级')
    mouse_click('登录确认')
    mouse_double_click(upgrade_name)
    if blackout:
        time.sleep(wait_time)
        xrs_serial.serial_bitstream('com36','断电', 1)
        xrs_serial.serial_bitstream('com36','上电', 1)
    else:
        #设备需要先离线，然后后在线，就代表升级完成
        while arp_scan.all_islive(dev_mac):
            #此处循环检查设备是否存活，如果失败则跳出循环
            print(xrs_time.get_current_time(),'设备正在升级，请等待')
    time.sleep(10)
    while not arp_scan.all_islive(dev_mac):
        # 此处循环检查设备是否存活，如果成功则跳出循环
        print(xrs_time.get_current_time(),'未探测到设备')
        time.sleep(10)
    else:
        time.sleep(120)
        print(xrs_time.get_current_time(),'设备设备已启动')
        mouse_click('结果确认')



if __name__ == '__main__':
    upgrade_time = 40
    test_times = 40
    dev_mac = [
        '5A:00:08:83:74:F6',
        '5A:00:E5:3C:E7:0E'
    ]
    xrs_serial.serial_bitstream('com36','上电', 1)
    # get_mouse_location()
    j = 1
    while arp_scan.all_islive(dev_mac):
        time.sleep(20)
        print(xrs_time.get_current_time(), F'第{j}轮测试升级')
        j += 1
        for i in range(test_times):
            time_wait = i*(upgrade_time/test_times) + 10
            print(xrs_time.get_current_time(), F'在{time_wait}秒后断电上电')
            if arp_scan.islive(dev_mac[0]) and xrs_cgi.getDeviceVersion(arp_scan.ge_ip(dev_mac[0])) == '1.0.0-20230310':
                easytool_upgrade("升级包02",wait_time=time_wait, blackout=True)
            else:
                easytool_upgrade("升级包01", wait_time=time_wait, blackout=True)