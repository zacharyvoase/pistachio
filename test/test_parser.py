import unittest

from pistachio.parser.parser import parse
from pistachio.parser.syntax import Token

from fixtures import read_fixture


class TestParser(unittest.TestCase):

    def test_complex_view(self):
        lexed = map(lambda x: Token(*x), read_fixture('complex_view.pyon'))
        parsed = read_fixture('complex_view.pickle')
        assert parse(lexed) == parsed
