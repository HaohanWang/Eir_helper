__author__ = 'Haohan Wang'

import numpy as np

def replaceText():
    text = [line.strip() for line in open('../data/examples.txt')]

    n2c = np.load('../data/processed/n2c.npy').item()
    print type(n2c)
    f = open('example_new.txt', 'w')
    for line in text:
        if line.startswith('#'):
            f.writelines('\n')
        else:
            if line in n2c:
                f.writelines(n2c[line]+'\n')
            else:
                f.writelines('\n')
    f.close()


if __name__ == '__main__':
    n2c = np.load('../data/processed/n2c.npy').item()
    print n2c['Evidence']