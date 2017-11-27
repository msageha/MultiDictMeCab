import os
import subprocess
from sys import version_info

import MeCab

class Tagger(object):
    def __init__(self, dicdir=None): 
        self.dicdir = dicdir[-1] if dicdir[-1]=='/' else dicdir
        self.dictionaries = os.listdir('/usr/local/mecab/lib/mecab/dic')
        self.dic_num = len(dictionaries)
        self.taggerDict = {dic:MeCab.Tagger(f'-d {dicdir}/{dic}') for dic in self.dictionaries}

    def parse(self, *args):
        pass

    def parseToNode(self, text):
        """与えられた文字列を形態素解析し、MeCabライクなイテレータnodeを返す
        MeCabとは異なり、戻り値はPythonのイテレータなのでwhileで使うときはnode.next()を呼び出す。
        その代わり、MeCabでは不可能であったPythonライクなfor文や内包表記をサポートしています。 
        """
        text = text.strip()
        nodesDict = {key:tagger.parseToNode(text) for key in taggerDict}
        NodeList = []
        while True:
            nodeTmpDict = {key:{'surface':[], 'feature':[], 'wordLength':0}  for key in self.dictionaries}
            surfaceLengthList = [len(value['wordLength']) for value in nodeTmpDict]
            maxSurfaceLength = -1
            while all(i==maxSurfaceLength for i in surfaceLengthList):
                for i, key in enumerate(nodesDict):
                    if nodeTmpDict[key]['wordLength'] == maxSurfaceLength:
                        continue
                    nodeTmpDict[key]['surface'].append(nodesDict[key].surface)
                    nodeTmpDict[key]['feature'].append(nodesDict[key].feature)
                    

        return _MeCab.Tagger_parseToNode(self, *args)

    def dictionary_info(self):
        pass

# class Node(object):
#     def __init__():
#         pass

#     def next():
#         pass

#     def prev():
#         pass
