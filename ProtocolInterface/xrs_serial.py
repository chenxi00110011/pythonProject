import serial
import time
import xrs_time
from my_decorator import thread_decorator

"""
直接安装pyserial库即可，不要安装serial库
"""
dict_bitstream = {
    '上电': ['A0', '01', '01', 'A2'],
    '断电': ['A0', '01', '00', 'A1']
}

command_dict = {
    '创建工厂文件':'',
    '设备重启':'reboot',
    '获取网卡信息': '',
    '运行tf卡读写测试程序': 'mkdir -p /tmp/app/disk/mmcblk0p1;mount /dev/mmcblk0p1   /tmp/app/disk/mmcblk0p1; cd  /tmp/app/disk/mmcblk0p1;./iotest ',
    '调试模式': 'touch /mnt/mtd/en_debug_mode'
}

def default_command(self, command):
    if command:
        return command + '\r\n'
    else:
        return ''


def serial_bitstream(com, _str_code, time_delay=30):
    # 配置串口基本参数并建立通信
    ser = serial.Serial(com,9600)
    print(xrs_time.get_current_time(), '\t', f'设备{_str_code}，延时{time_delay}秒')
    _str_code = dict_bitstream[_str_code]
    for data in _str_code:
        hex_data = bytes.fromhex(data)
        # print(hex_data)
        # 串口发送数据
        result = ser.write(hex_data)
        time.sleep(0.1)
    time.sleep(time_delay)
    ser.close()

def serial_sent_utf(self, command, num=0):
    # 从字典里获取对应的RS232命令
    # encode()函数是编码，把字符串数据转换成bytes数据流
    self.ser.write(self.default_command(command).encode())
    data = self.ser.read(num)
    # 获取指令的返回值，并且进行类型转换，转换为字符串后便可以进行字符串对比，因而便可以根据返回值进行判断是否执行特定功能
    data = str(data, encoding='utf-8')
    return data

@thread_decorator
def keyboard_input(self):
    while True:
        keyboard_buff = input()
        self.serial_sent_utf(keyboard_buff)


if __name__ == '__main__':
    com = 'com36'
    serial_bitstream(com,'断电',15)
    serial_bitstream(com,'上电',600)


    # serial.Serial('com31', 115200)
