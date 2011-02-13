def first_match(*iterators):
    """
    Become the first of the given iterators which yields anything.

        >>> i1 = iter([])
        >>> i2 = iter([])
        >>> i3 = iter([4, 9, 8])
        >>> i4 = iter([7, 6, 5])
        >>> list(first_match(i1, i2, i3, i4))
        [4, 9, 8]
    """
    for it in iterators:
        it = iter(it)
        try:
            yield it.next()
        except StopIteration:
            continue
        else:
            for item in it:
                yield item
            raise StopIteration
