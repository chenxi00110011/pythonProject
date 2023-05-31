import os
import cv2


def get_image_properties_opencv(image_file):
    """
    使用 OpenCV 库读取图片属性。返回一个包含图片属性的字典。

    Args:
        image_file: 图片文件路径

    Returns:
        包含图片属性的字典
    """
    image = cv2.imread(image_file)
    height, width, channels = image.shape

    properties = {
        "size": f"{width}x{height}",
        "channels": channels
    }

    return properties


def get_all_image_properties(folder):
    """
    获取指定文件夹中所有图片的大小。

    Args:
        folder: 文件夹路径

    Returns:
        包含图片文件名和大小的字典列表
    """
    image_properties = []

    for filename in os.listdir(folder):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            file_path = os.path.join(folder, filename)
            properties = get_image_properties_opencv(file_path)
            properties["filename"] = filename
            image_properties.append(properties)

    return image_properties


if __name__ == '__main__':
    # 示例调用
    image_folder = 'C:\\Users\\Administrator\Desktop\\video\\screenshot'
    all_properties = get_all_image_properties(image_folder)
    print(all_properties)
