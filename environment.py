#Change this to not be a class

from lexicalAnalyser import *

class Environment:
	env = None

	def __init__(self):
		self.env = Lexeme()
		self.env.category = "ENV"	
		self.env.left = Lexeme()
		self.env.left.category = "TABLE"

	def cons(self, category, left, right):
	#Left and Right must be lexemes.  It creates this:
	#   New Lexeme
	#    /  \
	# left   right
		new = Lexeme()
		new.category = category
		new.left = left
		new.right= right
		return new

	def extend(self, variables, values, envList):
		self.env = self.cons("ENV", self.cons("TABLE", variables, values), envList)
		
	def createEnv(self):
		return(self.extend(None, None, None))

	def insertEnv(self, ID, value, ENV):
		frame = ENV.left
		frame.left = self.cons("JOIN", ID, frame.left)
		frame.right = self.cons("JOIN", value, frame.right)
		return value

	def lookup(self, ID, ENV):
		x = 0
		while (ENV != None):
			frame = ENV.left
			ids = frame.left
			vals = frame.right
			while (ids != None):
				if (ID.value == ids.left.value):
					x = vals.left
				ids = ids.right
				vals = vals.right
			ENV = ENV.right
		if (x != 0):
			return x
		else:
			print("ERROR")

	
	def replace(self, ID, newVal, ENV):
		while (ENV != None):
			frame = ENV.left
			ids = frame.left
			vals = frame.right
			while (ids != None):
				if (ID.value == ids.left.value):
					vals.left = newVal
					return vals.left
				else:
					ids = ids.right
					vals = vals.right
			ENV = ENV.right
		print("ERROR")

	def displayAll(self, ENV):
		envCounter = 0
		x = ENV
		while (x.right != None):
			envCounter += 1
			x = x.right
		while (ENV != None):
			print("ENVIRONMENT " + str(envCounter))
			frame = ENV.left
			ids = frame.left
			vals = frame.right
			while (ids != None):
				print(str(ids.left.value) + " is " + str(vals.left.value))
				ids = ids.right
				vals = vals.right
			envCounter -= 1
			ENV = ENV.right


def eval_(tree, env, e):
	
	if(tree == None):
		return None

	cat = tree.category

	if(cat == "INTEGER"):
		return tree

	elif(cat == "ID"):
		return env.lookup(tree, env, e)

	elif(cat == "STRING"):
		return tree

	elif(cat == "OP"):
		return evalSimpleOp(tree, env, e)

	elif(cat == "PRIMARY"):
		return eval_(tree.left, env, e)

	elif(cat == "PAREN"):
		return eval_(tree.left, env, e)

	elif(cat == "TOPNODE"):
		eval_(tree.left, env, e)
		eval_(tree.right, env, e)

	elif(cat == "FUNCDEF"):
		return evalFuncDef(tree, env, e)

def evalFuncDef(t, env, e):
	var closure = e.cons("CLOSURE", env, e.cons("JOIN", getFuncDefParams(t, env, e), e.cons("JOIN", getFuncDefBody(t, env, e), None)))

def evalSimpleOp(t, env, e):
	t.left.category = cat
	if (cat == "PLUS"):
		return (eval_(t.left.left, env, e) + eval_(t.right, env, e))
	if (cat == "MINUS"):
		return (eval_(t.left.left, env, e) - eval_(t.right, env, e))
	if (cat == "MULTIPLY"):
		return (eval_(t.left.left, env, e) * eval_(t.right, env, e))
	if (cat == "DEVIDE"):
		return (eval_(t.left.left, env, e) / eval_(t.right, env, e))
	if (cat == "POWER"):
		return (eval_(t.left.left, env, e) ^ eval_(t.right, env, e))
	if (cat == "PERIOD"):
		return (eval_(t.left.left, env, e) . eval_(t.right, env, e))
	
		

