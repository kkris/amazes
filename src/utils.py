def isiterable(iterable):

    if isinstance(iterable, basestring):
        return False

    try:
        iter(iterable)
        return True
    except TypeError:
        return False

def flatten(iterable):

    for item in iterable:
        if isiterable(item):
            for item in flatten(item):
                yield item
        else:
            yield item
