from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Crawling(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200, default='SOME STRING')
    text = models.TextField()
    link = models.URLField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def approve(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Google(models.Model):
    search_title = models.CharField(max_length=200)
    title = models.TextField(default='SOME STRING')
    #text = models.TextField()
    link = models.URLField()
    #created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class CustomUser(models.Model):
    is_customer=models.BooleanField("IS customer")
    is_seller=models.BooleanField("IS DOCTOR")
    role={
        ('user', "모든날짜"),
        ('h', "지난 1시간"),
        ('d', "지난 1일"),
        ('admin', "지난 1주"),
        ('m', "지난 1개월"),
        ('y', "지난 1년")}
    roles=models.CharField(max_length=10, choices=role,default="user")


class Search(models.Model):
    #title = models.CharField(max_length=200)
    title = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    period={
        ('t', "모든날짜"),
        ('h', "지난 1시간"),
        ('d', "지난 1일"),
        ('w', "지난 1주"),
        ('m', "지난 1개월"),
        ('y', "지난 1년"),
        ('d9', "매일 9시"),
        ('w9', "매주 9시")}

    period=models.CharField(max_length=10, choices=period, default="t")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class SearchComment(models.Model):
    post = models.ForeignKey('blog.Search', on_delete=models.CASCADE, related_name='searchcomments')
    title = models.TextField()
    text = models.TextField()
    link = models.URLField(default='')

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return str(self.published_date)

class SearchCommentDetail(models.Model):
    post = models.ForeignKey('blog.SearchComment', on_delete=models.CASCADE, related_name='searchcommentsdetails')
    title = models.TextField()
    text = models.TextField()
    link = models.URLField()

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.title

class CeleryOne(models.Model):
    #title = models.CharField(max_length=200)
    post = models.ForeignKey('blog.Search', on_delete=models.CASCADE, related_name='searchceleryone', null=True)
    title = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    period=models.CharField(max_length=10)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class CeleryTwo(models.Model):
    #title = models.CharField(max_length=200)
    post = models.ForeignKey('blog.Search', on_delete=models.CASCADE, related_name='searchcelerytwo', null=True)
    title = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    period=models.CharField(max_length=10)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
