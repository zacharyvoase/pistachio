import unittest

from pistachio.parser.lexer import lex

from fixtures import read_fixture


class TestLexer(unittest.TestCase):

    def test_complex_view(self):
        template = read_fixture('complex_view.mustache')
        lexed = read_fixture('complex_view.pyon')
        assert list(lex(template)) == lexed
