from tornado.queues import Queue
from azure import create_related_task_if_needed, notify_telegram_group
import json
import tornado.gen
import time

class AzureTaskQueue():
  queued_update = None

  @classmethod
  def setup(cls):
    cls.queued_update = Queue()

  @classmethod
  @tornado.gen.coroutine
  def run_azure_worker(cls):
    if not cls.queued_update:
      raise Exception('Not initialized')
    else:
      while True:
        try:
          update = yield cls.queued_update.get()
          create_related_task_if_needed(update)
          notify_telegram_group(update)
          with open('update_2.json', 'w') as f:
            f.write(json.dumps(update))
        except Exception as errors:
          raise Exception(errors)
