import os
import tornado.web
from addict import Dict
import json
from task_queues.azure_task_queue import AzureTaskQueue
import tornado.gen

class CrmAzureHandler(tornado.web.RequestHandler):

  def get(self):
    self.write({"Hello": "crm/azure"})
  
  @tornado.gen.coroutine
  def post(self):
    update = Dict(json.loads(self.request.body))
    yield AzureTaskQueue.queued_update.put(update)
    self.write(json.loads(self.request.body))
