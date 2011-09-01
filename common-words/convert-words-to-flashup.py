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

class FlashupWriter(HTMLParser):

    def __init__(self):
        super().__init__()
        self.header = ('#GRAMMAR 1' + LF + '#TOPLEFT Common Spanish Words' +
                       LF * 2)
        self.outfile = 'words.flashup'
        self.out = open(self.outfile, 'w')
        self.out.write(self.header)
        self.href = "href"
        self.anchor = "a"
        self.br = "br"
        self.wavfile = None
        self.vocab = "hola"
        self.defn = "hi"


    def handle_starttag(self, tag, attrs):
        if tag == self.anchor:
            attrs = dict(attrs)
            if self.href in attrs:
                self.wavfile = attrs[self.href]

        if tag == self.br:
            triple = (urldir + '/' + str(self.wavfile), self.vocab, self.defn)
            if not None in triple:
                mp3, voc, defn = triple
                self.out.write('* ' + voc + LF)
                self.out.write(defn + LF)
                self.out.write(LF)

    
    def finish(self):
        self.out.close()


class WavWriter(HTMLParser):

    def handle_starttag(self, tag, attrs):
        pass


def write_flashup(html):
    flashup_writer = FlashupWriter()
    flashup_writer.feed(html)


def write_wav(html):
    wav_writer = WavWriter()
    wav_writer.feed(html)


def main():
    with urlopen(url) as handle:
        html = handle.read()
        html = html.decode('windows-1252')

    write_flashup(html)
    write_wav(html)


if __name__ == '__main__':
    main()
