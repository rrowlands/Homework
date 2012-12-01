# pprinttable.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
pprinttable: a function for prettier tabular output.
"""

def pprinttable(rows):
    """
    input: an iterable of namedtuples
    Print each item of each row in columnar format
    By MattH via http://stackoverflow.com/questions/5909873/python-pretty-printing-ascii-tables

    >>> from collections import namedtuple
    >>> Row = namedtuple('Row',['first','second','third'])
    >>> pprinttable([Row(1,2,3), Row(1234567,11,12)])
    first   | second | third
    --------+--------+------
          1 |      2 |     3
    1234567 |     11 |    12
    """

    headers = rows[0]._fields
    lens = []
    for i in range(len(rows[0])):
        lens.append(len(str(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x))))))
    formats = []
    hformats = []
    for i in range(len(rows[0])):
        if isinstance(rows[0][i], int):
            formats.append("%%%dd" % lens[i])
        elif isinstance(rows[0][i], float):
            formats.append("%%%df" % lens[i])
        else:
            formats.append("%%-%ds" % lens[i])
        hformats.append("%%-%ds" % lens[i])
    pattern = " | ".join(formats)
    hpattern = " | ".join(hformats)
    separator = "-+-".join(['-' * n for n in lens])
    print hpattern % tuple(headers)
    print separator
    for line in rows:
        print pattern % tuple(line)
