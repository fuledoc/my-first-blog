from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, Crawling, Google, CustomUser, Search, SearchComment, SearchCommentDetail, CeleryOne, CeleryTwo
from .forms import PostForm, CommentForm, CrawlingForm, GoogleForm, CustomUserForm, SearchForm, SearchCommentForm, SearchCommentDetailForm, CeleryOneForm, CeleryTwoForm
#from .google_search import search
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#from .tasks import sleepy

import requests
from bs4 import BeautifulSoup

from .google_search import search

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_crawling_detail(request, pk):
    post = get_object_or_404(Crawling, pk=pk)
    return render(request, 'blog/post_crawling_detail.html', {'post': post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_crawling_list(request):
    posts = Crawling.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_crawling_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def crawling_new(request):
    req = requests.get('https://beomi.github.io/beomi.github.io_old/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select('h3 > a')

    for title in my_titles:
        form = CrawlingForm()
        post = form.save(commit=False)
        post.title = title.text
        post.link = title.get('href')
        post.author = request.user
        post.published_date = timezone.now()
        post.save()

    return redirect('post_crawling_list')

@login_required
def post_google_list(request):
    posts = Search.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_google_list.html', {'posts': posts})

def post_google_detail(request, pk):
    post = get_object_or_404(Search, pk=pk)
    return render(request, 'blog/post_google_detail.html', {'post': post})


def post_google_detail_list(request):
    posts = Google.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_google_detail_list.html', {'posts': posts})

@login_required
def google_new(request):
    query = "본 고안은 등판을 탄성적으로 지지하는"
    my_titles = search(query, tld='com', lang='ko', tbs='qdr:m', stop=10, pause=2)

    for title in my_titles:
        form = CrawlingForm()
        post = form.save(commit=False)
        post.title = query
        post.link = title
        post.published_date = timezone.now()
        post.save()

    return redirect('post_google_list')

@login_required
def post_google_search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        #form = CustomUserForm(request.POST)

        if form.is_valid():
            now_time = timezone.now()
            post = form.save(commit=False)
            post.published_date = now_time
            post.save()

            if post.period == 'd9':
                celeryoneform = CeleryOneForm()
                celeryonepost = celeryoneform.save(commit=False)
                celeryonepost.post = post
                celeryonepost.title = post.title
                celeryonepost.period = post.period
                #celeryonepost.published_date = now_time
                celeryonepost.save()

            if post.period == 'w9':
                celerytwoform = CeleryTwoForm()
                celerytwopost = celerytwoform.save(commit=False)
                celerytwopost.post = post
                celerytwopost.title = post.title
                celerytwopost.period = post.period
                #celerytwopost.published_date = now_time
                celerytwopost.save()

            searchcommentform = SearchCommentForm()
            searchcommentpost = searchcommentform.save(commit=False)
            searchcommentpost.post = post
            searchcommentpost.published_date = now_time
            #searchcommentpost.title = post.title
            searchcommentpost.save()

            '''
            searchcommentdetailform = SearchCommentDetailForm()
            searchcommentdetailpost = searchcommentdetailform.save(commit=False)
            searchcommentdetailpost.post = searchcommentpost
            searchcommentdetailpost.published_date = now_time
            '''
            # Log an error message
            #logger.error('Something went wrong!')

            query = post.title
            #tbs = 'qdr:' + post.period
            #my_links = search(query, tld='com', lang='ko', tbs='qdr:h')
            if post.period == 't':
                my_links = search(query, tld='com', lang='ko')
            elif post.period == 'd9':
                tbs = 'qdr:' + 'd'
                my_links = search(query, tld='com', lang='ko', tbs=tbs)
            elif post.period == 'w9':
                tbs = 'qdr:' + 'w'
                #logger.error('Something went wrong!')
                #logger.error(tbs)
                my_links = search(query, tld='com', lang='ko', tbs=tbs)
            else:
                tbs = 'qdr:' + post.period
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
                googleform = GoogleForm()
                googlepost = googleform.save(commit=False)
                googlepost.search_title = query
                googlepost.title = query
                googlepost.link = l
                googlepost.published_date = now_time
                googlepost.save()
                '''

            #searchcommentdetailpost.link = 'https://m.blog.naver.com/ummumm8606/221678570875'
            #searchcommentdetailpost.save()


            #googlepost.published_date = now_time
            #googlepost.link = 'test_l'


            '''
            post = form.save(commit=False)
            query = post.title
            now_time = timezone.now()
            post.published_date = now_time
            post.save()
            my_links = search(query, tld='com', lang='ko', tbs='qdr:d', pause=2)


            for l in my_links:
                googleform = GoogleForm()
                googlepost = googleform.save(commit=False)
                googlepost.search_title = query
                googlepost.title = query
                googlepost.link = l
                googlepost.published_date = now_time
                googlepost.save()

            '''

            return redirect('post_google_list')
    else:
        form = SearchForm()
        #form = CustomUserForm()
    return render(request, 'blog/post_google_edit.html', {'form': form})

def google_add_comment_to_post(request, pk):
    post = get_object_or_404(Search, pk=pk)
    if request.method == "POST":
        form = SearchCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.published_date = timezone.now()
            comment.save()
            return redirect('post_google_detail', pk=post.pk)
    else:
        form = SearchCommentForm()
    return render(request, 'blog/google_add_comment_to_post.html', {'form': form})


def google_add_comment_detail_to_post(request, pk, ppk):
    post = get_object_or_404(SearchComment, pk=ppk)
    if request.method == "POST":
        form = SearchCommentDetailForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_google_detail', pk=pk)
    else:
        form = SearchCommentDetailForm()
    return render(request, 'blog/google_add_comment_detail_to_post.html', {'form': form})


@login_required
def google_comment_remove(request, pk):
    comment = get_object_or_404(Search, pk=pk)
    comment.delete()
    return redirect('post_google_list')

@login_required
def google_comment_remove_detail(request, pk, ppk):
    comment = get_object_or_404(SearchComment, pk=ppk)
    comment.delete()
    return redirect('post_google_detail', pk=comment.post.pk)

'''
def index(request):
    sleepy(10)
    return HttpResponse('<h1>TASK IS DONE!</h1>')
'''

@login_required
def post_google_celery(request):
    posts = Search.objects.filter(period__contains='d9').order_by('-created_date') | Search.objects.filter(period__contains='w9').order_by('-created_date')
    return render(request, 'blog/post_google_celery.html', {'posts': posts})

@login_required
def post_google_celeryone(request):
    posts = CeleryOne.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_google_celeryone.html', {'posts': posts})

'''
@login_required
def post_google_celery(request):
    return render(request, 'blog/post_google_celery.html')
'''

def post_google_celeryone_draft(request):
    posts = CeleryOne.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_google_celeryone_draft.html', {'posts': posts})

def post_celeryone_publish(request, pk):
    post = get_object_or_404(CeleryOne, pk=pk)
    post.publish()
    return redirect('post_google_celeryone_draft')

'''
def post_celeryone_remove(request, pk):
    post = get_object_or_404(CeleryOne, pk=pk)
    post.published_date = None
    post.save()
    return redirect('post_google_celeryone_list')
'''
def post_celeryone_remove(request, pk):
    #post = get_object_or_404(Search, pk=pk)
    #subpost = get_object_or_404(post.searchceleryone, pk=post.searchceleryone.pk)
    return redirect('post_google_celery')

def post_google_celeryone_list(request):
    posts = CeleryOne.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_google_celeryone_list.html', {'posts': posts})
