from env.config import Config
import requests
from requests.auth import HTTPBasicAuth
from addict import Dict
from telegram import post
from helpers.map_keys import map_keys

azure_api_url = Config.get().azureDevopsAPIUrl
azure_username = Config.get().azureUsername
azure_pat = Config.get().azurePATToken
wit_end_point = f'{azure_api_url}/wit'
work_item_end_point = f'{wit_end_point}/workitems'
task_end_point = f'{work_item_end_point}/$task?api-version=6.0-preview.3'
auth=HTTPBasicAuth(azure_username, azure_pat)


def fetch_task_detail(task_url):
  try:
    r = requests.get(
      task_url,
      headers={'Content-Type': 'application/json-patch+json'},
      auth=auth
    )
    return r.json()
  except Exception as err: 
    print(err)
    return None


def add_task(config):
  title = config['title']
  links = config['links']
  area = config['area']
  iteration_path = config['iteration_path']
  try:
    title_body = {
      'op': 'add',
      'path': '/fields/System.Title',
      'value': title
    }

    area_body = {
      'op': 'add',
      'path': '/fields/System.AreaPath',
      'value': area
    }

    iteration_body = {
      'op': 'add',
      'path': '/fields/System.IterationPath',
      'value': iteration_path
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

    data = [title_body] + [area_body] + [iteration_body] + links_body
    
    r = requests.post(task_end_point, json=data, 
      headers={'Content-Type': 'application/json-patch+json'},
      auth=auth
    )
    if r.status_code != 200:
      print('Add QA task failed')
  except Exception as err:
    print(err)
    return None

def should_add_recheck_task(update):
  resource = update.resource
  update_info = resource.fields
  fields = resource.revision.fields
  relations = resource.revision.relations
  title = fields['System.Title']
  work_item_type = fields['System.WorkItemType']
  task_state = update_info.get('System.State', {})

  # Ignore work item type is task
  if work_item_type == 'Task':
    return False

  # Ignore new task created
  if task_state == 'New':
    return False

  # Check if recheck task exist
  for relation in relations:
    related_task_detail = Dict(fetch_task_detail(relation.url))
    if 'fields' in related_task_detail:
      related_task_title = related_task_detail.fields['System.Title']
      if 'Perform recheck' in related_task_title:
        return False

  # Only add recheck task when a non-QA, non-recheck task was closed
  if 'newValue' in task_state and task_state.get('newValue', '') == 'Closed':
    return True
  return False
  

def should_add_qa_task(update):
  resource = update.resource
  update_info = resource.fields
  fields = resource.revision.fields
  title = fields['System.Title']
  work_item_type = fields['System.WorkItemType']
  task_state = update_info.get('System.State', {})
  
  # Ignore work item type is task
  if work_item_type == 'Task':
    return False

  # Ignore new task created
  if task_state == 'New':
    return False

  # QA task should be added only a non-QA task was closed
  if 'newValue' in task_state and task_state.get('newValue', '') == 'Closed':
    return True
  return False


def add_related_task(update, task_type):
  resource = update.resource
  revision = resource.revision
  work_item_id = resource.workItemId
  link = resource._links.parent.href
  area = revision.fields['System.AreaPath'] # Project
  iteration_path = revision.fields['System.IterationPath'] # Srpint
  work_item_type = revision.fields['System.WorkItemType']

  task_title_map = {
    'qa': f'Perform Quality Assurance on #{work_item_id}',
    'recheck': f'Perform recheck on #{work_item_id} with live version'
  }
  
  # Prepare title and link back to closed work item
  work_item_link_type = {
    'parent': 'System.LinkTypes.Hierarchy-Reverse',
    'related': 'System.LinkTypes.Related'
  }

  task_title = task_title_map[task_type]
  task_relation_type = work_item_link_type['related'] if work_item_type != 'User Story' else work_item_link_type['parent']
  task_links = [{
    'value': link,
    'rel': task_relation_type # Parent link type
  }]
  for relation in revision.relations: # Set up qa task relation with completed task parent
    if relation.rel == work_item_link_type['parent'] and task_relation_type != work_item_link_type['parent']:
      task_links.append({
        'value': relation.url,
        'rel': work_item_link_type['parent']
      })
  add_task({
    'title': task_title,
    'area': area,
    'iteration_path': iteration_path,
    'links': task_links
  })


def create_related_task_if_needed(update):
  if should_add_qa_task(update):
    add_related_task(update, 'qa')
  if should_add_recheck_task(update):
    add_related_task(update, 'recheck')


def notify_telegram_group(update):
  project_id = update.resourceContainers.project.id
  try:
    config = Config.get()
    telegram_routes = map_keys(config['telegramRoutes'], 'projectId')
    chat_id = telegram_routes[project_id]['chatId']
    post(update.detailedMessage.markdown.replace("*", ""), chat_id, "Markdown")
  except KeyError:
    print('Error: "projectId" NOT found')
