from recognizer import *

def main():
        filename = sys.argv[1]
        x = Recognizer(filename)
        print("KEY: LEXEME: type, value, depth")
        print("No RIGHT means LEFT pointer.  The RIGHT has a number which corresponds with depth of the node it is RIGHT of.")
        printTree(x.getTree(), 0, 0)

main()


