import os
import tornado.web
from addict import Dict
import json
import tornado.gen
import telegram
from prometheus.prometheus import get_vps_metrics
from env.config import Config


class SentryHandler(tornado.web.RequestHandler):

  def get(self):
    self.write({"Hello": "crm/sentry"})
  
  @tornado.gen.coroutine
  def post(self):
    vps_info = Config.get().sentry
    update = Dict(json.loads(self.request.body))
    payload = update["data"]
    telegram.post(f'''{payload["description_title"]}\n{payload["description_text"]}''', vps_info.chatId)
    vps_metrics = get_vps_metrics(vps_info.nodeExporter, vps_info.vpsName)
    mgs = [
      f'{metrics["label"]} was {metrics["value"]} at {metrics["timestamp"]}\n\n' 
      for metrics in vps_metrics
    ]
    telegram.post(''.join(mgs), vps_info.chatId, 'html')
    self.write({'update': update})
