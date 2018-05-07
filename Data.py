from Classes import *

sample_data = Data()
sample_data.g = {
        "a": Group(10), "b": Group(20), "c": Group(30),
        "d": Group(10), "e": Group(40)
    }

sample_data.p = {
        "mutaqi": Professor("Mutaqi"), "khalid": Professor("Khalid"),
        "zafar": Professor("Zafar"), "basit": Professor("basit"),
        "khalid_zaheer": Professor("Khalid Zaheer")
    }
sample_data.c = {
        "hu100": Course("HU100"), "mt111": Course("mt111"),
        "hu160": Course("hu160"), "ch110": Course("ch110"),
        "cs101": Course("cs101"), "cs152": Course("cs152"),
    }
sample_data.r = {
        "lt1": Room(20),
        "lt2": Room(40),
    }
sample_data.t = {
        "Mon08:30-10:00": Slot("08:30", "10:00", "Mon"),
        "Mon10:15-11:45": Slot("10:15", "11:45", "Mon"),
        "Mon12:00-13:30": Slot("12:00", "13:30", "Mon")
    }
