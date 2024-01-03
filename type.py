class Char(str):
	def __init__(self, value):
		assert type(value) == str and len(value) == 1, "Char must be a str of length 1"
		super().__init__()

class Symbol(str):
	def __eq__(self, other):
		return type(other) == Symbol and str(self) == str(other)
	def __hash__(self):
		return str(self).__hash__() + 1

class ConkError(Exception):
	def __init__(self, message = ""):
		self.message = message
		super().__init__(type, message)

def to_string(value):
	if type(value) in [int, float]:
		return "%g" % value
	elif type(value) in [str, Char, Symbol]:
		return value
	elif type(value) == bool:
		return str(value).lower()
	elif type(value) == list:
		return "[" + " ".join([to_string_in_list(x) for x in value]) + "]"
	elif callable(value):
		return "<primitive>"
	elif isinstance(value, Exception):
		return "<error>"
	else:
		return str(value)

def to_string_in_list(value):
	if type(value) == Char:
		return "'" + value.encode("unicode_escape").decode("utf-8") + "'"
	elif type(value) == str:
		return "\"" + value.encode("unicode_escape").decode("utf-8") + "\""
	else:
		return to_string(value)