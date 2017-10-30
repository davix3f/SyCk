import re, linecache

testfile = "testfile"

lines={}


def file_length(testfile=testfile):

    lngt=0
    f=open(testfile, "r")
    for line in f:
        lngt+=1
    f.close()
    return(lngt)


class Basic:
	def openfile():
		Basic.f=open("testfile","r")
		return(Basic.f)

	def closefile():
		Basic.f.close()

def reader():
	line_number=1
	Basic.openfile()
	for line in Basic.f:
		lines[line_number]=linecache.getline(testfile, line_number)
		linecache.clearcache()
		line_number+=1

def readlines():
	for item in lines:
		print(item, lines[item])
