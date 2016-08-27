# coding=utf-8
from Node import Node, DoublyLinkedList


class DuplicateException(Exception):
    pass


class NotFoundException(Exception):
    pass


class FreqNode(DoublyLinkedList, Node):

    """Frequency node containing linked list of item nodes with
       same frequency."""

    def __init__(self, data):
        DoublyLinkedList.__init__(self)
        Node.__init__(self, data)

    def add_item_node(self, data):
        node = self.add_node(ItemNode, data)
        node.parent = self
        return node

    def insert_item_node(self, data, prev, next):
        node = self.insert_node(ItemNode, data, prev, next)
        node.parent = self
        return node

    def remove_item_node(self, node):
        self.remove_node(node)


class ItemNode(Node):

    def __init__(self, data):
        Node.__init__(self, data)
        self.parent = None


class LfuItem(object):

    def __init__(self, data, parent, node):
        self.data = data
        self.parent = parent
        self.node = node


class Cache(DoublyLinkedList):

    def __init__(self):
        DoublyLinkedList.__init__(self)
        self.items = dict()

    def insert_freq_node(self, data, prev, next):
        return self.insert_node(FreqNode, data, prev, next)

    def remove_freq_node(self, node):
        self.remove_node(node)

    def insert(self, key, value):
        if key in self.items:
            raise DuplicateException('Key exists')
        freq_node = self.head
        if not freq_node or freq_node.data != 1:
            freq_node = self.insert_freq_node(1, None, freq_node)

        freq_node.add_item_node(key)
        self.items[key] = LfuItem(value, freq_node)

    def access(self, key):
        try:
            tmp = self.items[key]
        except KeyError:
            raise NotFoundException('Key not found')

        freq_node = tmp.parent
        next_freq_node = freq_node.next

        if not next_freq_node or next_freq_node.data != freq_node.data + 1:
            next_freq_node = self.insert_freq_node(freq_node.data + 1,
                                                   freq_node, next_freq_node)
        item_node = next_freq_node.add_item_node(key)
        tmp.parent = next_freq_node

        freq_node.remove_item_node(tmp.node)
        if freq_node.count == 0:
            self.remove_freq_node(freq_node)

        tmp.node = item_node
        return tmp.data

    def delete_lfu(self):
        """Remove the first item node from the first frequency node.
        Remove the item from the dictionary.
        """
        if not self.head:
            raise NotFoundException('No frequency nodes found')
        freq_node = self.head
        item_node = freq_node.head
        del self.items[item_node.data]
        freq_node.remove_item_node(item_node)
        if freq_node.count == 0:
            self.remove_freq_node(freq_node)
