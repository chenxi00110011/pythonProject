import os
import re

from pymediainfo import MediaInfo
from environment_variable import adb_download


def getMp4Information(mp4Path):
    result = dict()
    media_info = MediaInfo.parse(mp4Path)
    data = media_info.to_json()
    data = eval(data)['tracks']

    for tracks in data:
        if tracks['track_type'] == 'Video':
            result['视频时长'] = tracks['other_duration'][0]
            result['分辨率'] = (tracks['width'], tracks['height'])

        elif tracks['track_type'] == 'General':
            result['视频帧率'] = eval(tracks['frame_rate'])
            result['平均码率'] = int(''.join(re.findall(r'\d+', tracks['other_overall_bit_rate'][0])))

        elif tracks['track_type'] == 'Audio':
            result['音频格式'] = tracks['format']

    return result


def get_gop(mp4_file):
    media_info = MediaInfo.parse(mp4_file)
    for track in media_info.tracks:
        if track.track_type == 'Video':
            print(track)
            print('GOP length:', track.menu('GOP').get('Format/Info'))

if __name__ == '__main__':
    mp4_file = 'C:\\Users\\Administrator\\Desktop\\video\\videos\\1.mp4'
    arguments = getMp4Information(mp4_file)
    print(arguments)