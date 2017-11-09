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

def mergeData():
    data = {}
    # 0 EOF error
    # 1 EOF error
    # 2 insecure string pickle
    # 4 EOF error
    # 6 EOF error
    # 7 EOF error
    for i in [1]:
        result = pickleLoad(dataPath + 'result/Result'+str(i))
        for a in result:
            data[a] = result[a]
        del result

    pickleSave(dataPath + 'allResults', data)

if __name__ == '__main__':
    mergeData()
