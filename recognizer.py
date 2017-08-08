#By: jttew

from lexicalAnalyser import *
import string
import sys


class Recognizer:
    currentLexeme = None
    text = None
    finalTree = None


    def __init__(self, filename):
        self.text = Scanner(filename)
        self.advance()
        self.finalTree = self.optFuncDefClassList()

    def getTree(self):
        return self.finalTree

#Probably Done	
    def check(self, type_):
        x = self.currentLexeme.category
#		print("check", x, type_, (x[0] == type_))
        return(x == type_)

#Probably Done
    def advance(self):
        self.currentLexeme = self.text.lex()

#Maybe Done
    def match(self, type_):
#		print("Match", type_)
        self.matchNoAdvance(type_)
        x = self.currentLexeme
        self.advance()
        return x

#
    def matchNoAdvance(self, type_):
        if (self.check(type_) == False):
            sys.exit("syntax error" + " looking for " + str(type_) + " found " + self.currentLexeme.category)

#----------------------------------------------------------

#DONE
    def optFuncDefClassList(self):
        tree = Lexeme()
        tree.category = "TOPNODE" #this makes parse tree easier to read
        print("Hey from line 48" + str(self.currentLexeme.value) + str(self.currentLexeme.category))
        if self.classPending():
            print("class ln51 hello?")
            tree.left = self.class_()
            tree.right = self.optFuncDefClassList()
            return tree
        elif self.funcDefPending():
            print("funcDef ln54 Hello?")
            tree.left = self.funcDef()
            tree.right = self.optFuncDefClassList()
            print("If these next two lines are values then funcDef and optfuncdefclasslist are returning values, ln57")
            print(tree.left)
            print(tree.right)
            return tree
        elif (self.check("ENDofINPUT")):
            print("ENDOFINPUT ln62")
            return None
        return tree

#DONE
    def classPending(self):
        return self.check("CLASS")

#DONE
    def class_(self):
        tree = self.match("CLASS")
        tree.right = self.match("ID")
        tree.left = self.block()
        return tree
#NOTHING TO SEE HERE###INCORRECT###DOING WORKING FOR NOTHNG###
#		self.match("OBRACE")
#		tree.right = optFuncDefDeclList()
#		self.match("CBRACE")

#ADDING CLASSES CORRECTLY###I MEAN INCORRECTLY###
#	def optFuncDefDeclList():
#		tree = Lexeme()
#		tree.category = "FUNCORDECL"
#		if(self.funcDefPending()):
#			tree.left = self.funcDef()
#			tree.right = self.optFuncDefDeclList()
#			return tree
#		elif(self.declPending()):

#DONE
    def funcDefPending(self):
        return self.check("DEFINE")

#DONE
    def funcDef(self):
        print("FUNCDEF ln82")
        tree = Lexeme()
        tree.category = "FUNC"
        self.match("DEFINE")
        tree.left = self.match("ID")
        self.match("OPAREN")
        tree.left.right = self.optPeramList()
        self.match("CPAREN")
        tree.right = self.block()
        return tree

#DONE	THIS MIGHT NEED TO CHECK FOR PRIMARIES
    def optPeramList(self):
        if(self.check("ID")):
            tree = self.match("ID")
            if(self.check("COMMA")):
                self.match("COMMA")
                tree.right = self.peramList()
            return tree
        else: return None

#DONE
    def peramList(self):
        tree = self.match("ID")
        if(self.check("COMMA")):
            self.match("COMMA")
            tree.right = self.peramList()
        return tree
#DONE
    def block(self):
        self.match("OBRACE")
        tree = self.optDeclList()
        self.match("CBRACE")
        return tree

#Done
    def optDeclList(self):
        tree = None
        if(self.declPending()):
            ###########################
            tree = self.declList()
        return tree

#Done	
    def declList(self):
        tree = self.decl()
        if(self.declPending()):
            tree.right = self.declList()
        return tree

#DONE
    def declPending(self):
        return(self.funcDefPending() or \
        self.conditionalPending() or self.varDeclPending() \
         or self.exprPending() or self.check("PRINT"))

