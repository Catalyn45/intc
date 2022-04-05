from distutils import ccompiler
import os
from enum import Enum, auto

compiler = ccompiler.new_compiler()

code_pattern =  '''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
%s
int main() {
	%s
	return 0;
}
'''

class Statements(Enum):
	ASSIGNMENT = auto()
	IF = auto()
	WHILE = auto()
	FUNCTION = auto()
	RETURN = auto()
	CALL = auto()
	PRINT = auto()
	READ = auto()
	COMMENT = auto()
	BLOCK = auto()
	EMPTY = auto()
	UNKNOWN = auto()


PARANTESIS_MAP = {
	'{': 0,
	'(': 0,
	'[': 0,
}

REVERSE_PARANTESIS_MAP = {
	'}': '{',
	')': '(',
	']': '['
}

def need_to_buffer(line):
	for char in line:
		if char in PARANTESIS_MAP:
			PARANTESIS_MAP[char] += 1
		elif char in REVERSE_PARANTESIS_MAP:
			PARANTESIS_MAP[REVERSE_PARANTESIS_MAP[char]] -= 1

	if any(PARANTESIS_MAP.values()):
		return True

	return False

BUFFER = ""

def identify_statement(statement):
	if "printf" in statement:
		return Statements.PRINT

	return Statements.UNKNOWN

def interpret(line):
	global code_pattern
	global BUFFER

	if line == "exit()":
		exit()

	BUFFER += line + '\n'
	if need_to_buffer(line):
		return

	with open("tmp_file.c", "w") as f:
		f.write(code_pattern % BUFFER)

	try:
		compiler.compile(["./tmp_file.c"])
		compiler.link_executable(["tmp_file.o"], "tmp_exec")
	except Exception as e:
		BUFFER = ""
		return print(e)

	NEW_BUFFER = ""

	for line in BUFFER.split("\n"):
		stmt_type = identify_statement(line)
		if stmt_type != Statements.PRINT:
			NEW_BUFFER += line + '\n'

	BUFFER = ""

	code_pattern = code_pattern % f"{NEW_BUFFER}%s"

	os.system("./tmp_exec")
	print()

def main():
	while True:
		try:
			code = input("> ")
		except EOFError:
			break

		interpret(code)

if __name__ == "__main__":
	main()