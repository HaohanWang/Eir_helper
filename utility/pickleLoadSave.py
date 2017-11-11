__author__ = 'Haohan Wang'

import pickle

def pickleLoad(filename):
    import cPickle as pickle
    # file = open(filename,'r')
    # object_file = pickle.load(file)
    # file.close()
    # return object_file
    with open(filename, 'rb') as handle:
        r = pickle.load(handle)
    return r

def pickleSave(fileName, fileToSave):
    with open(fileName, "wb") as mypicklefile:
        pickle.dump(fileToSave, mypicklefile, protocol=pickle.HIGHEST_PROTOCOL)