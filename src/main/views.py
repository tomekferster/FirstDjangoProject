from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostCategory
from django.contrib import messages
from .forms import CreatePostForm, CommentForm
from django.core.paginator import Paginator
# from django.core.mail import send_mail
# from mysite.settings import BASE_DIR

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)


def home(request):
    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request=request,
                  template_name='main/home.html',
                  context={"posts": page_obj})



def post_sort(request, single_slug):
    category_slugs = [c.slug for c in PostCategory.objects.all()]
    if single_slug in category_slugs:
        matching_posts = Post.objects.filter(post_category__slug=single_slug)
        return render(request, 'main/home.html', {"posts": matching_posts})
    else:
        return HttpResponse('WRONG SLUG')



def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    liked = False
    if post.likes.filter(id=request.user.id):
        liked = True
    else:
        liked = False  

    comments = post.comments.filter(active=True)
    new_comment = False
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment_form.instance.post = post
            comment_form.save()
            new_comment = True
    else:
        comment_form = CommentForm()
    return render(request=request,
                  template_name='main/post_detail.html',
                  context={"comment_form": comment_form,
                           "post": post,
                           "comments": comments,
                           "new_comment": new_comment,
                           "liked": liked})



def post_create(request):
    form = CreatePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        form = CreatePostForm()             # initialize form - the fields are empty after submitting
        return redirect('main:post-list')
    return render(request=request,
                  template_name='main/post_create.html',
                  context={"form": form})



def post_update(request, id):
    obj = get_object_or_404(Post, id=id)
    form = CreatePostForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST':
        form.save()
        messages.info(request, f"Article {obj.title} was updated")
        return redirect(obj.get_absolute_url())
    return render(request, 'main/post_update.html', {"form": form})


def post_like(request, id):
    obj = get_object_or_404(Post, id=id)
    liked = False
    if obj.likes.filter(id=request.user.id).exists():
        obj.likes.remove(request.user)
        liked = False
    else:
        obj.likes.add(request.user)
        liked = True
    return redirect(obj.get_absolute_url())




def post_delete(request, id):
    obj = get_object_or_404(Post, id=id)
    if request.method == "POST":
        obj.delete()
        messages.warning(request, f"Post ({obj.title}) was deleted!")
        return redirect('main:post-list')
    return render(request, 'main/post_delete.html', {'object': obj})



def about(request):
    pass