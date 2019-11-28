from django.contrib import admin
from .models import Post, Comment, Crawling, Google, Search, SearchComment, SearchCommentDetail, CeleryOne, CeleryTwo

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Crawling)
admin.site.register(Google)
admin.site.register(Search)
admin.site.register(SearchComment)
admin.site.register(SearchCommentDetail)
admin.site.register(CeleryOne)
admin.site.register(CeleryTwo)
