#~/usr/bin/python
import sys
import argparse
import os
# Using sonovice's implementation of the pdollar recognition engine.
# https://github.com/sonovice/dollarpy
# Included in this project as "dollarpy.py"
from dollarpy import Recognizer, Template, Point

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
	# Clears out the file "templates.dat"
	open("templates.dat", 'w').close()
	print("Templates list cleared!")
	
def add(gesturefile):
	# Adds the gesturefile's full path to the reference file of templates.
	fullpath = os.path.abspath(gesturefile)
	tf = open("templates.dat", 'a')
	tf.write(fullpath + "\n")
	tf.close()
	print("Template from " + gesturefile + " added!")
	
	
def read(eventstream):
	# Train the recognizer on the list of template files,
	# then execute the recognizer on the eventstream file.
	# -------------------------------------------------------------------------
	tf = open("templates.dat", 'r')
	templates = []
	for raw_lines in tf:
		line = raw_lines.strip()
		touch_num = 0
		gf = open(line, 'r')
		gname = gf.readline().strip()
		gpoints = []
		for lines in gf:
			gfline = lines.strip()
			if gfline == "BEGIN":
				touch_num += 1
			elif gfline == "END":
				continue
			else:
				x,y = int(gfline.split(',')[0]), int(gfline.split(',')[1])
				gpoints.append(Point(x, y, touch_num))
		t = Template(gname, gpoints)
		templates.append(t)
		gname = ""
		gpoints = []
	recog = Recognizer(templates)
	# -------------------------------------------------------------------------
	# Extract the necessary points from the event stream.
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
	    print(gname)



# Entry point of the application
if __name__=="__main__":
	main(sys.argv)