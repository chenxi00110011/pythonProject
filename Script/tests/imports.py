import os
import sys


# 将当前目录加入 sys.path 中
def add_path(path):
    # 确保路径存在
    if not os.path.exists(path):
        return

    # 将当前目录加入 sys.path 中
    sys.path.append(os.path.abspath(path))

    # 遍历子目录，将它们加入 sys.path 中
    for root, dirs, files in os.walk(os.path.abspath(path)):
        for dir in dirs:
            sys.path.append(os.path.join(root, dir))

# 将指定路径添加到 sys.path 中
add_path('../../../XrsPyTest\\')

from xrs_app import MobieProject
from xrs_mediainfo import getMp4Information
from environment_variable import adb_download
from xrs_serial import serial_bitstream
import pytest
import xrs_adb
import xrs_app
import image_properties

