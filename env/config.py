import json
from addict import Dict

class Config:
  value = None
  
  @classmethod
  def get(cls):
    if not cls.value:
      with open('config.json') as config_file:
        config_file_content = config_file.read()
        cls.value = Dict(json.loads(config_file_content))
    return cls.value
