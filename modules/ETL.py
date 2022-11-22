import tornado.web
from addict import Dict
import json
from infrastructure.tasks_queues.tasks_queue import TaskQueue
from domains.main import save_classes, save_headcount, save_students
# from domains.main import ETL
import tornado.gen

job_map = {
  'classes': save_classes,
  'students': save_students,
  'headcount': save_headcount,
}

class ETLHandler(tornado.web.RequestHandler):

  @tornado.gen.coroutine
  def post(self):
    body = Dict(json.loads(self.request.body))
    job_type = body['job_type']
    data = body['data']
    message = {
      data: data,
      'job': job_map[job_type],
    }
    yield TaskQueue.queued_update.put(message)
    self.write(json.loads(self.request.body))
