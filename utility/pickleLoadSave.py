__author__ = 'Haohan Wang'

import pickle

def pickleLoad(filename):
    file = open(filename,'rb')
    object_file = pickle.load(file)
    file.close()
    return object_file

def pickleSave(fileName, fileToSave):
    with open(fileName, "wb") as mypicklefile:
        pickle.dump(fileToSave, mypicklefile)