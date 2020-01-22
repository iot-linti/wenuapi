#!/usr/bin/python
'''Load an run tasks in background using rq.
Tasks are modules with a path matching the following glob pattern
./tasks/*_task.py and containing a run() function.'''

from redis import Redis
from rq import Queue
import importlib
import os

# Task path is ./tasks
TASKS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tasks')

def load_task_modules(path, package, endswith='_task.py'):
    '''Dinamically import the tasks modules and return them in
    a list'''
    task_names = [filename for filename in os.listdir(path)
                      if filename.endswith(endswith)]
    task_modules = []

    for task in task_names:
        task = task.rsplit('.', 1)[0]
        task_modules.append(importlib.import_module('{}.{}'.format(package, task)))

    return task_modules

def setup_tasks(queue, task_modules):
    '''Enqueue the tasks run functions in rq'''
    for module in task_modules:
        queue.enqueue(module.run, timeout=-1)


if __name__ == '__main__':
    # Setup Redis and rq
    redis_conn = Redis()
    queue = Queue(connection=redis_conn)
    # Load a list of the available task modules
    tasks = load_task_modules(TASKS_PATH, 'tasks')
    # Run the tasks
    setup_tasks(queue, tasks)
