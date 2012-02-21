
def isiterable(iterable, include_strings=False, include_dicts=True):
    if isinstance(iterable, basestring):
        return include_strings
    if isinstance(iterable, dict):
        return include_dicts
    try:
        iter(iterable)
        return True
    except TypeError:
        return False

def flatten(iterable, n=None, level=0):
    """
    Flatten a list or tuple.
    If `n` is set, stop at level `n`.

    Returns a generator.
    """
    if n is not None and level >= n:
        # reached max. level, don't flatten anymore
        yield iterable
        return

    for item in iterable:
        if isiterable(item, include_dicts=False):
            for subitem in flatten(item, n=n, level=level+1):
                yield subitem
        else:
            yield item
