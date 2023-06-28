import os
import shutil


def clean_desktop():
    desktop_path = os.path.expanduser("~/Desktop")  # 获取桌面路径
    file_list = os.listdir(desktop_path)  # 获取桌面上的文件列表
    print(file_list)
    del_file = ['.bin', '.rar', '.log', '.xml', '.xlsx', '.mp4', '.xls', '.tmp', '.txt', '.png']
    move_file = ['.xmind', '.eddx']
    for filename in file_list:
        src = desktop_path + '/' + filename
        for def_flag in del_file:
            if def_flag in filename:
                os.remove(desktop_path+'/'+filename)  # 删除文件
        if '.lnk' in filename:
            dst = desktop_path+'/快捷键/'+filename
            shutil.move(src, dst)  # 移动文件
        for def_flag in move_file:
            if def_flag in filename:
                dst = desktop_path+'/流程图/'+filename
                shutil.move(src, dst)  # 移动文件
        if '.' not in filename and os.path.isfile(src):
            os.remove(desktop_path + '/' + filename)  # 删除文件
        if '.mpp' in filename:
            dst = desktop_path+'/计划/'+filename
            shutil.move(src, dst)  # 移动文件

clean_desktop()