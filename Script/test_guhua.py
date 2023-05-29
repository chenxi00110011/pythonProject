import random
import time
import xrs_cgi

def generate_str()->str:
    asc_0_9 = [chr(i) for i in range(48,58)] # 0-9 ascii码
    asc_alphabet = [chr(i) for i in range(65,91)]+[chr(i) for i in range(97,123)]
    re_str = random.sample(asc_alphabet+asc_0_9,8)
    return ''.join(re_str)


if __name__ == "__main__":
    test_times = 10
    dev_ip ='192.168.123.157'
    for value in range(test_times):
        re_text = (F"\n"
                   F"<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
                   F"<CMDOTAuthInfo Version=\"1.0\">\n"
                   F"    <SerialNumber>M96608420314%06d</SerialNumber>\n"
                   F"    <CMDotSn>9660842000%06d</CMDotSn>\n"
                   F"    <BindCode>{generate_str()}</BindCode>\n"
                   F"    <Password>{generate_str()}</Password>\n"
                   F"    <CMDotCMEI_IMEI>111097200%06d</CMDotCMEI_IMEI>\n"
                   F"</CMDOTAuthInfo>\n")%(value,value,value)
        print(xrs_cgi.set_cmei(dev_ip,re_text))
        print(xrs_cgi.get_cmei(dev_ip))
        time.sleep(5)
