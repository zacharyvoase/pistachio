from urecord import Record


class Template(list):
    """
    The abstract syntax tree of a fully parsed mustache template.

    Note that this class just contains the syntree, not the rendering logic.
    That's the compiler's job.
    """

    def __repr__(self):
        return 'Template(%s)' % list.__repr__(self)


class Section(Template):
    """A Mustache section."""

    def __init__(self, type, name, position, initial=None):
        self.type = type
        self.name = name
        self.position = position
        if initial is not None:
            super(Section, self).__init__(initial)
        else:
            super(Section, self).__init__()

    def __repr__(self):
        return 'Section(%r, %r, %r, %s)' % (
                self.type, self.name, self.position, list.__repr__(self))


class Token(Record('type', 'content', 'position')):
    """A token in a Mustache template."""
    pass
