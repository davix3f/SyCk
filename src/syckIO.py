import re

from linecache import *

testfile = "testfile"

lines={}


def file_length(testfile=testfile):

    lngt=0

    f=open(testfile, "r")

    for line in f:
        lngt+=1
    f.close()

    return(lngt)


class basic:

	def openfile():

		basic.f=open("testfile","r")

		return(basic.f)

	def closefile():

		basic.f.close()


def reader():
	line_number=1
	basic.openfile()

	for line in basic.f:
		lines[line_number]=getline(testfile, line_number)
		clearcache()
		line_number+=1

def readlines():
	for item in lines:
		print(item, lines[item])