#DONE?		
    def decl(self):
        tree = Lexeme()
        tree.category = "DECL"
        if(self.funcDefPending()):
            tree.left = self.funcDef()
            return tree
        elif(self.conditionalPending()):
            tree.left = self.conditional()
            return tree
        elif(self.varDeclPending()):
            tree.left = self.varDecl()
            return tree
        elif(self.check("PRINT")):
            new = Lexeme()
            new.category = "PRINT"
            self.match("PRINT")
            self.match("OPAREN")
            new.left = self.primaryList()
            print(str(new.left) + " is on the left of Print")
            self.match("CPAREN")
            self.match("SEMICOLON")
            tree.left = new
            return tree
        else:
            tree.left = self.expr()
            return tree
        sys.exit("Bad decl")


#DONE
    def varDeclPending(self):
        return self.check("MAKE")

#DONE
    def varDecl(self):
        tree = Lexeme()
        tree.category = "VARDECL"
        self.match("MAKE")
        tree.left = self.match("ID")
        self.match("ASSIGN")
        tree.right = self.expr()#matches semicolon
        return tree

#
    def exprPending(self):
        return self.primaryPending()

#Done MAKE EXPR LEXEME
    def expr(self):
        tree = self.primary()
        if(self.opPending()):
            temp = self.op()
            temp.left.left = tree
            temp.right = self.exprWithoutSemi()
            tree = temp
        print("Semicolon: " + str(self.currentLexeme.value))
        self.match("SEMICOLON")
        return tree

    def exprWithoutSemi(self):
        tree = self.primary()
        if(self.opPending()):
            temp = self.op()
            temp.left.left = tree
            temp.right = self.exprWithoutSemi()
            tree = temp
        return tree

#DONE
    def primaryPending(self):
        return(self.check("STRING") or self.check("INTEGER") or self.check("TRUE") or self.check("FALSE") or self.check("ID") or self.check("OPAREN"))

 #DONE?
    def primary(self):
        tree = Lexeme()
        tree.category = "PRIMARY"
#"Hello."
        if(self.check("STRING")):
            tree.left = self.match("STRING")
#123
        elif(self.check("INTEGER")):
            tree.left = self.match("INTEGER")
            #if(self.check("PERIOD")):
            #	self.match("PERIOD")
            #	self.match("INTEGER")
#True
        elif(self.check("TRUE")):
            tree.left = self.match("TRUE")
#False
        elif(self.check("FALSE")):
            tree.left = self.match("FALSE")
#Null
        elif(self.check("NULL")):
            tree.left = self.match("NULL")
#(1+(2*3+4))
        elif(self.check("OPAREN")):
            tree.left = Lexeme()
            tree.left.category = "PAREN"
            self.match("OPAREN")
            tree.left.left = self.exprWithoutSemi()
            self.match("CPAREN")
#{1,2,3,4} IMPLEMENT LISTS, CHANGE BRACKET{ BRACE[ and Paren ( to be correct
        elif(self.check("OBRACKET")):
            tree.left = self.list_()

#add2(4)
        else:
            #self.funcCall()
            #this matches IDs and funcCalls at once
            tree.left = self.match("ID")
            if self.check("OPAREN"):
                temp = Lexeme()
                temp.category = "FUNCCALL"
                self.match("OPAREN")
                temp.right = self.optPrimaryList()
                self.match("CPAREN")
                temp.left = tree.left
                tree.left = temp
        return tree


    def list_(self):
        print("yo im a list")
        tree = Lexeme()
        tree.category = "LIST"
        self.match("OBRACKET")
        if(self.check("CBRACKET") == False):
            tree.left = self.optList()
        self.match("CBRACKET")
        return tree

    def optList(self):
        print("yo im inside the list mane")
        tree = Lexeme()
        tree.category = "OPTLIST"
        tree.left = self.primary()
        if(self.check("COMMA")):
            self.match("COMMA")
            tree.right = self.optList()
        return tree

#DONE NOT TESTED
    def optPrimaryList(self):
        tree = None
        if(self.primaryPending()):
            tree = Lexeme()
            tree.category = "PRIMARYLIST"
            tree.left = self.primary()
            if(self.check("COMMA")):
                self.match("COMMA")
                tree.left.right = self.primaryList()
        return tree

