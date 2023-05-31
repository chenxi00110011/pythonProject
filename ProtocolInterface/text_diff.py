import difflib


def read_file(filepath):
    """读取文件内容"""
    with open(filepath, "r") as file:
        file_content = file.read()
    return file_content


def compare_text(text1, text2):
    """比较两个文本，返回差异的行"""
    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
    return '\n'.join(line for line in diff if line.startswith('+ ') or line.startswith('- '))


def compare_files(file1, file2):
    """比较两个文件，返回差异的行"""
    text1 = read_file(file1)
    text2 = read_file(file2)
    return compare_text(text1, text2)


if __name__ == '__main__':
    # 比较两个文件
    file1_path = "C:\\Users\\Administrator\\Desktop\\video\\texts\\text1.txt"
    file2_path = "C:/Users/Administrator/Desktop/video/texts/text2.txt"
    diff = compare_files(file1_path, file2_path)
    print(diff)