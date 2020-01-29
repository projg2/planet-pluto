#!/usr/bin/env python3

import argparse
import configparser
import re


CAT_RE = re.compile(r'(category/|tag/|feeds?/|[?]feed=|rss).*$')


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('-o', '--output', default='planet.ini',
            type=argparse.FileType('w'),
            help='File to write config to')
    argp.add_argument('files', nargs='+',
            type=argparse.FileType('r'),
            help='Venus config files')
    args = argp.parse_args()

    inp = configparser.ConfigParser()
    outp = configparser.ConfigParser()
    for f in args.files:
        inp.read_file(f)
    for s in inp.sections():
        try:
            n = inp[s]['username']
        except KeyError:
            n = s
        outp.add_section(n)
        outp[n]['title'] = inp[s]['name']
        outp[n]['link'] = CAT_RE.sub('', s)
        outp[n]['feed'] = s

    args.output.write('title = Planet Gentoo (test)\n\n')
    outp.write(args.output)


if __name__ == '__main__':
    main()
