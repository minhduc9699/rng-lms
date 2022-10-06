import os
import tornado.web
from addict import Dict
import json
import tornado.gen
import telegram
from prometheus import get_vps_metrics

class SentryHandler(tornado.web.RequestHandler):

  def get(self):
    self.write({"Hello": "crm/sentry"})
  
  @tornado.gen.coroutine
  def post(self):
    update = Dict(json.loads(self.request.body))
    payload = update["data"]
    telegram.post(f'''{payload["description_title"]}\n{payload["description_text"]}''', -568254725)
    vps_metrics = get_vps_metrics('45.117.83.246:9100', 'Production')
    mgs = "{:_<20} {:_<30} {:_<10}\n".format('Label', 'Timestamp', 'Value')
    for metrics in vps_metrics:
      mgs += "{:_<20} {:_<30} {:_<10}\n".format(metrics['label'], metrics['timestamp'], metrics['value'])
    telegram.post(mgs, -568254725,'html')
    self.write({'update': update})