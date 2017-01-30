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
    #service = Service(args.css.read() if args.css else None)
    #app.router.add_get("/board.png", service.render_png)
    #app.router.add_get("/board.svg", service.render_svg)
	app.router.add_get("/", handle)
	
	web.run_app(app, port=port_num, host=host_addr)

	
class Game:
	def __init__(self):
		self.css == chess.svg.DEFAULT_STYLE
	
	def get_board(self, request):
		
	
	def post_move(self, request):
	
	
	


if __name__ == "__main__":
	main()