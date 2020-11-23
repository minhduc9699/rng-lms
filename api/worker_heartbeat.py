import os
import tornado.web
from env.config import Config
from addict import Dict
import json


class WorkerHeartBeatHandler(tornado.web.RequestHandler):

  def get(self):
    with open ('worker_heartbeat.json') as f:
      data = json.loads(f.read())
      print(data)
    self.write(data)
  
  def post(self):
    update = json.loads(self.request.body)
    with open('worker_heartbeat.json', 'w') as f:
      f.write(json.dumps(update))
    self.write(json.loads(self.request.body))
