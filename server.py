import os
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from infrastructure.tasks_queues.tasks_queue import TaskQueue
from infrastructure.tornado import application

# APIs

define("environment", default="development", help="Pick you environment", type=str)
define("site_title", default="Tornado Example", help="Site Title", type=str)
define("cookie_secret", default="sooooooosecret", help="Your secret cookie dough", type=str)
define("port", default="8000", help="Listening port", type=str)


def main():
  tornado.options.parse_command_line()
  print("Server listening on port " + str(options.port))
  logging.getLogger().setLevel(logging.DEBUG)
  TaskQueue.setup()
  tornado.ioloop.IOLoop.current().add_callback(TaskQueue.run_job)
  http_server = tornado.httpserver.HTTPServer(application.Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
  main()
