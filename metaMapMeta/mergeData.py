__author__ = 'Haohan Wang'

from utility.paths import *
import numpy as np

def loadText(num):
    textResult = [line.strip() for line in open(dataPath+'textResult/result'+str(num))]
    st = False
    for line in textResult:
        if line.startswith('----------------'):
            st = True