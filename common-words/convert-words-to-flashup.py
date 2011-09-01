#!/usr/bin/python3
#
# Usage: ./convert-words-to-flashup.py
# Output: words.flashup

from html.parser import HTMLParser
import io
import os
import os.path
import sys
import time
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

        for mp3url, vocab, defn in parser.items:
            out.write('* ' + vocab + LF)
            out.write(defn + LF)
            out.write(LF)

    mp3urls = [trip[0] for trip in parser.items]
    assert len(mp3urls) == len(set(mp3urls))
    mp3dir = 'mp3s'
    if not os.path.exists(mp3dir):
        os.mkdir(mp3dir)
    for mp3url in mp3urls:
        fname = mp3dir + os.sep + os.path.basename(mp3url)
        with open(fname, 'wb') as out:
            with urlopen(mp3url) as handle:
                out.write(handle.read())
                print('downloaded ' + mp3url)
                time.sleep(5) #being friendly


if __name__ == '__main__':
    main()
