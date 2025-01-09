import sys
import chardet
from bitarray import bitarray
import pickle
import os
import copy

# 分析文本中字符频率，返回”字符：频率“的字典
def analysis(fileName):
    '''
    分析文件的字符频率
    :param fileName: 文件名
    :return: 字符频率字典
    '''
    nodeDict = {}  # 空字典，用于统计字符频率
    with open(fileName, "rb") as fileObj:
        line = fileObj.readline()
    with open(fileName, "r", encoding=chardet.detect(line)['encoding']) as fileObj:
        while True:
            word = fileObj.read(1)
            if not word: break  # 读到文件结尾就推出循环
            var = nodeDict[word] if (word in nodeDict) else 0
            nodeDict[word] = var + 1
    # 增加'EOF'标志，表示压缩文件末尾
    nodeDict['EOF'] = 1
    return nodeDict


class Node:
    weight = 0
    value = ''
    left = None
    right = None



# 生成霍夫曼编码，接受一个频率字典，返回霍夫曼编码字典
def getHuffmanEncode(frequencyDict)->dict:
    '''
    根据字符频率生成霍夫曼编码
    :param frequencyDict: 字符频率
    :return: 霍夫曼编码字典
    '''
    rootNode = constructHuffmanTree(frequencyDict)
    stack = [] #栈结构缓存路径中的结点
    codeDict ={} # 字典，记录每个字符对应的的哈夫曼编码
    visitedNode = set() #集合，记录所有访问过的结点
    code = bitarray()#位数组，记录路径信息，即最终的哈夫曼编码
    stack.append(rootNode)
    while stack:
        curNode = stack[-1]
        visitedNode.add(curNode)
        if curNode.left and not (curNode.left in visitedNode):
            stack.append(curNode.left)
            code.append(0)
        elif curNode.right and not (curNode.right in visitedNode):
            stack.append(curNode.right)
            code.append(1)
        elif (not curNode.left) and (not curNode.right):
            codeDict[curNode.value]=bitarray(code.to01())
            stack.pop()
            code.pop()
        else:
            if len(code)>0: code.pop()      # 防止根结点弹出时产生溢出
            stack.pop()
    return codeDict
def constructHuffmanTree(nodeDict:dict)->Node:
    '''
    根据字符频率字典生成霍夫曼树
    :param nodeDict: 字符频率字典
    :return: 霍夫曼树的根
    '''
    # 首先生成霍夫曼树
    temp = []  # 空list，用于缓存哈夫曼树的结点
    # 根据字典创建结点对象
    for i,v in nodeDict.items():
        node = Node()
        node.value = i
        node.weight = v
        temp.append(node)
    while True:
        # 循环到最后一次时，temp list中只会剩下1个元素，即为霍夫曼树的根
        if (len(temp)) == 1 :
            break
        # 从list中找两个频率最小的结点
        index1, index2 = 0, 1
        for i in range(2, len(temp)):
            if temp[index1].weight > temp[i].weight:
                index2 = i
                continue
            elif temp[index2].weight > temp[i].weight:
                index2 = i

        # 处理结点,从下往上构建霍夫曼树
        newNode = Node()
        newNode.weight = temp[index1].weight + temp[index2].weight
        newNode.left = temp[index1]
        newNode.right = temp[index2]
        temp.append(newNode)

        i1 = index1 if index1 < index2 else index2
        i2 = index2 if index1 < index2 else index1
        del temp[i2]
        del temp[i1]
    return temp[0]

# 根据编码字典生成解码字典
def getHuffmanDecode(nodeDict:dict):
    reversedDict = {}
    for i in nodeDict.items():
        k,v=i
        reversedDict[v.to01()] = k
    return reversedDict

def getFileEncoding(fileName:str)->str:
    with open(fileName, "rb") as fileObj:
        line = fileObj.read()
    return chardet.detect(line)['encoding']

'''try:'''
if sys.argv[1] == '-c':  # 压缩文件
    fileName = sys.argv[2]                  #读取要压缩的文件名
    frequencyDict = analysis(fileName)      #分析文件字符频率
    codeDict = getHuffmanEncode(frequencyDict)  #根据字符频率创建字典
    # 获取原文件编码格式
    fileEncoding = getFileEncoding(fileName)
    # 创建解码字典文件，储存解码信息
    with open(fileName + "-code", "wb") as newFile:
        decodeDict = getHuffmanDecode(codeDict)
        decodeDict['encoding'] = fileEncoding
        pickle.dump(decodeDict,newFile)
    # 打开原文件
    with open(fileName, "r", encoding=fileEncoding) as fileObj:
        # 创建压缩文件
        with open(fileName+"-compressed","wb") as newFile:
            hexCode = bitarray()  # 写入缓存，每满一字节写入一次
            while True:
                # 每次读取一个字符
                chr = fileObj.read(1)
                # 处理文件末尾
                if not chr:
                    if len(hexCode) ==0 :
                        newFile.write(codeDict['EOF'])
                    else:
                        newFile.write(hexCode+codeDict['EOF'][:8-len(hexCode)])
                        newFile.write(codeDict['EOF'][8-len(hexCode):])
                    break
                code = copy.copy(codeDict[chr])
                for i,v in enumerate(code):
                    if len(hexCode)==8:
                        newFile.write(hexCode)  # 将缓存写入文件
                        hexCode.clear()         # 清空写入缓存
                    hexCode.append(v)       # 将code的数据逐位压入缓存
    print("压缩完成！")
# 解压部分
elif sys.argv[1] == '-x':
    fileName = sys.argv[2]  # 获取待解压的文件名
    codeDictFileName = sys.argv[3]  # 获取字典文件名
    decodeDict = {}
    with open(codeDictFileName,'rb') as f:
        decodeDict = pickle.load(f)    #读取解码字典
    # 解压文件
    with open(fileName,'rb') as compressedFile:         # 打开压缩文件
        with open(fileName + '-uncompressed', 'w', encoding=decodeDict['encoding']) as uncompressedFile:    # 创建解压文件
            code=''
            while True:
                tmp = compressedFile.read(1)      # 一次读一字节
                if not tmp: break                 # 读取到压缩文件结尾则返回
                key = format(int(tmp.hex(),16),'#010b')[2:]           # 转换成字符串表示的二进制
                for i,v in enumerate(key):
                    code = code + v
                    if code in decodeDict.keys():
                        if decodeDict[code] == 'EOF': break     #读到'EOF'标志则结束
                        uncompressedFile.write(decodeDict[code])
                        code = ''
    print("解压完成！")
'''except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(e, exc_type, fname, exc_tb.tb_lineno)
    print("Error please using \"{0} -c filename\" to comprise a txt file, or using\"{0} -x filename decodeDictFile\" to uncomprise a compressed file".format(sys.argv[0]))'''