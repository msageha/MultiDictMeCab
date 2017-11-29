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
        text = text.strip()
        mecabNodesDict = {key:tagger.parseToNode(text).next for key, tagger in self.taggerDict.items()}
        nodesList = []
        while all(node for node in mecabNodesDict.values()):
            nodeTmpDictForNodesList = {key:Node() for key in self.dictionaries}
            surfaceSumLengthDict = {key:0 for key in self.dictionaries}
            maxSurfaceSumLength = -1
            while not all(i==maxSurfaceSumLength for i in surfaceSumLengthDict.values()):
                for key in self.dictionaries:
                    #TODO:::ここ上長な処理．もう少し効率化したい
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

    # def totalLength(self):
    #     return self.totalLength

    # def surface(self):
    #     return self.surface

    # def feature(self):
    #     return self.feature

    # def next(self):
    #     return self.next

    # def prev(self):
    #     return self.prev

if __name__ == '__main__':
    text = input()
    multiDict = Tagger()
    nodes = multiDict.parseToNode(text)

    outputSurface = {key:[] for key in multiDict.dictionaries}
    outputFeature = {key:[] for key in multiDict.dictionaries}
    for nodeDic in nodes:
        for dic in multiDict.dictionaries:
            node = nodeDic[dic]
            while node:
                outputSurface[dic].append(node.surface)
                outputFeature[dic].append(node.feature)
                node = node.next
        length = max([len(i) for i in outputSurface.values()])
        for dic in multiDict.dictionaries:
            for i in range(length - len(outputSurface[dic])):
                outputSurface[dic].append('')
                outputFeature[dic].append('')

    #出力
    print('---surface---')
    for key in multiDict.dictionaries:
        print(f'{key}', end='\t')
    print()
    for i in range(length):
        for key in multiDict.dictionaries:
            print(f'{outputSurface[key][i]}', end='\t')
        print()

    print('---feature---')
    for key in multiDict.dictionaries:
        print(f'{key}\t feature ', end='\t')
    print()
    for i in range(length):
        for key in multiDict.dictionaries:
            print(f'{outputSurface[key][i]}\t{outputFeature[key][i]}', end='\t')
        print()

