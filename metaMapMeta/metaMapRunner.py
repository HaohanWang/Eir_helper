__author__ = 'Haohan Wang'

import sys
sys.path.append('../')

from utility.paths import *
from utility.pickleLoadSave import *

import numpy as np
import subprocess
import time
import os

tmpPath = currentPath + 'metaMapMeta/'

def loadData(num):
    # data = np.load(dataPath + 'download_articles')
    data = pickleLoad(dataPath + 'splitAbstracts'+str(num))
    return data

def loadTriedCases(num):
    try:
        # ls = pickleLoad(dataPath+'triedCase/'+'triedCase'+str(num))
        text = [line.strip() for line in open(dataPath+'triedCase/'+'triedCase'+str(num))]
        ls = []
        for line in text:
            items = line.split('\t')
            ls.append((items[0], items[1]))
        return ls
    except:
        return []


def processedInputData(abstract):
    f = open(tmpPath + 'tmp.txt', 'w')
    abstract = ''.join([i if ord(i) < 128 else ' ' for i in abstract])
    f.writelines(abstract.encode('utf-8')+'\n')
    f.close()

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def processedOutputData():
    text = [line.strip() for line in open('output.txt')]
    sequence = []
    for line in text:
        if line.startswith('mappings'):
            s = len('mappings([map')
            items = line[s:].split('map')[0].split('ev(')
            for item in items[1:]:
                infos = item.split(',')
                score = -int(infos[0])
                concept = infos[1][1:-1]
                sst = find_nth(item, '[', 2)+1
                est = find_nth(item, ']', 2)
                st = item[sst:est].split(',')
                sequence.append((score, concept, st))

    return sequence

def callMetaMap():
    mainCommand = metaMapPath+'bin/metamap16'
    command = [mainCommand,'-q', '<', 'tmp.txt', '>', 'output.txt']
    # print command
    # subprocess.check_output(command)
    os.system(' '.join(command))

def run(num):
    original_data = loadData(num)
    triedCase = loadTriedCases(num)

    queriesCount = len(original_data)
    c = 0
    seqs_total = []
    for a in original_data:
        c += 1
        start = time.time()
        if a not in triedCase:
            triedCase.append(a)
            f2 = open(dataPath + 'triedCase/' + 'triedCase' + str(num), 'w')
            for a in triedCase:
                f2.writelines('\t'.join(a) + '\n')
            f2.close()
            try:
                for k in original_data[a]:
                    if 'metamap' not in k:
                        processedInputData(k['abstract'])
                        callMetaMap()
                        seqs = processedOutputData()
                        k['metamap'] = seqs
                        f1 = open(dataPath + 'textResult/result'+str(num), 'a')
                        f1.writelines('\t'.join(a)+'\t')
                        f1.writelines(k['abstract']+'\t')
                        f1.writelines('\t'.join(seqs))
                        f1.close()
            except:
                pass
        end = time.time()
        print '\nprocessed Query:', c, '/', queriesCount, '\t with ', len(original_data[a]), 'documents',
        print 'in ', end-start, 'seconds'
        pickleSave(dataPath + 'result/'+'Result'+str(num), original_data)

if __name__ == '__main__':
    num = int(sys.argv[1])
    run(num)
