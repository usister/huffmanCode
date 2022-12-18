import chardet
# 分析文本中字符频率，返回”字符：频率“的字典
def analysis(fileName):
    dict = {}  # 空字典，用于统计字符频率
    with open(fileName, "rb") as fileObj:
        line = fileObj.readline()
    with open(fileName, "r", encoding=chardet.detect(line)['encoding']) as fileObj:
        while True:
            word = fileObj.read(1)
            if not word: break  # 读到文件结尾就推出循环
            var = dict[word] if (word in dict) else 0
            dict[word] = var + 1
    return dict
dict = analysis("text.txt")
print(dict)