parse for writing specifications using plan text
================================================

::

    >>> from prosa_parser.parser import parse
    >>> from pprint import pprint
    >>> pprint(parse("""
    ... Feature: Manipulate strings.
    ...   In order to have some fun.
    ...   As a programming beginner.
    ...   I want to manipulate strings.
    ... 
    ...   Scenario: Uppercased strings.
    ...     Given i have the string "prosa leaves".
    ...     When i put it in upper case.
    ...     Then i see the string is "PROSA LEAVES".
    ... """))
    [['Feature', ':'],
     [['Manipulate', 'strings', '.'],
      ['In', 'order', 'to', 'have', 'some', 'fun', '.'],
      ['As', 'a', 'programming', 'beginner', '.'],
      ['I', 'want', 'to', 'manipulate', 'strings', '.'],
      ['Scenario', ':'],
      [['Uppercased', 'strings', '.'],
       ['Given', 'i', 'have', 'the', 'string', '"prosa leaves"', '.'],
       ['When', 'i', 'put', 'it', 'in', 'upper', 'case', '.'],
       ['Then', 'i', 'see', 'the', 'string', 'is', '"PROSA LEAVES"', '.']]]]
