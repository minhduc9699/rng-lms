import os
import tornado.web
from env.config import Config
from addict import Dict
import json
from telegram import post
from helpers.map_keys import map_keys
from azure import add_task


def should_add_qa_task(update):
  resource = update.resource
  update_info = resource.fields
  fields = resource.revision.fields
  title = fields['System.Title']
  
  # QA task should be added only a non-QA task was closed
  if 'System.State' in update_info \
    and update_info['System.State']['newValue'] == 'Closed' \
      and 'Perform QA' not in title \
        and 'Perform Quality Assurance' not in title:
          return True
  return False

def add_qa_task(update):
  resource = update.resource
  revision = resource.revision

  work_item_id = resource.workItemId
  link = resource._links.parent.href
  area = revision.fields['System.AreaPath'] # Project
  iteration_path = revision.fields['System.IterationPath'] # Srpint
  work_item_type = revision.fields['System.WorkItemType']
  
  # Prepare title and link back to closed work item
  work_item_link_type = {
    'parent': 'System.LinkTypes.Hierarchy-Reverse',
    'related': 'System.LinkTypes.Related'
  }

  qa_task_title = f'Perform Quality Assurance on #{work_item_id}'
  qa_task_relation_type = work_item_link_type['related'] if work_item_type != 'User Story' else work_item_link_type['parent']
  qa_task_links = [{
    'value': link,
    'rel': qa_task_relation_type # Parent link type
  }]
  for relation in revision.relations: # Set up qa task relation with completed task parent
    if relation.rel == work_item_link_type['parent'] and qa_task_relation_type != work_item_link_type['parent']:
      qa_task_links.append({
        'value': relation.url,
        'rel': work_item_link_type['parent']
      })
  add_task({
    'title': qa_task_title,
    'area': area,
    'iteration_path': iteration_path,
    'links': qa_task_links
  })

def create_qa_task_if_needed(update):
  if should_add_qa_task(update):
    add_qa_task(update)

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
    create_qa_task_if_needed(update)
    notify_telegram_group(update)
    with open('update_2.json', 'w') as f:
      f.write(json.dumps(update))
    self.write(json.loads(self.request.body))
