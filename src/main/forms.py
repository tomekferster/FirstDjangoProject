from django import forms
from .models import Post, PostComment


# class CreatePostForm(forms.ModelForm):
    
#     class Meta:
#         model = Post
#         fields = ['title', 'image', 'content', 'post_category']


# class UpdatePostForm(forms.ModelForm):
    
#     class Meta:
#         model = Post
#         fields = ['title', 'image', 'content', 'post_category']


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = PostComment
        widgets = {
            'comment_text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'This is a place for your comment'
                })
        }
        fields = ['comment_text']