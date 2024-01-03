from type import *
from lark import Lark, Transformer

def parse(string, start = "term"):
	class ElationTransformer(Transformer):
		def term(self, items):
			return items
		def bool(self, items):
			return {"true": True, "false": False}[items[0].value]
		def int(self, items):
			return int(items[0].value)
		def float(self, items):
			return float(items[0].value)
		def char(self, items):
			return Char(items[0].value[1 : -1].encode("utf-8").decode("unicode_escape"))
		def string(self, items):
			return items[0].value[1 : -1].encode("utf-8").decode("unicode_escape")
		def symbol(self, items):
			return Symbol(items[0].value)
		def list(self, items):
			return items
	return ElationTransformer().transform(Lark(r"""
	term: factor*
	?factor: bool
		   | int
		   | float
		   | char
		   | string
		   | symbol
		   | list
	!bool: "true" | "false"
	int: SIGNED_INT
	float: SIGNED_FLOAT
	char: ESCAPED_CHAR
	string: ESCAPED_STRING
	symbol: SYMBOL
	list: "[" factor* "]"
	ESCAPED_CHAR: /'([^\\']|\\.+)'/
	SYMBOL: /[^\s#\[\]'\"]+/

	%import common.WS
	%import common.SH_COMMENT
	%import common.SIGNED_INT
	%import common.SIGNED_FLOAT
	%import common.ESCAPED_STRING
	%ignore WS
	%ignore SH_COMMENT
	""", start = start).parse(string))