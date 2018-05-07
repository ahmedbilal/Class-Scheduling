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


class Slot:
    def __init__(self, start, end, day):
        self.start = start
        self.end = end
        self.day = day


class Data:
    def __init__(self):
        self.g = dict()
        self.p = dict()
        self.c = dict()
        self.r = dict()
        self.t = dict()
