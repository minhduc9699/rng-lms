import os
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import json
from addict import Dict
from telegram import post

define("environment", default="development", help="Pick you environment", type=str)
define("site_title", default="Tornado Example", help="Site Title", type=str)
define("cookie_secret", default="sooooooosecret", help="Your secret cookie dough", type=str)
define("port", default="8000", help="Listening port", type=str)

with open('config.json') as config_file:
  config_file_content = config_file.read()
  config = json.loads(config_file_content)
  telegram_routes = { route['projectId']: route for route in config['telegramRoutes']}

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write({"Hello": "world"})

class CrmAzureHandler(tornado.web.RequestHandler):
  def get(self):
    self.write({"Hello": "crm/azure"})
  def post(self):
    update = Dict(json.loads(self.request.body))
    project_id = update.resourceContainers.project.id
    try:
      chat_id = telegram_routes[project_id]['chatId']
      post(update.detailedMessage.markdown.replace("*", ""), chat_id, "Markdown")
    except KeyError:
      print('Error: "projectId" NOT found')
    self.write(json.loads(self.request.body))

class FourOhFourHandler(tornado.web.RequestHandler):
  def get(self, slug):
    self.render("404.html")

class Application(tornado.web.Application):
    def __init__(self):
      handlers = [
        (r"/azure", CrmAzureHandler),
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

def main():
  tornado.options.parse_command_line()
  print("Server listening on port " + str(options.port))
  logging.getLogger().setLevel(logging.DEBUG)
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
