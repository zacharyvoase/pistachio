import re

from strscan import Scanner
from calabash import source

from pistachio.exceptions import LexerError
from pistachio.parser.syntax import Token
from pistachio.utils import first_match


TAG_TYPES = {
    '#': 'section',
    '^': 'inverted_section',
    '/': 'close',
    '!': 'comment',
    '=': 'set_tags',
    '>': 'partial',
    '<': 'partial',
    '{': 'var_raw',
    '&': 'var_raw',
    '': 'var',
}

TAG_TYPE_RE = re.compile('[%s]' % ''.join(map(re.escape, TAG_TYPES.keys())))
TAG_CONTENT_RE = re.compile(r'([\w\?\!\/\-])*')

# These types of tags allow any content; the rest only allow
# `ALLOWED_CONTENT`.
ANY_CONTENT_TAGS = ('!', '=')


@source
def lex(template, open_tag='{{', close_tag='}}'):
    """Lex a Mustache template string."""
    scanner = Scanner(template)
    grammar = {'open_tag': open_tag, 'close_tag': close_tag}
    while not scanner.eos():
        for item in first_match(_scan_tags(scanner, grammar), _scan_text(scanner, grammar)):
            yield item


@source
def _scan_tags(scanner, grammar):
    # Open tag
    open_tag = scanner.scan(re.escape(grammar['open_tag']))
    if not open_tag:
        raise StopIteration
    tag_pos = scanner.prev
    tag_type = scanner.scan(TAG_TYPE_RE) or ''
    scanner.skip(r'\s*') # Skip arbitrary whitespace after the open tag.

    # Tag content
    if tag_type in ANY_CONTENT_TAGS:
        # Just scan until we see the close of the tag, regardless of what's
        # inside it.
        content = scanner.scan_upto(r'\s*%s?%s' % (re.escape(tag_type), re.escape(grammar['close_tag'])))
    else:
        content = scanner.scan(TAG_CONTENT_RE)
    if not content:
        raise LexerError[scanner]("Illegal content in %r tag" % TAG_TYPES[tag_type])

    new_grammar = None
    if tag_type == '=':
        # Grammar re-definition (set delimiters instruction)
        new_open_tag, new_close_tag = content.split(' ', 1)
        new_grammar = {'open_tag': new_open_tag, 'close_tag': new_close_tag}
    else:
        yield Token(type=TAG_TYPES[tag_type], content=content, position=tag_pos)

    # Close tag.
    scanner.skip(r'\s*')
    if tag_type == '{':
        # Triple mustache special case.
        scanner.skip(r'}')
    elif tag_type:
        # Means that we parse {{#tag#}} the same as {{#tag}}.
        scanner.skip(re.escape(tag_type))
    tag_close = scanner.scan(re.escape(grammar['close_tag']))
    if not tag_close:
        raise LexerError[scanner]("Unclosed tag (expected: %r)" % grammar['close_tag'])

    # If this tag has re-defined the grammar, update the shared grammar object.
    if new_grammar:
        grammar.update(new_grammar)


@source
def _scan_text(scanner, grammar):
    pos = scanner.pos
    text = scanner.scan_upto(re.escape(grammar['open_tag']))
    if text is None:
        text = scanner.rest
        scanner.terminate()
    yield Token(type='text', content=text, position=pos)
