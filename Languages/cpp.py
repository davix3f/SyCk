#lang:CPP
#v:0.1b


class For:
	init_pattern = r"^for\("  #starting for 'for' cycle

	mid_pattern = {"init_condition":r"int [\w]+[\s]?\=[\s]?[\d]+\;", #initial statement
			"final_condition":r";(int)?[\w]+(\==|\<|\>|!=|\>=|\<=)[\d]+", #final condition to stop for
			"increment_operator":r"([\w]+)?[\s]?(\++|\--|\+=[\d]+|\-=[\d]+|\/=[\d]+|\*=[\d]+)\)" #incrementing operator [ex x++]
                        }

	final_pattern = r"\)[\s]?\{.+\}" # something){codecodecode} -- detector


class While:
	init_pattern = r"while[\s]?\("

	mid_pattern = r"(([\w]+[\s]?(\==|\<|\>|!=|\>=|\<=)?[\d]*)|[\w]+)"

	final_pattern = r"\)[\s]?\{.+\}"


class DoWhile:
	init_pattern = r"do \{.+\}"

	final_pattern = r"while\((([\s]*\([\w]+[\s]?(\==|\<|\>|!=|\>=|\<=)?[\d]*)|[\w])+\)"
