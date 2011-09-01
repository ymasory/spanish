#!/usr/bin/python3
#
# Usage: ./convert-words-to-flashup.py
# Output: words.flashup

from html.parser import HTMLParser
import io
import os
import os.path
import sys
from urllib.request import urlopen

LF = '\n'
url = 'http://wordsgalore.com/wordsgalore/languages/spanish/spanish1000.html'
urldir = os.path.dirname(url)

class MyParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.href = "href"
        self.anchor = "a"
        self.br = "br"
        self.wavfile = self.text = self.vocab = self.defn = ''
        self.items = []


    def handle_starttag(self, tag, attrs):
        if tag == self.anchor:
            self.text = ''
            attrs = dict(attrs)
            if self.href in attrs:
                self.wavfile = attrs[self.href]

        if tag == self.br:
            self.defn = self.text.strip()
            triple = (urldir + '/' + str(self.wavfile), self.vocab, self.defn)
            if not None in triple and not '' in triple:
                self.items.append(triple)


    def handle_endtag(self, tag):
        if tag == self.anchor:
            self.vocab = self.text.strip()
            self.text = ''

    
    def handle_data(self, data):
        self.text += data


def main():
    with urlopen(url) as handle:
        html = handle.read()
        html = html.decode('windows-1252')

    parser = MyParser()
    parser.feed(html)
    header = ('#GRAMMAR 1' + LF + '#TOPLEFT Common Spanish Words' + LF * 2)
    with open('spanish-words.flashup', 'w', encoding='utf-8') as out:
        out.write(header)

        for mp3, vocab, defn in parser.items:
            out.write('* ' + vocab + LF)
            out.write(defn + LF)
            out.write(LF)


if __name__ == '__main__':
    main()
