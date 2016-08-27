# Author: YiHan
# Date: 2015-11-16


class MaxPQ:

    def __init__(self,   list_a=None):
        if list_a:
            self._list = list(list_a)
        else:
            self._list = list()

    def isEmpty(self):
        if len(self._list) == 0:
            return True
        else:
            return False

    def size(self):
        return len(self._list)

    def _parent(self, i):
        if i == 0:
            return None

        return (i + 1) / 2 - 1

    def _left_child(self, i):
        idx = i * 2 + 1
        if idx >= self.size():
            return None

        return idx

    def _right_child(self, i):
        idx = i * 2 + 2
        if idx >= self.size():
            return None

        return idx

    def _exch(self, i, j):
        self._list[i], self._list[j] = self._list[j], self._list[i]

    # up
    def _swim(self, i):
        parent_idx = self._parent(i)

        while parent_idx is not None:

            if self._list[parent_idx] < self._list[i]:

                self._exch(parent_idx, i)

                i, parent_idx = parent_idx, self._parent(parent_idx)

            else:
                break

    # down
    def _sink(self, i):
        left_idx = self._left_child(i)
        right_idx = self._right_child(i)

        while left_idx is not None or right_idx is not None:
            if right_idx is None:
                bigger_idx = left_idx
            elif self._list[left_idx] > self._list[right_idx]:
                bigger_idx = left_idx
            else:
                bigger_idx = right_idx

            if self._list[bigger_idx] > self._list[i]:
                self._exch(bigger_idx, i)
                i, left_idx, right_idx = bigger_idx, self._left_child(
                    bigger_idx), self._right_child(bigger_idx)
            else:
                break

    def insert(self, value):
        self._list.append(value)
        self._swim(self.size() - 1)

    def del_max(self):
        self._exch(0, self.size() - 1)
        value = self._list.pop()
        self._sink(0)
        return value

    def max(self):
        self._list[0]


def main():
    mq = MaxPQ()
    mq.insert(20)
    mq.insert(40)
    mq.insert(21)
    mq.insert(42)
    mq.insert(23)
    mq.insert(44)
    mq.insert(482)
    mq.insert(25)
    mq.insert(46)
    mq.insert(27)
    mq.insert(481)

    print mq._list

    for i in range(mq.size()):
        m = mq.del_max()
        print m
        # print mq._list


if __name__ == '__main__':
    main()
