# @Author: chesterblue
# @File Name:makeDir.py
import os

def makeLogDir():
    if os.path.exists("../log"):
        pass
    else:
        os.mkdir("../log")

def makeSitesDir():
    if os.path.exists("../sites"):
        pass
    else:
        os.mkdir("../sites")


if __name__ == '__main__':
    makeLogDir()
    makeSitesDir()