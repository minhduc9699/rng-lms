import os
import tornado.web
from addict import Dict
import json
import tornado.gen
import telegram
from prometheus import get_vps_metrics
from env.config import Config


class SentryHandler(tornado.web.RequestHandler):

  def get(self):
    self.write({"Hello": "crm/sentry"})
  
  @tornado.gen.coroutine
  def post(self):
    vps_info = Config.get().sentry
    update = Dict(json.loads(self.request.body))
    payload = update["data"]
    telegram.post(f'''{payload["description_title"]}\n{payload["description_text"]}''', -568254725)
    vps_metrics = get_vps_metrics(vps_info['nodeExporter'], vps_info['vpsName'])
    mgs = "{:_<20} {:_<30} {:_<10}\n".format('Label', 'Timestamp', 'Value')
    for metrics in vps_metrics:
      mgs += "{:_<20} {:_<30} {:_<10}\n".format(metrics['label'], metrics['timestamp'], metrics['value'])
    telegram.post(mgs, vps_info['chatId'],'html')
    self.write({'update': update})