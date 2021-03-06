from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


from celery.schedules import crontab

'''
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'blog.tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}
app.conf.timezone = 'Asia/Seoul'
'''

'''
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'blog.tasks.post_celery_search_detail',
        #'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'schedule': crontab(hour=14, minute=36, day_of_week=2),
        #'args': (16, 16),
    },
}
app.conf.timezone = 'Asia/Seoul'
'''

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-daily-morning': {
        'task': 'blog.tasks.post_celery_one_value_input',
        #'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'schedule': crontab(hour=15, minute=15),
        #'args': (16, 16),
    },

    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'blog.tasks.post_celery_two_value_input',
        #'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'schedule': crontab(hour=15, minute=20, day_of_week=3),
        #'args': (16, 16),
    },
}
app.conf.timezone = 'Asia/Seoul'
