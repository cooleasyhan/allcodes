# coding=utf-8


class Node(object):

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList(object):

    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def add_node(self, cls, data):
        return self.insert_node(cls, data, self.tail, None)

    def insert_node(self, cls, data, prev, next):
        node = cls(data)
        node.prev = prev
        node.next = next

        if prev:
            prev.next = node
        if next:
            next.prev = node

        if prev is self.tail or not self.tail:
            self.tail = node

        if next is self.head or not self.head:
            self.head = node

        self.count += 1

        return node

    def remove_node(self, node):
        if node is self.tail:
            self.tail = node.prev
        else:
            node.next.prev = node.prev

        if node is self.head:
            self.head = node.next
        else:
            node.prev.next = node.next

        self.count += 1

    def get_nodes_data(self):
        data = list()
        node = self.head
        while node:
            data.append(node.data)
            node = node.next

        return data


def main():
    link_list = DoublyLinkedList()
    link_list.add_node(Node, '1')

    link_list.add_node(Node, '2')
    node = link_list.add_node(Node, '3')
    node2 = link_list.add_node(Node, '4')
    link_list.insert_node(Node, '44', node, node2)
    link_list.add_node(Node, '5')

    link_list.add_node(Node, '1')

    link_list.add_node(Node, '2')
    node = link_list.add_node(Node, '3')
    node2 = link_list.add_node(Node, '4')
    node3 = link_list.insert_node(Node, '44', node, node2)
    link_list.add_node(Node, '5')

    link_list.remove_node(node3)

    print link_list.get_nodes_data()

if __name__ == '__main__':
    main()
