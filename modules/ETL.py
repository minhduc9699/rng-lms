import tornado.web
from addict import Dict
import json
from infrastructure.tasks_queues.tasks_queue import TaskQueue
from infrastructure.mysql.main import get_connection
# from domains.main import ETL
import tornado.gen


def save_students(students):
  # students = {
  #   ... in sql tables
  # }
  connection = get_connection()
  # SQL COMMAND 
  # Insert into....
  return

def save_classes(classes):
  connection = get_connection()
  # SQL COMMAND 
  # Insert into...
  return

def save_headcount(headcount):
  connection = get_connection()
  # SQL COMMAND 
  # Insert into...
  return

job_map = {
  'classes': save_classes,
  'students': save_students,
  'headcount': save_headcount,
}


class ETLHandler(tornado.web.RequestHandler):

  def get(self, students):
    # INPUT
    # students = {
    #   'id':
    #   'name':
    #   ...
    # }
    # Process
    save_students(students)
    # OUTPUT
    self.write({"Hello": "ETL"})
  
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
