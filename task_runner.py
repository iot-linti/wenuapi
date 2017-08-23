#!/usr/bin/python
import os
import importlib
from celery import Celery
from wenuapi.settings import rabbitmq_url

TASKS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tasks')
print(rabbitmq_url)
app = Celery('wenuapibroker', broker=rabbitmq_url)

#@app.on_after_configure.connect
#def setup_tasks(sender, **kwargs):
#    task_names = [filename for filename in os.listdir(TASKS_PATH)
#                      if filename.endswith('_task.py')]
#
#    task_modules = []
#
#    for task in task_names:
#        task = task.rsplit('.', 1)[0]
#
#        task_modules.append(importlib.import_module('tasks.' + task))
#        configuration = task_modules[-1].configuration()
#
#        if configuration.periodic:
#            sender.add_periodic_task(
#                configuration.period,
#                task_modules[-1].run,
#            )

@app.task
def hi():
    import time
    time.sleep(5)
    print("Hola")


if __name__ == '__main__':
    task_packages = ['tasks.' + pack for pack in os.listdir('tasks')
                     if os.path.isdir(os.path.join('tasks', pack))]
    print task_packages
    app.autodiscover_tasks(task_packages)
    app.start()
