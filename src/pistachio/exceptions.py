"""Common exceptions used throughout Pistachio."""


class ParserError(Exception):
    """An exception somewhere in the Mustache parser."""

    # This means `__getitem__()` will be defined on the error class itself.
    class __metaclass__(type):
        def __getitem__(cls, scanner):
            """
            Create an error shortcut callback for a :class:`strscan.Scanner`.

            This method makes it quicker to raise an error given a scanner::

                >>> from strscan import Scanner
                >>> s = Scanner("test string")
                >>> s.skip("test")
                4
                >>> ParserError[s]('Message goes here')
                Traceback (most recent call last):
                ...
                ParserError: [@4] Message goes here
            """
            def error(msg):
                raise cls(msg,
                        position=scanner.coords(),
                        source=scanner.string)
            return error

    def __init__(self, msg, position=None, source=None):
        self.msg = msg
        self.position = position
        self.source = source

    def __str__(self):
        if isinstance(self.position, tuple):
            return "%s\n[line:%d col:%d] %s" % (self.msg,) + self.position
        elif isinstance(self.position, (int, long)):
            return "[@%d]: %s" % (self.position, self.msg)
        else:
            return self.msg


class LexerError(ParserError):
    """An error in lexing/tokenizing the input stream."""
    pass


class SyntaxError(ParserError):
    """An error in the syntax of a Mustache template."""
    pass
