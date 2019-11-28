# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from .forms import GoogleForm
from .models import Google, CeleryOne, CeleryTwo
from .forms import SearchCommentForm, SearchCommentDetailForm
from django.utils import timezone

import requests
from bs4 import BeautifulSoup

from .google_search import search

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def post_celery():
    form = GoogleForm()
    post = form.save(commit=False)
    post.search_title = 'TEST CELERY SEARCH_TITLE'
    post.title = 'TEST CELERY TITLE'
    post.published_date = timezone.now()
    post.save()

@shared_task
def post_celery_search():
    title = '의자'
    query = title
    tbs = 'qdr:' + 'd'
    my_links = search(query, tld='com', lang='ko', tbs=tbs)

    for l in my_links:
        form = GoogleForm()
        post = form.save(commit=False)
        post.search_title = query
        post.title = query
        post.link = l
        post.published_date = timezone.now()
        post.save()

@shared_task
def post_celery_search_detail():
    posts = CeleryOne.objects.order_by('-created_date')
    for post in posts:
        query = post.title
        if post.period == 'd9':
            tbs = 'qdr:' + 'd'
            my_links = search(query, tld='com', lang='ko', tbs=tbs)
            for l in my_links:
                googleform = GoogleForm()
                googlepost = googleform.save(commit=False)
                googlepost.search_title = query
                googlepost.title = query
                googlepost.link = l
                googlepost.published_date = timezone.now()
                googlepost.save()

@shared_task
def post_celery_one_value_input():
    posts = CeleryOne.objects.order_by('-created_date')
    for post in posts:
        query = post.title
        now_time = timezone.now()

        searchcommentform = SearchCommentForm()
        searchcommentpost = searchcommentform.save(commit=False)
        searchcommentpost.post = post.post
        searchcommentpost.published_date = now_time
        #searchcommentpost.title = post.title
        searchcommentpost.save()

        if post.period == 'd9':
            tbs = 'qdr:' + 'd'
            my_links = search(query, tld='com', lang='ko', tbs=tbs)

            for l in my_links:
                searchcommentdetailform = SearchCommentDetailForm()
                searchcommentdetailpost = searchcommentdetailform.save(commit=False)
                searchcommentdetailpost.post = searchcommentpost
                searchcommentdetailpost.title = query
                searchcommentdetailpost.link = l
                searchcommentdetailpost.published_date = now_time
                searchcommentdetailpost.save()


@shared_task
def post_celery_two_value_input():
    posts = CeleryTwo.objects.order_by('-created_date')
    for post in posts:
        query = post.title
        now_time = timezone.now()

        searchcommentform = SearchCommentForm()
        searchcommentpost = searchcommentform.save(commit=False)
        searchcommentpost.post = post.post
        searchcommentpost.published_date = now_time
        #searchcommentpost.title = post.title
        searchcommentpost.save()

        if post.period == 'w9':
            tbs = 'qdr:' + 'w'
            #logger.error('Something went wrong!')
            #logger.error(tbs)
            my_links = search(query, tld='com', lang='ko', tbs=tbs)

            for l in my_links:
                searchcommentdetailform = SearchCommentDetailForm()
                searchcommentdetailpost = searchcommentdetailform.save(commit=False)
                searchcommentdetailpost.post = searchcommentpost
                searchcommentdetailpost.title = query
                searchcommentdetailpost.link = l
                searchcommentdetailpost.published_date = now_time
                searchcommentdetailpost.save()

'''
@shared_task
def post_celery_search():
    #posts = get_object_or_404(Post)
    posts = Google.objects.order_by('-published_date')
    for post in posts:
        post.search_title
'''

'''
@shared_task
def post_celery_search():
    form = GoogleForm()
    post = form.save(commit=False)
    post.search_title = 'TEST CELERY SEARCH_TITLE'
    post.title = 'TEST CELERY TITLE'
    post.published_date = timezone.now()
    post.save()
'''
