import chardet
from bitarray import bitarray


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


class Node:
    weight = 0
    value = ''
    left = None
    right = None


# 挑出字典中值最小的元素，转换成Node类型并返回，随后删除字典中的该元素
def getMinNode(dictionary: dict):
    node = Node()
    node.value = list(dict.items())[0]
    node.weight = list(dict.items())[1]
    for i, v in dict.items():
        if node.value > list(dict.items())[0]:
            node.value = list(dict.items())[0]
            node.weight = list(dict.items())[1]
    dict[node.value] = None
    return node


# 生成霍夫曼编码，接受一个频率字典，返回霍夫曼编码字典
def getHuffmanEncode(dictionary: dict):
    codeDict = {}  # 空字典，用于存储计算出的霍夫曼编码

    # 首先生成霍夫曼树
    temp = []  # 空list，保存最上层的结点
    while True:
        # 从字典中挑出两个频率最小的结点，插入到list
        for i in range(0, 1):
            if dict:
                temp.append(getMinNode(dict))
        # 从list中找两个频率最小的结点
        index1, index2 = 0, 1
        for i in range(2, 3):
            if temp[index1].weight > temp[i].weight:
                index2 = i
                continue
            elif temp[index2].weight > temp[i].weight:
                index2 = i

        # 处理结点,从下网上构建霍夫曼树
        newNode = Node()
        newNode.weight = temp[index1].weight + temp[index2].weight
        newNode.left = temp[index1]
        newNode.right = temp[index2]
        temp.append(newNode)
        del temp[index1]
        del temp[index2]
        # 循环到最后一次时，temp list中只会剩下1个元素，即为霍夫曼树的根
        if (len(temp)) == 1 and (not dict):
            break
    return temp[0]
    # 根据霍夫曼树计算霍夫曼编码
    stack = []  # 栈结构，方便先序遍历
    code = bitarray()

    curNode = temp[0]  # 从根结点开始遍历
    stack.append(curNode)  # 将根结点压入堆栈

    while True:
        if not stack:  # 栈空则遍历结束
            break
        if not (curNode.left and curNode.right):  # 处理叶子结点
            if curNode.value != '':  # 只处理原始树的叶子结点
                tmp = code  # 复制code数组
                codeDict[curNode.value] = tmp  # 完成单个字符的编码
            curNode = stack.pop()  # 弹出栈顶元素
            del code[len(code)]  # 路径回退
        if curNode.left:  # 处理有左结点的情况
            stack.append(curNode.left)  # 将左结点压入堆栈
            curNode.left = None  # 删除该左结点
            code.append(0)  # 记录路径
            continue
        if curNode.right:
            stack.append(curNode.right)
            curNode.right = None
            code.append(1)
            continue
    return codeDict


# 根据编码字典生成解码字典
def getHuffmanDecode(dcitionary: dict):
    reversedDict = {}
    for k, v in reversedDict.items():
        reversedDict[v] = k


bitA = bitarray()
for i in range(16):
    bitA.append(1)

with open("abc.bat", "wb") as file:
    file.write(bitA)
with open("abc.bat", "rb") as file:
    a = file.read(1)
    print(type(a))
    # a = bytes()
    # a.decode()
    print(bin(int(a.hex(), 16))[2])

if __name__ == '__main__':
    pass
