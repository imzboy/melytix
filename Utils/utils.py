
class NestedDict(dict):
    def __missing__(self, key):
        self[key] = NestedDict()
        return self[key]


def all_dict_paths(d):
    def iter(d, path):
        paths = []
        for k, v in d.items():
            if isinstance(v, dict):
                paths += iter(v, path + [k])
            else:
                paths.append((path + [k], v))
        return paths
    return iter(d, [])


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
