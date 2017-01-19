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
		help="adds the gesture file to the list of gesture templates",
		metavar="<gesturefile>")
	p.add_argument("-r",
		help="clears the templates",
		action="store_true")
	p.add_argument("estream",
		help="prints the name of gestures as they are recognized from the event stream",
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
	open("templates.dat", 'w').close()
	print("Templates list cleared!")
	
def add(gesturefile):
	gf = open(gesturefile, 'r')
	tf = open("templates.dat", 'a')
	for line in gf:
		tf.write(line)
	gf.close(), tf.close()
	print("Templates added from file: ", gesturefile)
	
	
def read(eventstream):
	# --- Gesture file format ---
	# GestureName
	# BEGIN
	# x,y
	# ...
	# BEGIN
	# ...
	# x,y
	# END
	# --- Event stream format ---
	# MOUSEDOWN
	# x,y
	# ...
	# x,y
	# MOUSEUP
	# MOUSEDOWN
	# x,y ...
	# MOUSDOWN
	# RECOGNIZE
	# MOUSEDOWN
	# ...
	# MOUSEUP
	# RECOGNIZE
	'''
	# Train the recognizer on the list of templates.
	tf = open("templates.dat", 'r')
	state = 0
	gname = ""
	gpoints = []
	templates = []
	touch_num = 0
	for line in tf:
		if line == "\n":
			continue
		if state == 0:
			# The line is the gesture name.
			gname = line.strip()
			state = 1
		elif state == 1:
			# The line is "BEGIN", skip it.
			state = 2
		elif state == 2:
			# The line is either an (x,y), or "END".
			if line.strip() == "END":
				# Add the gesture template.
				t = Template(gname, gpoints)
				#print("Recognizer trained on gesture: ", gname)
				templates.append(t)
				gname = ""
				gpoints.clear()
				touch_num += 1
				state = 0
			else:
				points = line.strip().split(',')
				x, y = int(points[0]), int(points[1])
				gpoints.append(Point(x, y, touch_num))
	recog = Recognizer(templates)
	pdb.set_trace()
	# Extract the necessary points from the event stream.
	'''
	gestures = []   # list of lists of points
	gesture = []    # list of points
	touch_num = 0
	es = open(eventstream, 'r')
	for raw_line in es:
	    line = raw_line.strip()
	    if line == "MOUSEDOWN":
	        touch_num += 1
	    elif line == "MOUSEUP":
	        continue
	    elif line == "RECOGNIZE":
	        # It's assumed recognize clears after recognition.
	        gestures.append(gesture)
	        gesture = []
	        touch_num = 0
	    else:
	        x,y = int(line.split(',')[0]), int(line.split(',')[1])
	        gesture.append(Point(x, y, touch_num))
	es.close()
	for gesture in gestures:
	    gname, accuracy = recog.recognize(gesture)
	    print gname










# Entry point of the application
if __name__=="__main__":
	main(sys.argv)

