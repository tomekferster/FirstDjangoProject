from django.shortcuts import get_object_or_404, reverse
from django.contrib import messages
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .models import Post, PostCategory
from .forms import CommentForm
from .utils import PostLikeAndComment



class PostListView(ListView):
    # model = Post                # not needed here, because we have a queryset
    queryset = Post.objects.all()
    context_object_name = 'posts'
    template_name = 'main/home.html'
    paginate_by = 3


class PostSortedListView(ListView):
    # model = Post        # not really needed here, because we have a queryset
    context_object_name = 'posts'
    template_name = 'main/home.html'
    paginate_by = 3

    def get_queryset(self):
        self.post_cat = get_object_or_404(PostCategory, slug=self.kwargs.get('single_slug'))
        return Post.objects.filter(post_category=self.post_cat)


class PostDetailView(PostLikeAndComment, FormMixin, DetailView):
    # model = Post
    queryset = Post.objects.all()
    context_object_name = 'post'
    template_name = 'main/post_detail.html'
    form_class = CommentForm


    def get_success_url(self):
        messages.info(self.request, "Your comment is awaiting moderation")
        return reverse('main:post-detail', kwargs={'pk': self.object.pk})
        
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(active=True)
        context['liked'] = self.object.likes.filter(pk=self.request.user.pk)
        return context

    def form_valid(self, form, user):
        form.instance.user = user
        form.instance.post = self.object
        form.save()
        return super(PostDetailView, self).form_valid(form)



class PostCreateView(LoginRequiredMixin, CreateView):
    queryset = Post.objects.all()
    template_name = 'main/post_create.html'
    fields = ['title', 'image', 'content', 'post_category']
    
    def get_success_url(self):
        messages.success(self.request, f"Post '{self.object.title}' was created!")
        return reverse('main:post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    queryset = Post.objects.all()
    template_name = 'main/post_update.html'
    fields = ['title', 'image', 'content', 'post_category']

    def get_success_url(self):
        messages.success(self.request, f"Post '{self.object.title}' was updated!")
        return reverse('main:post-list')

    def form_valid(self, form):
        form.save()
        return super(PostUpdateView, self).form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    queryset = Post.objects.all()
    template_name = 'main/post_delete.html'
    context_object_name = 'post'

    def get_success_url(self):
        messages.warning(self.request, f"Post '{self.object.title}' was deleted!")
        return reverse('main:post-list')


def about(request):
    pass