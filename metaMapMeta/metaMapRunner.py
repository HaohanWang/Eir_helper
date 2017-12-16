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
    # data = pickleLoad(dataPath + 'Result'+str(num))
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


def processedInputData(abstract, num):
    f = open(tmpPath + 'tmp'+str(num)+'.txt', 'w')
    f.writelines(abstract.encode('utf-8')+'\n')
    f.close()

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def processedOutputData(num):
    text = [line.strip() for line in open('output'+str(num)+'.txt')]
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

def callMetaMap(num):
    mainCommand = metaMapPath+'bin/metamap16'
    command = [mainCommand,'-q', '<', 'tmp'+str(num)+'.txt', '>', 'output'+str(num)+'.txt']
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
                        abstract = k['abstract']
                        abstract = ''.join([i if ord(i) < 128 else ' ' for i in abstract])
                        processedInputData(abstract, num)
                        callMetaMap(num)
                        seqs = processedOutputData(num)
                        k['metamap'] = seqs
                        f1 = open(dataPath + 'textResult/result'+str(num), 'a')
                        f1.writelines('----------------\n')
                        f1.writelines('\t'.join(a)+'\n')
                        f1.writelines(k['PMID']+'\n')
                        for m in seqs:
                            f1.writelines(str(m[0])+'\t'+str(m[1])+'\t'+'\t'.join(m[2])+'\n')
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
