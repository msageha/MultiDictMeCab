import os
import subprocess
from sys import version_info

import MeCab

class Tagger:
    def __init__(self, dicdir=subprocess.check_output(['mecab-config', '--dicdir']).decode('utf-8').strip()):
        self.dicdir = dicdir[-1] if dicdir[-1]=='/' else dicdir
        self.dictionaries = os.listdir(dicdir)
        self.taggerDict = {dic:MeCab.Tagger(f'-d {dicdir}/{dic}') for dic in self.dictionaries}
        [mecab.parse('') for mecab in self.taggerDict.values()]

    def parse(self, *args):
        pass

    def parseToNode(self, text):
        """与えられた文字列を形態素解析し、MeCabライクなイテレータnodeを返す
        MeCabとは異なり、戻り値はPythonのイテレータなのでwhileで使うときはnode.next()を呼び出す。
        その代わり、MeCabでは不可能であったPythonライクなfor文や内包表記をサポートしています。
        """
        text = text.strip()
        mecabNodesDict = {key:tagger.parseToNode(text).next for key, tagger in self.taggerDict.items()}
        nodesList = []
        while all(node for node in mecabNodesDict.values()):
            nodeTmpDictForNodesList = {key:Node() for key in self.dictionaries}
            surfaceSumLengthDict = {key:0 for key in self.dictionaries}
            maxSurfaceSumLength = -1
            while not all(i==maxSurfaceSumLength for i in surfaceSumLengthDict.values()):
                for key in self.dictionaries:
                    #TODO:::ここ上長な処理
                    node = nodeTmpDictForNodesList[key]
                    while node.next:
                        node = node.next
                    if node.totalLength == maxSurfaceSumLength:
                        continue
                    mecabNode = mecabNodesDict[key]
                    nextNode = Node(prevNode=node, surface=mecabNode.surface, feature=mecabNode.feature, _mecabNode=mecabNode)
                    node.next = nextNode
                    mecabNodeNext = mecabNode.next
                    mecabNodesDict[key] = mecabNodeNext
                    surfaceSumLengthDict[key] = nextNode.totalLength
                    maxSurfaceSumLength = max(surfaceSumLengthDict.values())
            nodesList.append(nodeTmpDictForNodesList)
        return nodesList

    def dictionary_info(self):
        pass


class Node:
    def __init__(self, prevNode=None, nextNode=None, surface='', feature='', _mecabNode=None):
        self.surface = surface
        self.feature = feature
        self.prev = prevNode
        self.next = nextNode
        self._mecabNode = _mecabNode
        totalLength = len(surface)
        if prevNode:
            totalLength += prevNode.totalLength
        self.totalLength = totalLength

    def totalLength(self):
        return self.totalLength

    def surface(self):
        return self.surface

    def feature(self):
        return self.feature

    def next(self):
        return self.next

    def prev(self):
        return self.prev
