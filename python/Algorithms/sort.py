'''sort base class'''
import random
import time

LIST_A = list()
for i in range(10000):
    LIST_A.append(random.randint(1, 100))


class TimeIt(object):

    def __init__(self):
        pass

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            begin = time.time()
            fn(*args, **kwargs)
            end = time.time()
            print 'Time:' + str(end - begin)
        return wrapped


class BaseSort(object):

    '''BaseSort'''

    @classmethod
    def prepare_list(cls):
        '''prepare_list'''

        return LIST_A

    def sort(self, list_a):
        '''sort'''
        raise NotImplementedError

    @classmethod
    def exch(cls, list_a, i, j):
        '''exch'''
        tmp = list_a[i]
        list_a[i] = list_a[j]
        list_a[j] = tmp

    @classmethod
    def show(cls, list_a):
        '''show'''
        print list_a

    @classmethod
    def is_sorted(cls, list_a):
        '''is_sorted'''
        for i in range(1, len(list_a)):
            if list_a[i] < list_a[i - 1]:
                return False

        return True

    def main(self):
        '''main'''
        list_a = []
        list_a = self.prepare_list()
        self.sort(list_a)
        assert self.is_sorted(list_a)
        # self.show(list_a)


class SelectSort(BaseSort):

    '''TestSort'''
    @TimeIt()
    def sort(self, list_a):
        length = len(list_a)
        if length == 0:
            return

        for i in range(0, length):
            min_value = list_a[i]
            min_index = i
            for j in range(i, length):
                if min_value <= list_a[j]:
                    pass
                else:
                    min_value = list_a[j]
                    min_index = j

            self.exch(list_a, i, min_index)


class InsertionSort(BaseSort):

    '''InsertionSort'''
    @TimeIt()
    def sort(self, list_a):
        length = len(list_a)
        if length == 0:
            return

        for i in range(1, length):
            key = list_a[i]
            index = i
            for j in range(0, i):  # find insert index
                if list_a[j] > list_a[i]:
                    index = j
                    break
            for k in range(i, index, -1):
                list_a[k] = list_a[k - 1]

            list_a[index] = key


class InsertionSort2(BaseSort):

    '''InsertionSort'''
    @TimeIt()
    def sort(self, list_a):
        length = len(list_a)
        if length == 0:
            return

        for i in range(1, length):
            for k in range(i, 0, -1):
                if list_a[k] < list_a[k - 1]:
                    self.exch(list_a, k, k - 1)
                else:
                    break


class ShellSort(BaseSort):

    '''ShellSort'''
    @TimeIt()
    def sort(self, list_a):
        length = len(list_a)
        if length == 0:
            return

        h = 1
        while h < length / 3:
            h = 3 * h + 1

        while h >= 1:
            for i in (0, h):
                for i in range(i, length, h):
                    for k in range(i, 0, -1 * h):
                        if list_a[k] < list_a[k - 1]:
                            self.exch(list_a, k, k - h)
                        else:
                            break
            h = h / 3


class ShellSort2(BaseSort):

    '''ShellSort2'''
    @TimeIt()
    def sort(self, list_a):
        length = len(list_a)
        if length == 0:
            return

        h = 1
        while h < length / 3:
            h = 3 * h + 1

        while h >= 1:
            for i in range(h, length):
                for k in range(i, 0, -1):
                    if list_a[k] < list_a[k - h]:
                        self.exch(list_a, k, k - h)
                    else:
                        break

            h = h / 3


if __name__ == '__main__':
    for sort in (SelectSort(), InsertionSort(), InsertionSort2(),
                 ShellSort(), ShellSort2()):
        sort.main()
        pass
