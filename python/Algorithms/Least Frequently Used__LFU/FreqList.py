# coding=utf-8
from Node import Node, DoublyLinkedList


class LFUNode(Node):

    def __init__(self, data):
        self.dataList = DoublyLinkedList()
        Node.__init__(self, data)


class LFUItem(Node):

    def __init__(self, data):
        Node.__init__(self, data)
        self.parent = None


# Cache Object
class LFUList(DoublyLinkedList):

    def __init__():
        pass
