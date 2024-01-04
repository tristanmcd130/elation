from evaluate import *
from preconditions import *
from sys import argv

primitives = []
def primitive(name, precondition = lambda q, s, e: True):
	def primitive_wrapper(function):
		global primitives
		def precondition_checker(queue, stack, env):
			if not precondition(queue, stack, env):
				return [ElationError(f"{name} requires {precondition.requirement}")] + queue, stack, env
			return function(queue, stack, env)
		primitives = env_set(primitives, Symbol(name), [precondition_checker])
		return precondition_checker
	return primitive_wrapper

@primitive("include", one_string)
def include(queue, stack, env):
	with open(stack[0]) as file:
		return queue, stack[1 : ], run(file.read(), stack[1 : ], env)[2]

@primitive("define", define_arguments)
def define(queue, stack, env):
	return queue, stack[2 : ], env_set(env, stack[1][0], stack[0])

@primitive("trace", one_list)
def trace(queue, stack, env):
	new_queue = stack[0]
	new_stack = stack[1 : ]
	while len(new_queue) > 0:
		print(f"Stack: {to_string(new_stack)[1 : -1]}\nQueue: {to_string(new_queue)[1 : -1]}\n")
		new_queue, new_stack, env = step(new_queue, new_stack, env)
	return new_queue, new_stack, env

@primitive("stack")
def stack(queue, stack, env):
	return queue, [stack] + stack, env

@primitive("unstack", one_list)
def unstack(queue, stack, env):
	return queue, stack[0], env

@primitive("queue")
def queue(queue, stack, env):
	return queue, [queue] + stack, env

@primitive("unqueue", one_list)
def unqueue(queue, stack, env):
	return stack[0], stack[1 : ], env

@primitive("env")
def env(queue, stack, env):
	return queue, [env] + stack, env

@primitive("unenv", one_list)
def unenv(queue, stack, env):
	return queue, stack[1 : ], stack[0]

@primitive("dup", one_argument)
def dup(queue, stack, env):
	return queue, [stack[0]] + stack, env

@primitive("swap", two_arguments)
def swap(queue, stack, env):
	return queue, [stack[1], stack[0]] + stack[2 : ], env

@primitive("pop", one_argument)
def pop(queue, stack, env):
	return queue, stack[1 : ], env

@primitive("choice", choice_arguments)
def choice(queue, stack, env):
	return queue, [stack[1] if stack[2] else stack[0]] + stack[3 : ], env

@primitive("and", two_logicals)
def _and(queue, stack, env):
	return queue, [stack[1] and stack[0]] + stack[2 : ], env

@primitive("or", two_logicals)
def _or(queue, stack, env):
	return queue, [stack[1] or stack[0]] + stack[2 : ], env

@primitive("xor", two_logicals)
def _xor(queue, stack, env):
	return queue, [stack[1] ^ stack[0]] + stack[2 : ], env

@primitive("not", one_logical)
def _not(queue, stack, env):
	return queue, [not stack[0]] + stack[1 : ], env

@primitive("+", two_numbers)
def add(queue, stack, env):
	return queue, [stack[1] + stack[0]] + stack[2 : ], env

@primitive("-", two_numbers)
def sub(queue, stack, env):
	return queue, [stack[1] - stack[0]] + stack[2 : ], env

@primitive("*", two_numbers)
def mul(queue, stack, env):
	return queue, [stack[1] * stack[0]] + stack[2 : ], env

@primitive("/", two_numbers)
def div(queue, stack, env):
	return queue, [stack[1] / stack[0]] + stack[2 : ], env

@primitive("%", two_numbers)
def mod(queue, stack, env):
	return queue, [stack[1] % stack[0]] + stack[2 : ], env

