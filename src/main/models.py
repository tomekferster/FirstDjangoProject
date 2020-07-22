from django.db import models
from django.utils import timezone
from django.contrib.auth.forms import User
from django.conf import settings
from django.urls import reverse
from PIL import Image
from account.models import Account

class PostCategory(models.Model):
    name                = models.CharField(max_length=200)
    slug                = models.SlugField()

    class Meta:
        verbose_name_plural = 'Post categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:post-sort", kwargs={"single_slug": self.slug})


class Post(models.Model):
    post_category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='blog_posts')  # related_name is used to make it User.blog_posts instead of User.post_set
    title = models.CharField(max_length=25)
    date_published = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='post_images', blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    likes  = models.ManyToManyField(Account, related_name='likes', blank=True)

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['-date_published']

    def __str__(self):
        return f'{self.title} - {self.author}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 600 or img.height > 600:
            new_size = (600, 600)
            img.thumbnail(new_size)
            img.save(self.image.path)

    def total_likes(self):
        return self.likes.count()


    def get_absolute_url(self):
        return reverse("main:post-detail", kwargs={"id": self.id})



class PostComment(models.Model):
    user                = models.ForeignKey(Account, on_delete=models.CASCADE)
    post                = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_date        = models.DateTimeField(default=timezone.now)
    comment_text        = models.TextField(max_length=150)
    active              = models.BooleanField(default=False)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return f'{self.post.title} - {self.user.username}'