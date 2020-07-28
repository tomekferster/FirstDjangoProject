from .models import Post
from django.shortcuts import redirect
from django.contrib import messages


class PostLikeAndComment:

    def post(self, request, *args, **kwargs):
        # 'like' and 'dislike' are the names of buttons in 'post_detail.html' template
        if 'like' in request.POST or 'dislike' in request.POST:
            print(request.POST)
            self.object = self.get_object()
            if self.object.likes.filter(pk=self.request.user.pk):
                self.object.likes.remove(self.request.user)
            else:
                self.object.likes.add(self.request.user)
            return redirect(self.object.get_absolute_url())

        else:
            print(request.POST) 
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form, request.user)
            else:
                return self.form_invalid(form)