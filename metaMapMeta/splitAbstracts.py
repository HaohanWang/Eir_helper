__author__ = 'Haohan Wang'

from utility.pickleLoadSave import *
from utility.paths import *
import numpy as np

def loadData(num):
    data = np.load(dataPath + 'download_articles')
    # data = pickleLoad('../test/splitAbstracts'+str(num))
    return data

def splitData():
    data = loadData(0)

    queries = []
    for k in data:
        queries.append(k)
    tl = len(queries)

    m = tl/8
    for i in range(7):
        data_tmp = {}
        for j in range(i*m, (i+1)*m):
            k = queries[j]
            data_tmp[k] = data[k]
        pickleSave(dataPath+'splitAbstracts'+str(i), data_tmp)
        del data_tmp
    data_tmp = {}
    for j in range(7*m, tl):
        k = queries[j]
        data_tmp[k] = data[k]
    pickleSave(dataPath+'splitAbstracts'+str(7), data_tmp)
    del data_tmp

if __name__ == '__main__':
    splitData()
