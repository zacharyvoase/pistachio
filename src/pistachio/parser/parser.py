from urecord import Record

from pistachio.exceptions import SyntaxError
from pistachio.parser.syntax import Template, Section


def parse(tokens):
    result = Template()
    current = result
    stack = []
    for token in tokens:
        if token.type in ('section', 'inverted_section'):
            section = Section(*token)  # Token(type, content, position)
            current.append(section)
            stack.append(current)
            current = section
        elif token.type == 'close':
            if not isinstance(current, Section) or current.name != token.content:
                raise SyntaxError("Unmatched close tag: %r" % token.content, token.position)
            current = stack.pop()
        elif token.type == 'comment':
            pass
        else:
            current.append(token)
    return result


def unparse(tree):
    """Disassemble a fully-parsed tree back into a template string."""

    output = []
    for token in tree:
        if token.type == 'section':
            output.append('{{#%s}}%s{{/%s}}' % (token.name, unparse(token), token.name))
        elif token.type == 'inverted_section':
            output.append('{{^%s}}%s{{/%s}}' % (token.name, unparse(token), token.name))
        elif token.type == 'var':
            output.append('{{%s}}' % token.content)
        elif token.type == 'var_raw':
            output.append('{{&%s}}' % token.content)
        elif token.type == 'partial':
            # token.content is `(padding, partial_name)`.
            output.append('%s{{>%s}}' % token.content)
        elif token.type == 'text':
            output.append(token.content)
    return ''.join(output)
