from math import ceil, log2

class Group:
    def __init__(self, size):
        self.size = size

class Professor:
    def __init__(self, name):
        self.name = name

class Course:
    def __init__(self, code):
        self.code = code

class Room:
    def __init__(self, size):
        self.size = size

g = { "a": Group(10), "b": Group(20), "c":Group(30),
      "d": Group(10), "e": Group(40)
    }
p = {
        "mutaqi": Professor("Mutaqi"), "khalid": Professor("Khalid"),
         "zafar": Professor("Zafar"), "javaid": Professor("Javaid"),
        "khalid_zaheer": Professor("Khalid Zaheer")
    }
c = {
        "hu100": Course("HU100"), "mt111": Course("mt111"),
        "hu160": Course("hu160"), "ch110": Course("ch110"),
        "cs101": Course("cs101")
    }
lts = {
        "lt1": Room(20),
        "lt2": Room(40),
        "lt3": Room(10)
    }

def bits_needed(x):
    return ceil(log2(len(x)))


def binary_converter(x):
    bit_repr = {}
    for c in range(len(x)):
        keys = list(x.keys())
        bit_repr[keys[c]] = (bin(c)[2:]).rjust(bits_needed(x), '0')
    return bit_repr

g_bin = binary_converter(g)
p_bin = binary_converter(p)
c_bin = binary_converter(c)
lts_bin = binary_converter(lts)

# print(g_bin, p_bin, c_bin)

cpg = [
        [c_bin["hu100"], p_bin["mutaqi"], g_bin["a"]],
        [c_bin["mt111"], p_bin["khalid"], g_bin["a"]],
        [c_bin["hu160"], p_bin["mutaqi"], g_bin["b"]],
        [c_bin["ch110"], p_bin["zafar"],  g_bin["c"]],
        [c_bin["cs101"], p_bin["javaid"], g_bin["e"]]

    ]

for i in range(len(cpg)):
    cpg[i] = "".join(cpg[i])


print(cpg)
