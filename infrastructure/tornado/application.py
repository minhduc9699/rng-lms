import os
import tornado.web
from tornado.options import options
from modules.ETL import ETLHandler


class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write({"Hello": "world"})

class FourOhFourHandler(tornado.web.RequestHandler):
  def get(self, slug):
    self.render("404.html")

class Application(tornado.web.Application):
    def __init__(self):
      handlers = [
        (r"/etls", ETLHandler),
        (r"/", MainHandler),
        (r"/([^/]+)", FourOhFourHandler),
      ]
      settings = dict(
        site_title=options.site_title,
        cookie_secret=options.cookie_secret,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
      )
      tornado.web.Application.__init__(self, handlers, **settings)
