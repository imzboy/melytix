

def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.subclasses():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return list(subclasses)
