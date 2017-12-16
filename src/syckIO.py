import re
import linecache

lines={}

filename=""

def file_length(filename):
    length=0
    f=open(filename, "r")
    for line in f:
        length+=1
    f.close()
    return(length)


class Basic:
	def openfile():
		Basic.f=open(filename,"r")
		return(Basic.f)

	def closefile():
		Basic.f.close()

def reader():
	line_number=1
	Basic.openfile()
	for line in Basic.f:
		lines[line_number]=linecache.getline(filename, line_number)
		linecache.clearcache()
		line_number+=1

def readlines():
	for item in lines:
		print(item, lines[item])
