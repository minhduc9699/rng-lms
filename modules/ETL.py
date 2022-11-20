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
    update = Dict(json.loads(self.request.body))
    message = {
      **update,
      'job': self.get,
    }
    yield TaskQueue.queued_update.put(message)
    self.write(json.loads(self.request.body))
