
length, cnt = raw_input('line 1: ').split(' ')


name = raw_input('name: ')


while True:
    xy = raw_input('x y:')
    if not xy:
        break

    x, y = str(xy).split(' ')

    if x == y:
        continue

    print x, y

    name = name.replace(x, '~Y~')
    name = name.replace(y, x)
    name = name.replace('~Y~', y)

print name
