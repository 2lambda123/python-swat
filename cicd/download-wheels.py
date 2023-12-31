#!/usr/bin/env python

'''
Download Wheel files from URL

Wheel files may be stored in a staging area before being published to the
public PyPI repository. This is done so that new packages can be tested
before being published officially.

This utility allows you to download a set of wheel files from a repository
(optionally specifying a specific version of the package) and storing
them in a local directory. They can then be uploaded to the final location
using `twine`.

'''

import argparse
import os
import re
import sys
from urllib.parse import urljoin
from urllib.request import urlopen, urlretrieve


def print_err(*args, **kwargs):
    ''' Print a message to stderr '''
    sys.stderr.write(*args, **kwargs)
    sys.stderr.write('\n')


def main(args):
    ''' Main routine '''
    if not args.version:
        args.version = r'\d+\.\d+\.\d+(\.\w+)*'

    os.makedirs(args.dir, exist_ok=True)

    txt = urlopen(args.url).read().decode('utf-8')
    whls = re.findall(
        r'href=[\'"](.+?/swat-{}(?:-\d+)?-.+?\.whl)'.format(args.version), txt)
    for whl in whls:
        url = urljoin(args.url, whl)
        print(url)
        urlretrieve(url, filename=os.path.join(args.dir, whl.split('/')[-1]))

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.strip(),
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--version', '-v', type=str, metavar='version',
                        help='version of package to download')
    parser.add_argument('--dir', '-d', type=str, metavar='directory',
                        default='.',
                        help='directory to download the files to')
    parser.add_argument('url', type=str, metavar='url',
                        help='URL of PyPI package to download')

    args = parser.parse_args()

    try:
        sys.exit(main(args))
    except argparse.ArgumentTypeError as exc:
        print_err('ERROR: {}'.format(exc))
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
