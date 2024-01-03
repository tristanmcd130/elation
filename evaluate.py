from parse import *
from lark import LarkError

def env_has(env, symbol):
	return len([x for x in env if x[0] == symbol]) > 0

def env_get(env, symbol):
	return [x for x in env if x[0] == symbol][0][1 : ]

def step(queue, stack, env):
	if len(queue) == 0:
		return [], stack, env
	value = queue[0]
	if callable(value):
		return value(queue[1 : ], stack, env)
	elif type(value) == ElationError:
		print(f"Error: {value.message}")
		return [], stack, env
	elif type(value) == Symbol:
		if env_has(env, value):
			return env_get(env, value) + queue[1 : ], stack, env
		else:
			return [ElationError(f"{value} undefined in current environment")] + queue[1 : ], stack, env
	else:
		return queue[1 : ], [value] + stack, env

def evaluate(program, stack, env):
	queue = program
	while len(queue) > 0:
		queue, stack, env = step(queue, stack, env)
	return [], stack, env

def run(string, stack = [], env = []):
	try:
		return evaluate(parse(string), stack, env)
	except LarkError as error:
		print(f"Parser error: {error}")
	return [], stack, env

def repl(stack = [], env = []):
	while True:
		try:
			_, stack, env = run(input("> "), stack, env)
			print(to_string(stack)[1 : -1])
		except KeyboardInterrupt:
			print()
		except EOFError:
			print()
			break