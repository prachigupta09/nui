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
#------------------------------------------------------------------------------
boardcss = '''
.square.light {             fill: #f2f2f2;                      }
.square.dark {              fill: #8c8c8c;                      }
.square.light.lastmove {    fill: #ced26b;                      }
.square.dark.lastmove {     fill: #aaa23b;                      }
.check {                    fill: url(#check_gradient);         }
'''

def main():
	start("localhost", 7777)

def start(host_addr, port_num):
	app = web.Application()
	chessgame = GameController()
	app.router.add_get("/", chessgame.get_root)
	app.router.add_get("/board.svg", chessgame.get_board)
	app.router.add_post("/move", chessgame.post_move)
	web.run_app(app, port=port_num, host=host_addr)

# Todo: Decouple the GameManager from the Game.
class GameController:
	
	# Initialize the game.
	def __init__(self):
		self.board = chess.Board()
		self.css = boardcss
	
	
	# Default route. Redirect to the board.
	@asyncio.coroutine
	def get_root(self, request):
	    return web.Response()
	    # What to do?
	
	
	# Responds to a GET request for the board.
	# Todo: Allow for parameters to alter the board.svg file?
	@asyncio.coroutine
	def get_board(self, request):
		return web.Response(text=self.render_board(request),
			content_type="image/svg+xml")
	
	
	# Responds to a POST request for a move.
	@asyncio.coroutine
	def post_move(self, request):
		data = yield from request.post()
		#print(data)
		# Apply the move. If it is successful, redirect to getting the board.
		rv = self.make_move(data)
		return web.Response(status=rv, text=self.render_board(request),
			content_type="image/svg+xml")
	
	
	# Returns the active board, in svg format.
	def render_board(self, request):
		return chess.svg.board(board=self.board, style=self.css)
		
		
	# Applies a post request move to the board. Returns status code if move invalid.
	def make_move(self, post_data):
		# If the post_data looks weird, it's because it's url encoded.
		# First, validate the paramters we need to make a move.
		try:
			piece = post_data["piece"]
		except (KeyError, ValueError):
			piece = ""
		try:
			from_square = post_data["from"]
		except (KeyError, ValueError):
			from_square = ""
		try:
			to_square = post_data["to"]
		except (KeyError, ValueError):
			raise web.HTTPBadRequest(reason="Parameter [to] not specified!")
		
		# Attempt to make the move.
		move_str = piece + from_square + to_square
		try:
			move = self.board.parse_san(move_str)
		except (ValueError):
			# Invalid move specified.
			prompt = "Move: " + move_str + " is invalid!\nValid moves are: " + str([str(move) for move in self.board.legal_moves])
			raise web.HTTPBadRequest(reason=prompt)
			
			
        if move in self.board.legal_moves:
            self.board.push(move)
            return 202
        else:
            #prompt = "Move: " + move_str + " is illegal!\nLegal moves are: " + str([str(move) for move in self.board.legal_moves])
            #prompt=""
            raise web.HTTPBadRequest(reason="")
            
			
			
	
if __name__ == "__main__":
	main()
	
	
	
	
	
	
	
