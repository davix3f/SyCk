import re

from cpp import *

test = """do {
	code
	code }
while(a)"""


def check(type):

	print("Type is:", type)

	def recognizer():

		"""Are you a for?"""

		if re.match(type.init_pattern, test, flags=re.DOTALL):
			return(True)
		else:
			print("error in recognizer")
			return(False)

	def middler():

		"""It's not important what you find in the end, but along the walk"""

		if type == DoWhile:
			return(True)  #since doWhile doesn't have any mid-code, afaik

		
		if type is For:

			valid=0 # if it reaches 3, [init,cond,increment] are all valid

			for item in type.mid_pattern:
				if re.search(type.mid_pattern[item], test):
					print(item, 0)
					valid+=1
				else:
					print(item, 1)
			if valid==3:
				return(True)
			else:
				#print("error in middler")
				return(False)

		else:

			if re.search(type.mid_pattern, test):
				return(True)
			else:
				print("error in middler")
				return(False)



	def final():

		#jk, also what you find in the end matters. a lot.

		if re.search(type.final_pattern, test, flags=re.DOTALL):
			return(True)
		else:
			print("error in final")
			return(False)


	if recognizer() and middler() and final():
		print(0)
	else:
		print("error")
