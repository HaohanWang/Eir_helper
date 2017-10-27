__author__ = 'Haohan Wang'

import numpy as np

def extract_concept():
    totalLine = 6600000
    s = 0
    ms = 1
    n2c = {}
    c2n = {}
    with open('../data/raw/MRCONSO.RRF') as f:
        for line in f:
            s += 1
            if s > ms*totalLine*0.005:
                print 'finished:', 0.005*ms
                ms += 1

            items = line.split('|')
            c = items[0]
            n = items[-5]
            n2c[n]=c
            if c not in c2n:
                c2n[c] = n

    np.save('../data/processed/n2c', n2c)
    np.save('../data/processed/c2n', c2n)


if __name__ == '__main__':
    extract_concept()