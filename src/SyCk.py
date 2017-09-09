# original lib modules
import re

# custom written modules
from syckIO import *
from cpp import * #for using it on cpp

print("Available classes from cpp are:", lang_classes)

readline("range",(1,8))

test = Output.test

for line in test:
	for item in lang_classes:
		if re.match(item.init_pattern, test):
			print("It matches", item, "init_pattern")
			re.match(item.init_pattern, test)
			exit()
		else:
			print("It doesn't match", item, "init_pattern")
			pass


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

		"""It's not important what you find at the end, but what you find along the journey"""

		if type == DoWhile:
			return(True)  	#since doWhile doesn't have any mid-code, afaik

		
		if type is For:

			valid=0 # if it reaches 3, [init,cond,increment] are all valid

			for item in type.mid_pattern:						# checking if init,cond and increment are
				if re.search(type.mid_pattern[item], test):		# all valid, by selecting every element of dict 'mid_pattern'
					print(item, 0)								# of For in cpp.py
					valid+=1
				else:
					print(item, 1)
			if valid==3:
				return(True)
			else:
				#print("error in middler")
				return(False)

		else:
			if re.search(type.mid_pattern, test):				# checking if mid-part coding of some loop is matchy.
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

	Output.reset()


	if recognizer() and middler() and final():
		print(0)
	else:
		print("error")