@primitive("sign", one_number)
def sign(queue, stack, env):
	return queue, [stack[0] // abs(stack[0]) if stack[0] else 0] + stack[1 : ], env

@primitive("abs", one_number)
def _abs(queue, stack, env):
	return queue, [abs(stack[0])] + stack[1 : ], env

@primitive("ord", one_character)
def _ord(queue, stack, env):
	return queue, [ord(stack[0])] + stack[1 : ], env

@primitive("chr", one_integer)
def _chr(queue, stack, env):
	return queue, [chr(stack[0])] + stack[1 : ], env

# TODO: all the crappy math functions

@primitive("max", two_numbers)
def _max(queue, stack, env):
	return queue, [max(stack[1], stack[0])] + stack[2 : ], env

@primitive("min", two_numbers)
def _min(queue, stack, env):
	return queue, [min(stack[1], stack[0])] + stack[2 : ], env

@primitive("cons", cons_arguments)
def cons(queue, stack, env):
	return queue, [stack[1] + stack[0] if type(stack[0]) == str else [stack[1]] + stack[0]] + stack[2 : ], env

@primitive("first", nonempty_sequence)
def first(queue, stack, env):
	return queue, [stack[0][0]] + stack[1 : ], env

@primitive("rest", nonempty_sequence)
def rest(queue, stack, env):
	return queue, [stack[0][1 : ]] + stack[1 : ], env

@primitive("at", at_arguments)
def at(queue, stack, env):
	return queue, [stack[1][0]] + stack[2 : ], env

@primitive("size", one_sequence)
def size(queue, stack, env):
	return queue, [len(stack[0])] + stack[1 : ], env

@primitive("case", dip_arguments)
def case(queue, stack, env):
	matches = [x[1 : ] for x in stack[0][ : -1] if x[0] == stack[1]]
	return (matches[0] if len(matches) else stack[0][-1]) + queue, stack[2 : ], env

@primitive("uncons", one_sequence)
def uncons(queue, stack, env):
	return queue, [stack[0][1 : ], Char(stack[0][0]) if type(stack[0]) == str else stack[0][0]] + stack[1 : ], env

@primitive("drop", at_arguments)
def drop(queue, stack, env):
	return queue, [stack[1][stack[0] : ]] + stack[2 : ], env

@primitive("take", at_arguments)
def take(queue, stack, env):
	return queue, [stack[1][ : stack[0]]] + stack[2 : ], env

@primitive("concat", concat_arguments)
def concat(queue, stack, env):
	return queue, [stack[1] + stack[0]] + stack[2 : ], env

@primitive("name", one_symbol)
def name(queue, stack, env):
	return queue, [str(stack[0])] + stack[1 : ], env

@primitive("intern", one_string)
def intern(queue, stack, env):
	return queue, [Symbol(stack[0])] + stack[1 : ], env

@primitive(">", two_numbers)
def gt(queue, stack, env):
	return queue, [stack[1] > stack[0]] + stack[2 : ], env

@primitive("<", two_numbers)
def lt(queue, stack, env):
	return queue, [stack[1] < stack[0]] + stack[2 : ], env

@primitive("=", two_arguments)
def eq(queue, stack, env):
	return queue, [stack[1] == stack[0]] + stack[2 : ], env

@primitive("in", cons_arguments)
def _in(queue, stack, env):
	return queue, [stack[1] in stack[0]] + stack[2 : ], env

@primitive("integer", one_argument)
def integer(queue, stack, env):
	return queue, [type(stack[0]) == int] + stack[1 : ], env

@primitive("float", one_argument)
def _float(queue, stack, env):
	return queue, [type(stack[0]) == float] + stack[1 : ], env

@primitive("char", one_argument)
def char(queue, stack, env):
	return queue, [type(stack[0]) == Char] + stack[1 : ], env

@primitive("logical", one_argument)
def logical(queue, stack, env):
	return queue, [type(stack[0]) == bool] + stack[1 : ], env

@primitive("string", one_argument)
def string(queue, stack, env):
	return queue, [type(stack[0]) == str] + stack[1 : ], env

@primitive("list", one_argument)
def _list(queue, stack, env):
	return queue, [type(stack[0]) == list] + stack[1 : ], env

@primitive("i", one_list)
def i(queue, stack, env):
	return stack[0] + queue, stack[1 : ], env

@primitive("dip", dip_arguments)
def dip(queue, stack, env):
	return stack[0] + [Symbol("mention"), stack[1]] + queue, stack[2 : ], env

@primitive("nullary", one_list)
def nullary(queue, stack, env):
	return stack[0] + [stack[1 : ], Symbol("cons"), Symbol("unstack")] + queue, stack[1 : ], env

@primitive("unary2", one_list)
def unary2(queue, stack, env):
	return [stack[2]] + stack[0] + [stack[1]] + stack[0] + queue, stack[3 : ], env

@primitive("unary3", one_list)
def unary3(queue, stack, env):
	return [stack[3]] + stack[0] + [stack[2]] + stack[0] + [stack[1]] + stack[0] + queue, stack[4 : ], env

@primitive("unary4", one_list)
def unary4(queue, stack, env):
	return [stack[4]] + stack[0] + [stack[3]] + stack[0] + [stack[2]] + stack[0] + [stack[1]] + stack[0] + queue, stack[5 : ], env

@primitive("cleave", two_lists)
def cleave(queue, stack, env):
	return stack[2] + [stack[1]] + stack[2] + [stack[0]] + queue, stack[3 : ], env

@primitive("linrec", four_lists)
def linrec(queue, stack, env):
	p = stack[3]
	t = stack[2]
	r1 = stack[1]
	r2 = stack[0]
	return [p, t, r1 + [p, t, r1, r2, Symbol("linrec")] + r2, Symbol("ifte")] + queue, stack[4 : ], env

@primitive("tailrec", three_lists)
def tailrec(queue, stack, env):
	p = stack[2]
	t = stack[1]
	r1 = stack[0]
	return [p, t, r1 + [p, t, r1, Symbol("tailrec")], Symbol("ifte")] + queue, stack[3 : ], env

@primitive("binrec", four_lists)
def binrec(queue, stack, env):
	p = stack[3]
	t = stack[2]
	r1 = stack[1]
	r2 = stack[0]
	return [p, t, r1 + [[p, t, r1, r2, Symbol("binrec")], Symbol("unary2")] + r2, Symbol("ifte")] + queue, stack[4 : ], env

@primitive("genrec", four_lists)
def genrec(queue, stack, env):
	p = stack[3]
	t = stack[2]
	r1 = stack[1]
	r2 = stack[0]
	return [p, t, r1 + [[p, t, r1, r2, Symbol("genrec")]] + r2, Symbol("ifte")] + queue, stack[4 : ], env

@primitive("infra", two_lists)
def infra(queue, stack, env):
	return [stack[1], Symbol("unstack")] + stack[0] + [stack[2 : ], Symbol("cons"), Symbol("unstack")] + queue, stack[2 : ], env

@primitive("get")
def get(queue, stack, env):
	return queue, [parse(input(), start = "factor")] + stack, env

@primitive("put")
def put(queue, stack, env):
	print(to_string(stack[0]), end = "")
	return queue, stack[1 : ], env

@primitive("argv")
def _argv(queue, stack, env):
	return queue, [argv] + stack, env

@primitive("quit")
def quit(queue, stack, env):
	exit()

@primitive("mention", nonempty_queue)
def mention(queue, stack, env):
	return queue[1 : ], [queue[0]] + stack, env