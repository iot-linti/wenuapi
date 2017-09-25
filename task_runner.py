#!/usr/bin/python
from redis import Redis
from rq import Queue
import importlib
import os

TASKS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tasks')

def load_task_modules(path, package, endswith='_task.py'):
    task_names = [filename for filename in os.listdir(path)
                      if filename.endswith(endswith)]
    task_modules = []

    for task in task_names:
        task = task.rsplit('.', 1)[0]
        task_modules.append(importlib.import_module('{}.{}'.format(package, task)))

    return task_modules

def setup_tasks(queue, task_modules):
    for module in task_modules:
        queue.enqueue(module.run, timeout=-1)


if __name__ == '__main__':
    redis_conn = Redis()
    queue = Queue(connection=redis_conn)
    tasks = load_task_modules(TASKS_PATH, 'tasks')
    setup_tasks(queue, tasks)
