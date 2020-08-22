from env.config import Config
import requests
from requests.auth import HTTPBasicAuth

azure_api_url = Config.get().azureDevopsAPIUrl
azure_username = Config.get().azureUsername
azure_pat = Config.get().azurePATToken
wit_end_point = f'{azure_api_url}/wit'
work_item_end_point = f'{wit_end_point}/workitems'
task_end_point = f'{work_item_end_point}/$task?api-version=6.0-preview.3'

def add_task(title, links):
  try:
    title_body = {
      'op': 'add',
      'path': '/fields/System.Title',
      'value': title
    }

    links_body = [
      {
        'op': 'add',
        'path': '/relations/-',
        'value': {
          'rel': link['rel'],
          'url': link['value']
        }
      }
      for link in links
    ]

    data = [title_body] + links_body
    
    auth=HTTPBasicAuth(azure_username, azure_pat)
    r = requests.post(task_end_point, json=data, 
      headers={'Content-Type': 'application/json-patch+json'},
      auth=auth
    )
    if r.status_code != 200:
      print('Add QA task failed')
  except Exception as err:
    print(err)
    return None
  