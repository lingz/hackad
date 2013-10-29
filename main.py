import os.path
from live_stylus import ConvStylus

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("index.html")

class Hack72Handler(tornado.web.RedirectHandler):
  def get(self):
    self.render("hack72.html")
  
  def initialize(self):
    pass

if __name__ == '__main__':
  ConvStylus(os.path.join(os.path.dirname(__file__), "static/css/"))
  tornado.options.parse_command_line()
  app = tornado.web.Application(
    handlers=[(r'/', IndexHandler), (r'/hack72', Hack72Handler)],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True
  )
  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
