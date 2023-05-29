import os
import re

from pymediainfo import MediaInfo
from environment_variable import adb_download


# media_info = MediaInfo.parse(adb_download+'IOTDBB-065896-UXLYD_2023_05_18_16_22_38_CH_1_deviceNametest_dev.mp4')
# data = media_info.to_json()
# data = eval(data)['tracks'][1]
# # print(data)
# for k in data.keys():
#     print(k,':',data[k])

def getMp4Information(mp4Path):
    result = dict()
    media_info = MediaInfo.parse(mp4Path)
    data = media_info.to_json()
    data1 = eval(data)['tracks'][1]
    result['视频时长'] = data1['other_duration'][0]
    result['分辨率'] = (data1['width'], data1['height'])
    data2 = eval(data)['tracks'][0]
    result['视频帧率'] = eval(data2['frame_rate'])
    result['平均码率'] =int(''.join(re.findall(r'\d+', data2['other_overall_bit_rate'][0])))
    result['码率控制方式'] = data2['overall_bit_rate_mode']
    return result


def get_gop(mp4_file):
    media_info = MediaInfo.parse(mp4_file)
    for track in media_info.tracks:
        if track.track_type == 'Video':
            print(track)
            print('GOP length:', track.menu('GOP').get('Format/Info'))

if __name__ == '__main__':
    # dir = adb_download + 'videos\\'
    # fileName = os.listdir(dir)[0]
    # arguments = getMp4Information(dir + fileName)
    # print(arguments)
    mp4_file = 'C:\\Users\\Administrator\\Desktop\\video\\videos\\超清.mp4'
    import cv2


    def count_i_frames(video_path):
        cap = cv2.VideoCapture(video_path)
        i_frame_count = 0
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == 0 or cap.get(cv2.CAP_PROP_POS_FRAMES) % cap.get(
                    cv2.CAP_PROP_GOP_SIZE) == 0:
                i_frame_count += 1
        cap.release()
        return i_frame_count


    video_path = mp4_file
    i_frame_count = count_i_frames(video_path)
    print("The number of I-frames in the video is:", i_frame_count)