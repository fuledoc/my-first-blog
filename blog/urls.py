from django.urls import path
from . import views

urlpatterns = [
    #path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('crawling/<int:pk>/', views.post_crawling_detail, name='post_crawling_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('crawling/new', views.crawling_new, name='crawling_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('crawlings', views.post_crawling_list, name='post_crawling_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

    path('google/new', views.google_new, name='google_new'),

    path('', views.post_google_list, name='post_google_list'),

    #path('google/list', views.post_google_list, name='post_google_list'),
    path('google/<int:pk>/', views.post_google_detail, name='post_google_detail'),
    path('google/detail_list', views.post_google_detail_list, name='post_google_detail_list'),
    path('google/search', views.post_google_search, name='post_google_search'),
    path('google/<int:pk>/comment/', views.google_add_comment_to_post, name='google_add_comment_to_post'),
    path('google/<int:pk>/comment/<int:ppk>/detail/', views.google_add_comment_detail_to_post, name='google_add_comment_detail_to_post'),
    path('google_comment/<int:pk>/remove/<int:ppk>', views.google_comment_remove_detail, name='google_comment_remove_detail'),
    path('google_comment/<int:pk>/remove/', views.google_comment_remove, name='google_comment_remove'),
    path('google/celery', views.post_google_celery, name='post_google_celery'),
    path('google/celeryone', views.post_google_celeryone, name='post_google_celeryone'),
    path('google/celeryone/drafts/', views.post_google_celeryone_draft, name='post_google_celeryone_draft'),
    path('google/<int:pk>/publish/', views.post_celeryone_publish, name='post_celeryone_publish'),
    path('google/<int:pk>/remove/', views.post_celeryone_remove, name='post_celeryone_remove'),
    path('google/celeryone/list/', views.post_google_celeryone_list, name='post_google_celeryone_list'),

    #path('', views.index, name='index')
]
