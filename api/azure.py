import os
import tornado.web
from env.config import Config
from addict import Dict
import json
from telegram import post
from helpers.map_keys import map_keys
from azure import add_task, fetch_task_detail


def should_add_recheck_task(update):
  resource = update.resource
  update_info = resource.fields
  fields = resource.revision.fields
  relations = resource.revision.relations
  title = fields['System.Title']

  # Check if recheck task exist
  for relation in relations:
    related_task_detail = Dict(fetch_task_detail(relation.url))
    if 'fields' in related_task_detail:
      related_task_title = related_task_detail.fields['System.Title']
      if 'Perform recheck' in related_task_title:
        return False

  # Only add recheck task when a non-QA, non-recheck task was closed
  if 'System.State' in update_info \
    and update_info['System.State']['newValue'] == 'Closed' \
      and 'Perform QA' not in title \
        and 'Perform Quality Assurance' not in title \
          and 'Perform recheck' not in title:
            return True
  return False
  

def should_add_qa_task(update):
  resource = update.resource
  update_info = resource.fields
  fields = resource.revision.fields
  title = fields['System.Title']
  
  # QA task should be added only a non-QA task was closed
  if 'System.State' in update_info \
    and update_info['System.State']['newValue'] == 'Closed' \
      and 'Perform QA' not in title \
        and 'Perform Quality Assurance' not in title \
          and 'Perform recheck' not in title:
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

class CrmAzureHandler(tornado.web.RequestHandler):

  def get(self):
    self.write({"Hello": "crm/azure"})
  
  def post(self):
    update = Dict(json.loads(self.request.body))
    create_related_task_if_needed(update)
    notify_telegram_group(update)
    with open('update_2.json', 'w') as f:
      f.write(json.dumps(update))
    self.write(json.loads(self.request.body))
