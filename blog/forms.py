from django import forms

from .models import Post, Comment, Crawling, Google, CustomUser, Search, SearchComment, SearchCommentDetail, CeleryOne, CeleryTwo

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class CrawlingForm(forms.ModelForm):

    class Meta:
        model = Crawling
        fields = ('title', 'link',)

class GoogleForm(forms.ModelForm):

    class Meta:
        model = Google
        fields = ('search_title', 'title',)

class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('is_customer', 'is_seller', 'roles',)

class SearchForm(forms.ModelForm):

    class Meta:
        model = Search
        fields = ('title', 'period',)

class SearchCommentForm(forms.ModelForm):

    class Meta:
        model = SearchComment
        fields = ('title', 'link',)

class SearchCommentDetailForm(forms.ModelForm):

    class Meta:
        model = SearchCommentDetail
        fields = ('title', 'link',)

class CeleryOneForm(forms.ModelForm):

    class Meta:
        model = CeleryOne
        fields = ('title', 'period',)

class CeleryTwoForm(forms.ModelForm):

    class Meta:
        model = CeleryTwo
        fields = ('title', 'period',)
