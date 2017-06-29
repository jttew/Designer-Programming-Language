#!/usr/bin/env python

#By: jttew

#This goes through a text file, converts it to tokens, and prints them in order.

import string
import sys

class Scanner:
	name = ''
	#a = None, use this in funcs as a lexer obj

	def __init__(self, filename):
		self.name = filename
		self.a = Lexer(self.name)

	def lex(self):
		return self.a.lex()
			
	def scan(self):
		LexemeList = []
		token = self.a.lex()
		while(token.category != "ENDofINPUT"):
			#print(token.category, token.value)
			LexemeList.append(token)
			token = self.a.lex()
		return LexemeList

class Lexer:
	tokens = [] #I put tokens here
	tokenType = []
	#tokenLineNumbers = [] #see line 94
	currentlyString = False

	def __init__(self, filename):
		 #open and read the file	
		op = open(filename, 'r')
		rawLines = op.readlines()
		op.close() 
		lines = []
		for line in rawLines:
			lines += [line.strip()]
		self.treat(lines)

	 #calls treatLine for each line
	def treat(self, lines):
		lineNum = 0
		for line in lines:
			self.treatLine(line, lineNum)
			lineNum += 1
	
	 #finds the positions of each item		
	def treatLine(self, line, number):
		tokenPositions = []
		currentlyChars = False
		currentlyComment = False
		if(self.currentlyString == True):
			sys.exit()
		for spot in range(len(line)):
#			 #comments
#			if(line[spot] == '#'):
#				if (self.currentlyString == False):
#				currentlyComment = True
#			if(currentlyComment == True):
#				tempLine = list(line)
#				tempLine[spot] = " "
#				line = ''.join(tempLine)
			 #while in string
			if(self.currentlyString == True):
				if (line[spot] == '"'):
					tokenPositions += [spot + 1]
					self.currentlyString = False
			 ###
			 #whtespace
			elif(line[spot] == ' '):
				if currentlyChars == True:
					tokenPositions += [spot]
					currentlyChars = False
			 #string start
			elif(line[spot] == '"'):
				if currentlyChars == True:
					tokenPositions += [spot]
					currentlyChars = False
				tokenPositions += [spot]
				self.currentlyString = True
			 #punctuation
			elif(line[spot] in string.punctuation):
				if currentlyChars == True:
					tokenPositions += [spot]
					currentlyChars = False
				tokenPositions += [spot]
				tokenPositions += [spot + 1]
			 #letter or number
			else:
				if currentlyChars == False:
					tokenPositions += [spot]
					currentlyChars = True
		 #adding the last position if it is not punctuation
		if(len(line) > 0):
			if(line[-1] in string.punctuation):
				pass
			else:
				tokenPositions += [len(line)]
		 #converting locations to tokens
		tokPosLength = len(tokenPositions)
		token = []
		for x in range(0, tokPosLength, 2):
			self.tokens += [line[tokenPositions[x]:tokenPositions[x+1]]]
			#self.tokenLineNumbers += [number]

	 #pop each item and find what type it is
	def lex(self):
		try:
			l = Lexeme()
			l.token = self.tokens.pop(0)
			punct = l.punctDict.get(l.token, 0)
			term = l.termDict.get(l.token, 0)
			if(punct != 0):
				l.value = l.token
				l.category = punct
				return l 
			elif(l.token.isdigit()):
				l.value = int(l.token)
				l.category = "INTEGER"
				return l
			elif(l.token[0] == '"'):
				l.value = l.token
				l.category = "STRING"
				return l
			elif(term != 0):
				l.value = l.token
				l.category = term
				return l
			else:
				l.value = l.token
				l.category = "ID"
				return l
		except IndexError: #for pop()
			x = Lexeme()
			x.category = "ENDofINPUT"
			return x	
	

class Types:
	punctDict = {
	'(' : "OPAREN",
	')' : "CPAREN",
	'[' : "OBRACE", #yes i know these are brackets
	']' : "CBRACE", 
	'{' : "OBRACKET", #and these are braces
	'}' : "CBRACKET",
	'.' : "PERIOD",
	',' : "COMMA",
	'+' : "PLUS",
	'-' : "MINUS",
	'*' : "MULTIPLY",
	'/' : "DEVIDE",
	'^' : "POWER",
	'%' : "MOD",
	'<' : "LESSTHAN",
	'>' : "GREATERTHAN",
	'=' : "ASSIGN",
	'!' : "NOT",
	';' : "SEMICOLON"
	}
	
	termDict = {
	'if' : "IF",
	'else' : "ELSE",
	'while' : "WHILE",
	'def' : "DEFINE",
	'Null' : "NULL",
	'True' : "TRUE",
	'False' : "FALSE",
	'class' : "CLASS",
	'make' : "MAKE",
	'print' : "PRINT"
	}

class Lexeme(Types):
	token = 0
	category = None
	value = None
	left = None
	right = None
	
	

 #defining and calling main
#def main():
#	filename = sys.argv[1]
#	x = Scanner(filename)
#	y = x.scan()
#	for each in y:
#		print(each.category, each.value)
#
#
#main()
