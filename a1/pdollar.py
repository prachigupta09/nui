#~/usr/bin/python3
import sys
import argparse
# Using sonovice's implementation of the pdollar recognition engine.
# https://github.com/sonovice/dollarpy
# Included in this project as "dollarpy.py"
from dollarpy import Recognizer, Template, Point

import pdb

def main(argv):
	p = argparse.ArgumentParser()
	p.add_argument("-t", 
		help="add a gesture template to the recognizer",
		metavar="<gesturefile>")
	p.add_argument("-r", 
		help="resets the recognition engine", 
		action="store_true")
	p.add_argument("estream", 
		help="Prints the name of gestures as they are recognized from the event stream",
		metavar="<eventstream>",
		nargs="?") # makes this argument appear optional
	
	args = p.parse_args(sys.argv[1:])
	if(args.r):
		# Reset the engine.
		reset()
	elif(args.t != None):
		# Add the gesture file to the training set
		add(args.t)
	elif(args.estream != None):
		# Read gestures from the event stream file
		read(args.estream)
	else:
		# Formatting was incorrect
		p.print_help()


def reset():
	print("resetting engine...")
	
	
def add(gesturefile):
	print("adding new gesture template:", gesturefile)
	
	
def read(eventstream):
	print("streaming events from file:", eventstream)
	





















# Entry point of the application
if __name__=="__main__":
	main(sys.argv)

