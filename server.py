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
from task_queues import azure_task_queue
from cronjob import daily_scrum_reminder

# APIs
from api.azure import CrmAzureHandler
from api.worker_heartbeat import WorkerHeartBeatHandler

define("environment", default="development", help="Pick you environment", type=str)
define("site_title", default="Tornado Example", help="Site Title", type=str)
define("cookie_secret", default="sooooooosecret", help="Your secret cookie dough", type=str)
define("port", default="8000", help="Listening port", type=str)

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write({"Hello": "world"})

class FourOhFourHandler(tornado.web.RequestHandler):
  def get(self, slug):
    self.render("404.html")

class Application(tornado.web.Application):
    def __init__(self):
      handlers = [
        (r"/workers:heartbeat", WorkerHeartBeatHandler),
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
  daily_scrum_reminder.sched.start()
  tornado.options.parse_command_line()
  print("Server listening on port " + str(options.port))
  logging.getLogger().setLevel(logging.DEBUG)
  azure_task_queue.AzureTaskQueue.setup()
  tornado.ioloop.IOLoop.current().add_callback(azure_task_queue.AzureTaskQueue.run_azure_worker)
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
  main()
