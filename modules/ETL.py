import tornado.web
from addict import Dict
import json
from infrastructure.tasks_queues.tasks_queue import TaskQueue
from domains.main import ETL
import tornado.gen

class ETLHandler(tornado.web.RequestHandler):

  def get(self):
    self.write({"Hello": "ETL"})
  
  @tornado.gen.coroutine
  def post(self):
    update = Dict(json.loads(self.request.body))
    message = {
      **update,
      'job': ETL,
    }
    yield TaskQueue.queued_update.put(message)
    self.write(json.loads(self.request.body))
