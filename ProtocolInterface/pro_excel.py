import xlrd




def get_dev_info(url) ->dict:
    data = xlrd.open_workbook(url)
    table = data.sheet_by_index(0)
    dev_info = {}
    devices = {}
    for i in range(1,table.nrows):
        dev_info['dev_mac'] = table.row(i)[1].value.split()
        dev_info['test_time'] = table.row(i)[2].value.split()
        dev_info['check_point'] = table.row(i)[3].value.split()
        devices[table.row(i)[0].value] = dev_info
    return devices

url = 'C:\\Users\\Administrator\\Desktop\\dev_info.xlsx'
get_dev_info(url)