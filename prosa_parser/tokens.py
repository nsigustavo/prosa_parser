import re

def group(*choices): return '(' + '|'.join(choices) + ')'
def any(*choices): return group(*choices) + '*'
def maybe(*choices): return group(*choices) + '?'



class TokenError(Exception): pass

class SimpleToken(object):
    pseudomatch = None
    _len = 0
    def __init__(self, source, line_start, column_start):
        self.source = source
        self._end = [line_start, column_start]
        self._start = [line_start, column_start]

    def start(self):
        return self._start

    @classmethod
    def match(cls, source):
        if cls.regex.match(source):
            return cls

    def end(self):
        return self._end

    def __repr__(self):
        return type(self).__name__.upper()

    def tokenize(self):
        try:
            self.pseudomatch = match = self.regex.match(self.source)
            self._len = match.end()
            self._end[1] += self._len
            self.token = match.group()
        except Exception as e:
            raise TokenError("%r error: %s" %(self, str(e)))

        return self, self.token, self.start(), self.end()

    def rest_source(self):
        return self.source[len(self.token):]


    def evaluated(self):
        return self.token


class SimpleString(SimpleToken):
    tail_end_of_string = group(
        r"'[^'\\]*(?:\\.[^'\\]*)*'",
        r'"[^"\\]*(?:\\.[^"\\]*)*"')
    regex = re.compile(tail_end_of_string)

    @classmethod
    def match(cls, source):
        if source.startswith('"') or source.startswith("'"):
            return cls

    def evaluated(self):
        return eval(self.token)


class MultiLineString(SimpleToken):
    tail_end_of_multi_line_string = group(
        r"'''[^'\\]*(?:(?:\\.|'(?!''))[^'\\]*)*'''",
        r'"""[^"\\]*(?:(?:\\.|"(?!""))[^"\\]*)*"""')
    regex = re.compile(tail_end_of_multi_line_string)

    @classmethod
    def match(cls, source):
        if source.startswith('"""') or source.startswith("'''"):
            return cls

    def end(self):
        return [self._end[0]+len(self.token.split('\n'))-1,
                self._end[1]]

    def evaluated(self):
        return eval(self.token)

class Whitespace(SimpleToken):
    regex = re.compile(r'[ \f\t]+')


class LineEnd(SimpleToken):
    regex = re.compile(r'[\n]')

    def end(self):
        return [self._end[0]+1, 0]

    def rest_source(self):
        return self.source[1:]


class Word(SimpleToken):
    regex = re.compile('\S+(?<![\.\:\?\!\s])')


class EndOfTheSentence(SimpleToken):
    regex = re.compile('[\.\!\?](?=[ \f\t\n])')


class IndentDefinition(SimpleToken):
    regex = re.compile('[\:](?=[ \f\t\n])')


class PointFloat(SimpleToken):
    regex = re.compile(group(r'\d+\.\d+', r'\.\d+'))

    def evaluated(self):
        return float(self.token)


class IntNumber(SimpleToken):
    regex = re.compile(r'[1-9]\d*[lL]?')

    def evaluated(self):
        return int(self.token)


class Bracket(SimpleToken):
    regex = re.compile('[\]\[\(\)\{\}]')


class Variable(SimpleToken):
    regex = re.compile(r'\<[a-zA-Z_]\w*\>')


class Doctest(SimpleToken):
    regex = re.compile(r'''
        # Source consists of a PS1 line followed by zero or more PS2 lines.
        (?P<source>
            (?:^(?P<indent> [ ]*) >>>    .*)    # PS1 line
            (?:\n           [ ]*  \.\.\. .*)*)  # PS2 lines
        \n?
        # Want consists of any non-blank lines that do not start with PS1.
        (?P<want> (?:(?![ ]*$)    # Not a blank line
                     (?![ ]*>>>)  # Not a line starting with PS1
                     .*$\n?       # But any other line
                  )*)
        ''', re.MULTILINE | re.VERBOSE)

    re_match = re.compile(' *\>\>\> ')

    @classmethod
    def match(cls, source):
        if cls.re_match.match(source):
            return cls

    def end(self):
        return [self._end[0]+len(self.token.split('\n'))-1,
                self._end[1]]
    
