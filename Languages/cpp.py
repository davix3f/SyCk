#lang:CPP
#v:0.3

class Function:
    def __init__(self, name, return_type, extension=None, args=None, nested={}):
        
        self.name = name
        self.return_type = return_type
        self.extension = extension
        self.args = args
        self.nested = nested


    init_pattern = r"(?P<return_type>(int|bool|char|string|void))[\s]+(?P<f_name>\w+)[\s]*\(((int|bool|char|string)(.+)?)?\){"

    final_pattern = r"}$"

class For:

	init_pattern = r"^for\("  #starting for 'for' cycle

	mid_pattern = {"init_condition":r"(int [\w]+[\s]?\=[\s]?[\d]+\;)|(\;[\s]*)", #initial statement
			"final_condition":r"((int)?[\w]+(\==|\<|\>|!=|\>=|\<=)[\d]+\;)|(\;[\s]*)", #final condition to stop for
			"increment_operator":r"(([\w]+)?[\s]?(\++|\--|\+=[\d]+|\-=[\d]+|\/=[\d]+|\*=[\d]+)\))?" #incrementing operator [ex x++]
                        }

	final_pattern = r"\)[\s]?\{.+\}" # something){codecodecode} -- detector


class While:

	init_pattern = r"while[\s]?\("

	mid_pattern = r"(([\w]+[\s]?(\==|\<|\>|!=|\>=|\<=)?[\d]*)|[\w]+)"

	final_pattern = r"\)[\s]?\{.+\}"


class DoWhile:

	init_pattern = r"do \{.+\}"

	final_pattern = r"while\((([\s]*\([\w]+[\s]?(\==|\<|\>|!=|\>=|\<=)?[\d]*)|[\w])+\)"

class Switch(Function):
        
	init_pattern = r"switch[\s]*\(([\w]+|[\d]+)\)[\s]*\{"

	mid_pattern = r"case ([\w]+|[\d]+)\:[\n]([\t]*(.*)[\n]*)*break;"

	final_pattern = r"break;((\n)*)(\s*)?\}"



#List of all langclasses. Keep it updated.

lang_classes = [For, While, DoWhile, Switch, Function]
