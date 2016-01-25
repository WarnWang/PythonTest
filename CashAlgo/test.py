import collections

d = {"a": 1, "b": 4, "c": 2, "d": 0}

od = collections.OrderedDict(sorted(d.items(), key=lambda t: t[1]))

print od
print od["a"]
