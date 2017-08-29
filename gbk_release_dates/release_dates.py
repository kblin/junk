#!/usr/bin/env python

from __future__ import print_function
import argparse
from glob import glob
from helperlibs.bio import seqio
import os

__version__ = '0.1.0'

UNKNOWN_DATE = 'UNKNOWN'
MAX_DATE = 9999

def main():
    parser = argparse.ArgumentParser(version=__version__)
    parser.add_argument(dest='basedir', metavar='DIR',
                        default=os.getcwd(),
                        help='Directory to scan for genome files (default: %(default)s)')
    args = parser.parse_args()

    files = glob(os.path.join(args.basedir, '*.gbff.gz')) + glob(os.path.join(args.basedir, '**', '*.gbff.gz'))

    for filename in files:
        recs = seqio.parse(filename)
        for rec in recs:
            date = parse_publish_date(rec)
            if date != UNKNOWN_DATE:
                break
        print(rec.id, rec.annotations['organism'], date, sep='\t')


def parse_publish_date(record):
    """Get the publication date out of a GenBank record"""

    if 'references' not in record.annotations:
        return UNKNOWN_DATE

    min_date = MAX_DATE

    for ref in record.annotations['references']:
        journal = ref.journal
        print(journal)
        if journal.startswith('Submitted ('):
            offset = 18
            str_date = journal[offset:journal.find(')')]
        elif journal.endswith(')'):
            str_date = journal[journal.rfind('(')+1:-1]
        else:
            print("{ref.title}, {ref.comment}, {ref.authors}".format(ref=ref))
            continue
        try:
            new_date = int(str_date)
            if new_date < min_date:
                min_date = new_date
        except ValueError:
            print('could not convert', str_date)
            pass

    if min_date < MAX_DATE:
        return str(min_date)

    return UNKNOWN_DATE


if __name__ == '__main__':
    main()
