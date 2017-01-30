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
from aiohttp import web
import asyncio
import chess
import chess.svg




def main():
	start("127.0.0.1", 7777)

def start(host_addr, port_num):
	app = web.Application()
	chessgame = Game()
    #service = Service(args.css.read() if args.css else None)
    #app.router.add_get("/board.png", service.render_png)
    #app.router.add_get("/board.svg", service.render_svg)
	app.router.add_get("/", chessgame.get_board)
	
	web.run_app(app, port=port_num, host=host_addr)

# Todo: Decouple the GameManager from the Game.
class Game:
	
	# Initialize the game. 
	def __init__(self):
		self.board = chess.Board()
		self.css = chess.svg.DEFAULT_STYLE
	
	
	# Responds to a GET request for the board.
	# Todo: Allow for parameters to alter the board.svg file?
	@asyncio.coroutine
	def get_board(self, request):
		return web.Response(text=self.render_board(request), 
			content_type="image/svg+xml")
	
	
	# Responds to a POST request for a move.
	@asyncio.coroutine
	def post_move(self, request):
		# Apply the move. If it is successful, redirect to getting the board.
		return web.Response()
		pass
	
	
	# Returns the active board, in svg format.
	def render_board(self, request):
		return chess.svg.board(board=self.board, style=self.css)

	
if __name__ == "__main__":
	main()
	
	
	
	
	
	
	
