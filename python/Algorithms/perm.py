import copy
rst = list()


def perm(prefix, l):
    if len(l) == 1:
        print ','.join(['%s' % i for i in prefix + l])
    for i in l:
        tmp = list(l)
        tmp.remove(i)
        perm(prefix + [i], tmp)


if __name__ == '__main__':
    perm([],['a','b','c','d'])
