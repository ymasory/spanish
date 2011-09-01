#!/usr/bin/python3
#
# Convert into Flashup format the word list from
# Copy and paste the words in http://wordsgalore.com/wordsgalore/languages/spanish/spanish1000.html.
# The word list has been hand-modified with zz's to demarcate vocab items with
# multiple items.
#
# Usage: ./convert-words-to-flashup.py /path/to/words.txt
# Output: words.flashup

import os
import sys

def main():
    infile = os.path.abspath(sys.argv[1])
    LF = '\n'
    header = '#GRAMMAR 1\n#TOPLEFT Common Spanish Words'
    tmpfile =  infile + '.tmp'
    infiledir, infilename = os.path.split(infile)
    outfile = infiledir + os.sep + os.path.splitext(infilename)[0] + '.flashup'

    alldefs = set()
    with open(infile) as lines:
        with open(tmpfile, 'w') as out:
            for line in lines:
                if ' zz ' in line:
                    parts = line.split(' zz ')
                else:
                    parts = line.split(' ')
                out.write(parts[0] + '\t' + ' '.join(parts[1:]))

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
