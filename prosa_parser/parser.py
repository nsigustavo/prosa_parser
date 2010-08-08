#!/usr/bin/env python
#-*- coding:utf-8 -*-

from prosa_parser.tokens import *


def lexical_analysis(source):
    source+='\n'
    line_start = column_start = 0
    while source:
        TokenType = (
               Doctest.match(source)
            or Whitespace.match(source)
            or MultiLineString.match(source)
            or SimpleString.match(source)
            or PointFloat.match(source)
            or IntNumber.match(source)
            or Word.match(source)
            or EndOfTheSentence.match(source)
            or IndentDefinition.match(source)
            or LineEnd.match(source)
            or None
            )
        if TokenType == None: raise SyntaxError('invalid syntax: line:%s' %(line_start))
            
        token = TokenType(source, line_start, column_start)
        if TokenType not in (LineEnd, Whitespace):
            yield  token.tokenize()
        else:
            token.tokenize()
        line_start, column_start =  token.end()
        source = token.rest_source()


class SyntacticAnalysis(object):

    def __init__(self, literal_source=None, simple_tokens=None):
        self.tokens = simple_tokens
        self.literal_source = literal_source

    def analyze(self):
        self.sentences = []
        self.sentence = []
        while self.tokens:
            self._generate_sentences()
        return self.sentences
    
    def _generate_sentences(self):
        token = self.tokens.pop(0)
        self.sentence.append(token)
        if isinstance(token[0], EndOfTheSentence):
            self.append_sentence()
            self.sentence = []
        if isinstance(token[0], IndentDefinition):
            self.indent_level = self.sentence[0][2][1]
            self.append_sentence()
            self.sentences.append(self.generate_block(self.tokens))
            self.sentence = []

    def append_sentence(self):
        self.sentences.append(
            SentenceToken(
                self.literal_source,
                self.sentence))

    def generate_block(self, tokens):
        tokens_block=[]
        while tokens and self.indent_level <= tokens[0][2][1]:
            token = self.tokens.pop(0)
            tokens_block.append(token)
        return SyntacticAnalysis(self.literal_source, tokens_block ).analyze()


class SentenceToken(object):

    def __init__(self, slicer_text, tokens):
        start, end  = tokens[0][2], tokens[-1][3]
        self.text = slicer_text.slice(start, end)
        self.line_start = tokens[0][1][0]
        self.tokens = tokens

    def __repr__(self):
        return repr([token[1] for token in self.tokens])

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, x):
        return self.tokens[x][1]


class LiteralSource:

    def __init__(self, source):
        self.source = source
        self.lines = source.split('\n')
    
    def slice(self, start, end):
        (line_start, column_start), (line_end, column_end) = start, end
        lines = self.lines[line_start:line_end+1]
        lines[-1] = lines[-1][:column_end]
        lines[0] = lines[0][column_start:]
        return '\n'.join(lines)

    def __repr__(self):
        return self.source


def parse(source):
    return SyntacticAnalysis(
            LiteralSource(source),
            list(lexical_analysis(source))
                ).analyze()


def conf_parse(source):
    return list(parse(source))[0]

