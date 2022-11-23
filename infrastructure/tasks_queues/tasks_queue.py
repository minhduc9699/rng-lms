from tornado.queues import Queue
import json
import tornado.gen

class TaskQueue():
  queued_update = None

  @classmethod
  def setup(cls):
    cls.queued_update = Queue()

  @classmethod
  @tornado.gen.coroutine
  def run_job(cls):
    if not cls.queued_update:
      raise Exception('Not initialized')
    else:
      while True:
        try:
          message = yield cls.queued_update.get()
          print('running queue')
          print(message)
          job = message['job']
          data = message['data']
          if job: job(data)
        except Exception as errors:
          raise Exception(errors)
