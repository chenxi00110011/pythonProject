import re
import socket
from scapy.layers.inet import Ether
from scapy.layers.l2 import ARP
from scapy.sendrecv import srp  # scapy 扫描局域网MAC地址
from my_decorator import *


def arp_scan(mac) -> dict:
    '''
    扫描局域网中的mac，返回符合输入mac的设备ip
    :param mac: 设备的mac，如果输入"ff:ff:ff:ff:ff:ff"，则返回子网中所有的存活设备
    :return: 字典类型，mac、ip映射表
    '''
    mac = str.lower(mac)
    local_ip = socket.gethostbyname(socket.gethostname())
    gateway_ip = re.sub(r'\d+$', '1', local_ip)
    ipscan = f'{gateway_ip}/24'
    arp_table = {}
    try:
        # log.info('dst=',mac,'pdst=',ipscan)
        ans, unans = srp(Ether(dst=mac) / ARP(pdst=ipscan), timeout=2, verbose=False)
        # log.info(ans, unans)
    except Exception as e:
        raise e
    else:
        for snd, rcv in ans:
            _mac = rcv.sprintf("%Ether.src%")
            ip = rcv.sprintf("%ARP.psrc%")
            arp_table[_mac] = ip
    return arp_table


def islive(mac) -> bool:
    # 扫描局域网，判断设备是否存活
    mac = str.lower(mac)
    times = 3
    while times > 0:
        if mac in arp_scan(mac):
            return True
        else:
            times -= 1
            time.sleep(3)
            continue
    return False

def get_ip(mac) -> str:
    # 扫描局域网，获取设备ip地址
    mac = str.lower(mac)
    return arp_scan(mac)[mac]


if __name__ == '__main__':
    print(get_ip("5A:5A:00:42:3A:79"))
    # print(d.islive("5A:5A:00:3F:34:4D"))
