import xrs_serial
import time
import  re


def comp(c1,text):
    res = re.findall(c1,text)
    return res[0]


def avg_tf_test(path):
    with open(path,'r') as read_to_file:
        text = read_to_file.read()
    write_list = re.findall(r'write.*',text)
    read_list = re.findall(r'read.*',text)
    for i in range(len(write_list)):
        text_new = comp(r'\d{0,2}.\d{2} MB/sec',write_list[i])
        text_new = comp(r'\d{0,2}.\d{2}', text_new)
        write_list[i] = float(text_new)
    for i in range(len(read_list)):
        text_new = comp(r'\d{0,2}.\d{2} MB/sec',read_list[i])
        text_new = comp(r'\d{0,2}.\d{2}', text_new)
        read_list[i] = float(text_new)

    print(write_list,'\n',read_list)
    print('write：%0.2f MB/sec'%(sum(write_list)/len(write_list)))
    print('read：%0.2f MB/sec'%(sum(read_list)/len(read_list)))


ser = xrs_serial.XrsSerial('COM31')
ser.circular_print()
ser.serial_sent_utf(xrs_serial.command_dict['运行tf卡读写测试程序'])
time.sleep(5)
path = ser.logdir + ser.logname
avg_tf_test(path)
