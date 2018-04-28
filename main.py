def whichGroup(groups, classes):
    try:
        index = groups.index(classes)
        return index
    except ValueError:
        groups.append(classes)
        return len(groups) - 1


groups = [["CS101", "MECH101", "ENM201"], ["CS201", "MECH101", "ENM201"]]

whichGroup(groups, classes)
