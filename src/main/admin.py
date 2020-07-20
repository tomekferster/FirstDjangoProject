from django.contrib import admin
from .models import PostCategory, Post, PostComment

admin.site.register(PostCategory)
admin.site.register(Post)