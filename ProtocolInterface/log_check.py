import os
import re
import data_store
import xrs_time


class ObtainLog:
    '''
    关键字数据读取
    给日志添加标记（时间戳）
    依据标记读取日志
    日志打包存储
    日志上传服务器
    日志的关键字检查
    '''

    def __init__(self, com, dir):
        self.com_port = com
        self.dir = dir

    def searchLog(self, saveMode='only'):
        # 搜索日志
        # mode为'only'时，仅返回最新日期的日志列表
        # mode为'day'时，仅返回昨天和今天的日志列表
        file_list = []
        for file in os.listdir(dir):
            if self.com_port in file:
                file_list.append(file)
        if saveMode == 'only':
            return self.find_newest(file_list, saveMode='only')
        elif saveMode == 'day':
            return self.find_newest(file_list, saveMode='day')
        else:
            raise ValueError("输入参数错误")

    def find_newest(self, list, saveMode='only'):
        # 内部方法
        # 辅助searchLog方法，遍历文件列表，生成日期与文件的字典，以及找到最新日期
        # 根据模式返回最新日期还是昨天今天的日志列表
        file_d = {}
        date_max = 0
        for name in list:
            # print(name)
            timeRegex1 = re.compile("\d{4}-\d{1,2}-\d{1,2}")
            date_s = re.findall(timeRegex1, name)[0]
            if date_s in file_d.keys() and file_d[date_s]:
                file_d.update({date_s: file_d[date_s] + [name]})
            else:
                file_d[date_s] = [name]
            date_s = xrs_time.convert_to_timestamp(date_s)
            if date_s > date_max:
                date_max = date_s
            # print(file_d)
        # print(date_max)
        date_max = xrs_time.returnDate(date_max, "%Y-%m-%d")
        if saveMode == "only":
            result = file_d[date_max]

        elif saveMode == "day":
            result = file_d[xrs_time.today(-1)] + file_d[xrs_time.today()]
        else:
            raise Exception("输入参数错误")
        print(result)
        return result

    def readLog(slef, file_list) -> list:
        '''
        :param dir:日志所在文件夹
        :param file_list: 日志名称列表，一般是最新日期或者昨天今天。目前是默认排序的
        :return: 根据上一次标记来返回日志
        '''
        log_list = []
        for name in file_list:
            log_path = slef.dir + name
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as read_log:
                log_text = read_log.read()
            log = log_text.split('\n')
            log_list += log
        log_flag = log_list[-2]
        print(log_flag)
        last_log_flag = data_store.readToFile()[com][-1]
        data_store.writeToFile(com, log_flag)
        if log_list.count(last_log_flag):
            last_index = log_list.index(last_log_flag)
        else:
            last_index = 0
        print(last_index)
        return log_list[last_index:]


class AuditLog:

    def __init__(self, keyword_d, model):
        # 导入关键字的表格,
        self.model = model
        if self.model in keyword_d.keys():
            self.keyword_d = keyword_d[self.model]
        else:
            raise Exception("初始化错误，keyword_d文件不包含该版型")


    def logCheck(self, log_l):
        keyword_return = dict()
        for keyword,value in self.keyword_d.items():
            keyword_return[keyword] = []
            for log_h in log_l:
                if value in log_h:
                    date_s = xrs_time.logToDate(xrs_time.dict_re['date_ymdhms'],log_h)
                    keyword_return[keyword] = keyword_return[keyword]+[date_s]
        return keyword_return




if __name__ == "__main__":
    keyword_d = {
        '版型A': {
            '重启': 'U-Boot SPL 2013.07'
        }
    }
    com = 'COM35'
    dir = "C:\\Users\\Administrator\\AppData\\Roaming\\NetSarang\\5\\Xshell\\Logs\\"
    log = 'C:\\Users\\Administrator\\AppData\\Roaming\\NetSarang\\5\\Xshell\Logs\\COM35_2023-04-27_15-42-39.log'
    excel_url = "C:\\Users\\Administrator\\Desktop\\kaoji.xlsx"
    ob = ObtainLog(com, dir)
    file_list = ob.searchLog(saveMode="only")
    log_l = ob.readLog(file_list)
    print(data_store.readToFile())
    au = AuditLog(keyword_d,model='版型A')
    err_d = au.logCheck(log_l)
    print(err_d)
    data_store.data_d['异常'] = err_d
    # data_store.write_dict(excel_url,data_store.data_d['异常'])
    data_store.tabulation_write(excel_url,'C3',err_d)
