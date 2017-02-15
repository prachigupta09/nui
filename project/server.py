#!/usr/bin/env python
#------------------------------------------------------------------------------
# Objectives:
# 1. Make a webserver that hosts a game of chess.
#	 This requires being able to show the user the board.
# 2. Make a speech recognition client that can interpret commands to AN moves
# 3. Enhance the client to make calls to the webserver running chess.
#------------------------------------------------------------------------------
# Libraries:
# Inspired by https://github.com/niklasf/web-boardimage
# Reference http://python-chess.readthedocs.io/en/v0.16.2/core.html
from aiohttp import web
import asyncio
import chess
import chess.svg
import subprocess
#------------------------------------------------------------------------------
boardcss = '''
.square.light {             fill: #e6e6e6;                      }
.square.dark {              fill: #8c8c8c;                      }
.square.light.lastmove {    fill: #ced26b;                      }
.square.dark.lastmove {     fill: #aaa23b;                      }
.check {                    fill: url(#check_gradient);         }
'''
HOSTNAME = "thunder.cise.ufl.edu"
PORT = 7777


def main():
	start(HOSTNAME, PORT)

def start(host_addr, port_num):
	app = web.Application()
	chessgame = GameController()
	app.router.add_get("/", chessgame.get_root)
	app.router.add_get("/board.png", chessgame.get_board)
	app.router.add_post("/move", chessgame.post_move)
	app.router.add_post("/undo", chessgame.post_undo)
	web.run_app(app, port=port_num, host=host_addr)
	
def svg2png(raw_svg, width=400):
	# Converts raw_svg data (in xml format) to png bytes.
	ifile = "board.svg"
	ofile = "board.png"
	with open(ifile, "w") as f:
		f.write(raw_svg)
	subprocess.call(['inkscape', '-z', '-f', ifile, '-w', str(width), '-j', '-e', ofile])
	with open("board.png", "rb") as f:
		raw_png = f.read()
	return raw_png


class GameController:
	
	# Initialize the game.
	def __init__(self):
		self.board = chess.Board()
		self.css = boardcss
	
#----[Routes for the web application]------------------------------------------

	# Default route. Redirect to the board.
	@asyncio.coroutine
	def get_root(self, request):
		self.board = chess.Board()
		return web.HTTPFound("/board.png#newgame")
	
	
	# Responds to a GET request for the board.
	# Todo: Allow for parameters to alter the board.svg file?
	@asyncio.coroutine
	def get_board(self, request):
		#return web.Response(text=self.render_board(True), content_type="image/svg+xml")
		return web.Response(body=self.render_board(True), content_type="image/png")
	
	# Responds to a POST request for making a move.
	@asyncio.coroutine
	def post_move(self, request):
		data = yield from request.post()
		# Apply the move. If it is successful, redirect to getting the board.
		rv = self.make_move(data)
		return web.HTTPFound("/board.png")
		
	@asyncio.coroutine
	def post_undo(self, request):
	    self.undo_move()
	    return web.HTTPFound("/board.png")

#----[Game functions, called by routes]----------------------------------------
	
	# Returns the active board, in svg format.
	# Now returns the board in PNG format!
	def render_board(self, hint=False):
		next_moves = chess.SquareSet()
		if hint:
			for move in self.board.legal_moves:
				next_moves.add(move.to_square)
		# Conversion code:
		raw_svg = chess.svg.board(board=self.board, squares=next_moves, style=self.css)
		return svg2png(raw_svg)
		
		
	# Applies a post request move to the board. Returns status code if move invalid.
	def make_move(self, post_data):
		# If the post_data looks weird, it's because it's url encoded.
		# First, validate the paramters we need to make a move.
		try:
			piece = post_data["piece"].upper()
		except (KeyError, ValueError):
			raise web.HTTPBadRequest(reason="Parameter [piece] not specified!")
		
		try:
			to_square = post_data["to"].lower()
		except (KeyError, ValueError):
			raise web.HTTPBadRequest(reason="Parameter [to] not specified!")
		
		# The parameter from is either a piece or a position.
		move_str = piece + to_square
		my_legal_moves = [str(self.board.piece_at(move.from_square)).upper()
			+ chess.SQUARE_NAMES[move.to_square]
			for move in self.board.legal_moves]
		
		# Check if the move is a valid formatted move.
		try:
			if move_str[0] == "P":
				move = self.board.parse_san(move_str[1:])
			else:
				move = self.board.parse_san(move_str)
		except (ValueError):
			# Invalid move specified.
			prompt = "Move: " + move_str + " is invalid!\nValid moves are: " + str(my_legal_moves)
			raise web.HTTPBadRequest(reason=prompt)
		# Check if the move is legal.
		if move in self.board.legal_moves and move_str in my_legal_moves:
			self.board.push(move)
			return 202
		else:
			prompt = "Move: " + move_str + " is illegal!\nLegal moves are: " + str(my_legal_moves)
			raise web.HTTPBadRequest(reason=prompt)
            

	def undo_move(self):
	    if len(self.board.move_stack) > 0:
	        self.board.pop()
			
	
if __name__ == "__main__":
	main()
	
	
	
	
	
	
	
