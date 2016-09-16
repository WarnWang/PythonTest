import collections

d = {"one_int": 1, "two_int": 4, "sum_int": 2, "input_str": 0}

od = collections.OrderedDict(sorted(d.items(), key=lambda t: t[1]))

print od
print od["one_int"]
