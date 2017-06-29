#By: jttew
from __future__ import print_function
from recognizer import *
import sys


def prettyPrint(tree):

	if(tree == None):
		return None

	cat = tree.category

	if(cat == "INTEGER"):
		print(tree.value, end=' ')

	elif(cat == "ID"):
		print(tree.value, end=' ')

	elif(cat == "STRING"):
		print('"' + tree.value + '"', end=' ')

	elif(cat == "TOPNODE"):
		prettyPrint(tree.left)
		prettyPrint(tree.right)

	elif(cat == "CLASS"):
		print("class " + str(tree.right.value) + " [")
		prettyPrint(tree.left)
		print("  ]")

	elif(cat == "FUNC"):
		print("def", end=' ')
		prettyPrint(tree.left)
		print("(", end=' ')
		t = tree.left.right
		if(t != None):
			prettyPrint(t)
			t = t.right
		while(t != None):
			print(",", end=' ')
			prettyPrint(t)
			t = t.right
		print(") [")
		prettyPrint(tree.right)
		print("]")
		
	elif(cat == "DECL"):
		prettyPrint(tree.left)
		print(";")
		prettyPrint(tree.right) 

	elif(cat == "VARDECL"):
		print(str(tree.left.value) + " =", end=' ')
		prettyPrint(tree.right)

	elif(cat == "PRIMARY"):
		prettyPrint(tree.left)
		#TREE.RIGHT COVERED IN OTHER FUNCTIONS

	elif(cat == "PAREN"):
		print("(", end=' ')
		prettyPrint(tree.left)
		print(")", end=' ')

	elif(cat == "PRIMARYLIST"):
		print("(", end=' ')
		prettyPrint(tree.left)
		tree = tree.left.right
		while(tree != None):
			print(",", end=' ')
			prettyPrint(tree.left)
			tree = tree.left.right
		print(")", end=' ')

	elif(cat == "LIST"):
		print("{", end=' ')
		prettyPrint(tree.left)
		print("}", end=' ')

	elif(cat == "OPTLIST"):
		prettyPrint(tree.left)
		if(tree.right != None):
			print(",", end=' ')
			prettyPrint(tree.right)

	elif(cat == "OP"):
		prettyPrint(tree.left)
		prettyPrint(tree.right)

	elif(cat == "PLUS"):
		prettyPrint(tree.left)
		print("+", end=' ')

	elif(cat == "MINUS"):
		prettyPrint(tree.left)
		print("-", end=' ')

	elif(cat == "MULTIPLY"):
		prettyPrint(tree.left)
		print("*", end=' ')

	elif(cat == "DEVIDE"):
		prettyPrint(tree.left)
		print("/", end=' ')

	elif(cat == "POWER"):
		prettyPrint(tree.left)
		print("^", end=' ')

	elif(cat == "LOGIC"):
		prettyPrint(tree.left)
		print(tree.value, end=' ')

	elif(cat == "WHILE"):
		print("while(", end=' ')
		prettyPrint(tree.left)
		print(") [")
		prettyPrint(tree.right)
		print("]")

	elif(cat == "IF"):
		print("if(", end=' ')
		prettyPrint(tree.left)
		print(") [")
		prettyPrint(tree.right.left)
		print("]")
		prettyPrint(tree.right.right)
	
	elif(cat == "ELSE"):
		print("else[")
		prettyPrint(tree.left)
		print("]")

	elif(cat == "FUNCCALL"):
		prettyPrint(tree.left)
		prettyPrint(tree.right)


def main():
	filename = sys.argv[1]
	x = Recognizer(filename)
	prettyPrint(x.getTree())
	eval_(x.getTree())

def eval_(p):
	if(p == None):
		return None
	print(p)
	print(p.category)
	cat = p.category
	if(cat == "TOPNODE"):
		eval_(p.left)
		return eval_(p.right)
	elif(cat == "FUNC"):
		return eval_(p.right)
	elif(cat == "DECL"):
		eval_(p.left)
		return eval_(p.right)
	elif(cat == "PRINT"):
		args = p.left
		print(args)
		while args != None:
			prettyPrint(eval_(args.left))
			args = args.right
		return None
	elif(cat == "PRIMARY"):
		return eval_(p.left)
	elif(cat == "STRING"):
		return p	
	
	sys.exit("ERROR" + cat)
	return None
		

main()
