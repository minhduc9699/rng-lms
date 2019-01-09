from google.cloud import firestore
import os
from addict import Dict
from datetime import datetime, timezone, timedelta

def init():
  config_file = "tk-progress-firebase-adminsdk-mbmg0-91918abc04.json"
  cwd = os.getcwd()
  config_path = os.path.join(cwd, config_file)
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config_path
  return firestore.Client()

def sprint_message():
  client = init()
  sprint_docs = client.collection('sprints').get()

  sprints = [
    sprint_doc.to_dict()
    for sprint_doc in sprint_docs
  ]
  sprints = [
    {
      **sprint,
      **{
        "project": sprint['project'].get().to_dict()
      }
    }
    for sprint in sprints
  ]

  sprint = sprints[0]
  def message(sprint):
    time_left = sprint['deadline'] - datetime.now(timezone.utc)
    project = sprint['project']['title']
    seconds = int(time_left.seconds) % 60
    minutes = int(time_left.seconds / 60) % 60
    hours = int(time_left.seconds / 60 / 60)
    text = '''*{0}*
We have `{1} days, {2} hours, {3} minutes, {4} seconds` left'''.format(project, time_left.days, hours, minutes, seconds)
    return text
  
  return "\r\n\r\n".join([message(sprint) for sprint in sprints])

if __name__ == "__main__":
  sprint_msg = sprint_message()
  print(sprint_msg)