#DONE NOT TESTED
    def primaryList(self):
        tree = Lexeme()
        tree.category = "PRIMARYLIST"
        tree.left = self.primary()
        if(self.check("COMMA")):
            self.match("COMMA")
            tree.left.right = self.primaryList()
        return tree

#The new version is about 15 lines up, I put it inside primary
#	def funcCall(self):
#		self.match("ID")
#		self.match("OPAREN")
#		self.optPeramList()
#		self.match("CPAREN")

#DONE
    def opPending(self):
        return(self.check("PLUS") or self.check("MINUS") or self.check("DEVIDE") or self.check("MULTIPLY") or self.check("PERIOD") or self.check("POWER") or self.logicPending())

#DONE
    def op(self):
        tree = Lexeme()
        tree.category = "OP"
        if(self.check("PLUS")):
            tree.left = self.match("PLUS")
        elif(self.check("MINUS")):
            tree.left = self.match("MINUS")
        elif(self.check("DEVIDE")):
            tree.left = self.match("DEVIDE")
        elif(self.check("MULTIPLY")):
            tree.left = self.match("MULTIPLY")
        elif(self.check("PERIOD")):
            tree.left = self.match("PERIOD")
        elif(self.check("POWER")):
            tree.left = self.match("POWER")
        else:
            tree.left = self.logic()
        return tree

#
    def logicPending(self):
        return (self.check("LESSTHAN") or (self.check("GREATERTHAN")) or (self.check("ASSIGN")))

#DONE
    def logic(self):
        tree = Lexeme()
        tree.category = "LOGIC"
        if(self.check("LESSTHAN")):
            self.match("LESSTHAN")
            tree.value = "<"
            if(self.check("ASSIGN")):
                self.match("ASSIGN")
                tree.value = "<="
            if(self.check("GREATERTHAN")):
                self.match("GREATERTHAN")
                tree.value = "<>"
            return tree
        elif(self.check("GREATERTHAN")):
            self.match("GREATERTHAN")
            tree.value = ">"
            if(self.check("ASSIGN")):
                self.match("ASSIGN")
                tree.value = ">="
            return tree
        elif(self.check("ASSIGN")):
            tree.value = "="
            if(self.check("ASSIGN")):
                self.match("ASSIGN")
                tree.value = "=="
            return tree
        return None

#
    def conditionalPending(self):
        return (self.check("WHILE") or self.check("IF"))

#DONE
    def conditional(self):
        if(self.check("WHILE")):
            return self.while_()
        else:
            return self.if_()

#DONE	
    def while_(self):
        tree = self.match("WHILE")
        self.match("OPAREN")
        tree.left = self.exprWithoutSemi()
        self.match("CPAREN")
        tree.right = self.block()
        return tree

#DOEN
    def if_(self):
        tree = self.match("IF")
        self.match("OPAREN")
        tree.left = self.exprWithoutSemi()
        self.match("CPAREN")
        tree.right = Lexeme()
        tree.right.category = "BLOCKOPTELSE"
        tree.right.left = self.block()
        tree.right.right = self.optElse()
        return tree

#DONE
    def optElse(self):
        tree = None
        if(self.check("ELSE")):
            tree = self.match("ELSE")
            tree.left = self.block()
        return tree


def printTree(tree, num, depth): #num for formatting depth for printing
    if (num >= 0):
        print(string.rjust("Lexeme: " + str(tree.category) + ", " + str(tree.value) + ", " + str(depth) + " " * num ,55))
    else:
        print(string.rjust("Lexeme: " + str(tree.category) + ", " + str(tree.value) + ", " + str(depth),55 - num))
    if(tree.left != None):
        #print("LEFT " + str(num))
        printTree(tree.left, num + 1, depth + 1)
    if(tree.right != None):
        print("RIGHT " + str(depth))
        printTree(tree.right, num - 1, depth + 1)

#def main():
#	filename = sys.argv[1]
#	x = Recognizer(filename)
#	print("KEY: LEXEME: type, value, depth")
#	print("No RIGHT means LEFT pointer.  The RIGHT has a number which corresponds with depth of the node it is RIGHT of.")
#	printTree(x.getTree(), 0, 0)
#
#main()

#def main():
#	filename = sys.argv[1]
#	x = Recognizer(filename)
#
#main()
