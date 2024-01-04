from type import *

class Precondition:
	def __init__(self, function, requirement):
		self.function = function
		self.requirement = requirement
	def __call__(self, queue, stack, env):
		try:
			return self.function(queue, stack, env)
		except Exception:
			return False

one_logical = Precondition(lambda q, s, e: type(s[0]) == bool, "a logical")
two_logicals = Precondition(lambda q, s, e: type(s[1]) == type(s[0]) == bool, "2 logicals")
one_character = Precondition(lambda q, s, e: type(s[0]) == Char, "a character")
one_integer = Precondition(lambda q, s, e: type(s[0]) == int, "an integer")
one_string = Precondition(lambda q, s, e: type(s[0]) == str, "a string")
one_list = Precondition(lambda q, s, e: type(s[0]) == list, "a list")
two_lists = Precondition(lambda q, s, e: type(s[1]) == type(s[0]) == list, "2 lists")
three_lists = Precondition(lambda q, s, e: type(s[2]) == type(s[1]) == type(s[0]) == list, "3 lists")
four_lists = Precondition(lambda q, s, e: type(s[3]) == type(s[2]) == type(s[1]) == type(s[0]) == list, "4 lists")
one_symbol = Precondition(lambda q, s, e: type(s[0]) == Symbol, "a symbol")
one_number = Precondition(lambda q, s, e: type(s[0]) in [int, float], "a number")
two_numbers = Precondition(lambda q, s, e: type(s[1]) in [int, float] and type(s[0]) in [int, float], "2 numbers")
one_sequence = Precondition(lambda q, s, e: type(s[0]) in [str, list], "a sequence")
nonempty_sequence = Precondition(lambda q, s, e: type(s[0]) in [str, list] and len(s[0]) > 0, "a nonempty sequence")
one_argument = Precondition(lambda q, s, e: len(s) >= 1, "1 argument")
two_arguments = Precondition(lambda q, s, e: len(s) >= 2, "2 arguments")
define_arguments = Precondition(lambda q, s, e: type(s[1]) == list and len(s[1]) == 1 and type(s[1][0]) == Symbol and type(s[0]) == list, "a quoted symbol followed by a list")
dip_arguments = Precondition(lambda q, s, e: len(s) >= 2 and type(s[0]) == list, "any value followed by a list")
choice_arguments = Precondition(lambda q, s, e: len(s) >= 3 and type(s[2]) == bool, "a logical followed by 2 values")
cons_arguments = Precondition(lambda q, s, e: (type(s[1]) == Char and type(s[0]) == str) or (len(s) >= 2 and type(s[0]) == list), "a character followed by a list or any value followed by a list")
at_arguments = Precondition(lambda q, s, e: len(s[1]) == list and type(s[0]) == int and s[0] >= 0, "a list followed by a positive integer")
concat_arguments = Precondition(lambda q, s, e: type(s[1]) == type(s[0]) and type(s[0]) in [str, list], "2 strings or 2 lists")
nonempty_queue = Precondition(lambda q, s, e: len(q) > 0, "a nonempty queue")