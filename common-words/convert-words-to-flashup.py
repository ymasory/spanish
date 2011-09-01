#!/usr/bin/python3
#
# Usage: ./convert-words-to-flashup.py
# Output: words.flashup

import os
import sys
import tempfile as tempfilemodule
from urllib.request import urlopen

def main():
    LF = '\n'
    url = ('http://wordsgalore.com/wordsgalore/languages/spanish/' +
           'spanish1000.html' )
    header = '#GRAMMAR 1\n#TOPLEFT Common Spanish Words'
    tmpfile =  tempfilemodule.mkstemp()[1]
    outfile = 'words.txt'

    html = urlopen(url).read()
    print(html)
    sys.exit()

    with open(tmpfile) as lines:
        with open(outfile, 'w') as out:
            out.write(header.strip() + LF * 2)
            for line in lines:
                if line not in alldefs:
                    word, definition = line.split('\t')
                    out.write('* ' + word + LF)
                    out.write(definition + LF)
                else:
                    print('ignoring duplicate ' + word)
                alldefs.add(line)
    print('successfully created ' + outfile)
    os.remove(tmpfile)

if __name__ == '__main__':
    main()
