from os import path
from linecache import *
import re, sys

testfile="testfile" #edit the string with the path of the file

if path.exists(testfile) != True:
	sys.exit("the selected file doesn't exists")

class Output:
	test=""

	def reset():
		test=""


def readline(selection_type=None,*selection):		# Selection_type possibilities:[singleline, range]
                                                    # Selection: A tuple if selection type is range, or a number if it's singleline


	
	def r_range(rangelines=selection[0]):

		""" start_read_from_line  takes as argument the [0] element of the tuple
			to use it as the starting line of the range of reading.

			finish_read_at_line  takes as argument the [1] element of the tuple
			to use it as the ending line of the range of reading.

			linedex and linedex_end are just shortcuts for faster-writable coding 
		"""

		start_read_from_line = rangelines[0]
		finish_read_at_line = rangelines[1]

		linedex = start_read_from_line

		linedex_end = finish_read_at_line


		""" 
							while loop explaining

			#1 line: prints the line number, and the corresponding line
			#2 line: edits Output.test variable adding each time the read line
					in orderd to make it ready for the SyCk main script
			#3 line: getline.clearcache() function
			#4 line: linedex++ 

		"""


		while int(linedex) <= int(linedex_end):
			print(str(linedex)+":",getline(str(testfile), linedex))
			Output.test += getline(str(testfile), linedex)
			clearcache()
			linedex += 1

	def r_line(line=selection[0]):

		""" Basically the same thing. Just with one line. """

		print(str(line)+":",getline(str(testfile), line))
		Output.test += getline(str(testfile), linedex)
		clearcache()


	""" Choosing the function in base of the selection_type value
		also some mistypes, oh-i-forgot errors escaping
	 """

	if selection_type == "singleline":
		r_line()
	elif selection_type == "range":
		r_range()
	elif selection_type == None:
		print("Selection_type key is NONE: closing <readline> function")
		return("NONE_error")
		exit()
	else:
		print("Selection_type key value not supported: closing <readline> function")
		return("NSUPP_error")
		exit()

	return(Output.test)    #here's the output test string for syck