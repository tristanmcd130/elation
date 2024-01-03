from evaluate import *
from preconditions import *

primitives = []
def primitive(name, precondition = lambda q, s, e: True):
	def primitive_wrapper(function):
		global primitives
		def precondition_checker(queue, stack, env):
			if not precondition(queue, stack, env):
				return [ElationError(f"{name} requires {precondition.requirement}")] + queue, stack, env
			return function(queue, stack, env)
		primitives.append([Symbol(name), precondition_checker])
		return precondition_checker
	return primitive_wrapper

@primitive("include", one_string)
def include(queue, stack, env):
	with open(stack[0]) as file:
		return queue, stack[1 : ], run(file.read(), stack[1 : ], env)[2]

@primitive("define", define_arguments)
def define(queue, stack, env):
	if env_has(env, stack[1][0]):
		return [ElationError(f"Cannot redefine {stack[1][0]}")] + queue, stack, env
	return queue, stack[2 : ], env + [stack[1] + stack[0]]

@primitive("trace", one_list)
def trace(queue, stack, env):
	while len(queue) > 0:
		print(f"Stack: {to_string(stack)[1 : -1]}\nQueue: {to_string(queue)[1 : -1]}\n")
		queue, stack, env = step(queue, stack, env)
	return queue, stack, env

@primitive("get")
def get(queue, stack, env):
	return queue, [parse(input(), start = "factor")] + stack, env

@primitive("put")
def put(queue, stack, env):
	print(to_string(stack[0]))
	return queue, stack[1 : ], env

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

@primitive("dip", dip_arguments)
def dip(queue, stack, env):
	return stack[0] + [[stack[1]], Symbol("first")] + queue, stack[2 : ], env

@primitive("choice", choice_arguments)
def choice(queue, stack, env):
	return queue, [stack[1] if stack[2] else stack[0]] + stack[3 : ], env

@primitive("and", two_booleans)
def _and(queue, stack, env):
	return queue, [stack[1] and stack[0]] + stack[2 : ], env

@primitive("or", two_booleans)
def _or(queue, stack, env):
	return queue, [stack[1] or stack[0]] + stack[2 : ], env

@primitive("xor", two_booleans)
def _xor(queue, stack, env):
	return queue, [stack[1] ^ stack[0]] + stack[2 : ], env

@primitive("not", one_boolean)
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

@primitive("max", two_numbers)
def _max(queue, stack, env):
	return queue, [max(stack[1], stack[0])] + stack[2 : ], env

@primitive("min", two_numbers)
def _min(queue, stack, env):
	return queue, [min(stack[1], stack[0])] + stack[2 : ], env

@primitive("cons", cons_arguments)
def cons(queue, stack, env):
	return queue, [stack[1] + stack[0] if type(stack[0]) == str else [stack[1]] + stack[0]] + stack[2 : ], env

@primitive("first", one_sequence)
def first(queue, stack, env):
	return queue, [stack[0][0]] + stack[1 : ], env

@primitive("rest", one_sequence)
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
	return queue, [stack[1] + stack[0]] + stack[1 : ], env