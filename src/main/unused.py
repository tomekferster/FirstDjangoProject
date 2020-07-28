#===============================================================================================================
# PAST FUNCTION VIEWS:
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# NOW PostListView
def home(request):
    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 3)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = True

    return render(request, 'main/home.html', {"posts": page_obj, "is_paginated": is_paginated})


# NOW PostSortedListView
def post_sort(request, single_slug):
    category_slugs = [c.slug for c in PostCategory.objects.all()]
    if single_slug in category_slugs:
        matching_posts = Post.objects.filter(post_category__slug=single_slug)
        return render(request, 'main/home.html', {'posts': matching_posts})
    else:
        return HttpResponse('WRONG SLUG')

# NOW PostDetailView
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
    
    context =  {
        'comment_form': comment_form,
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'liked': liked
    }
    return render(request, 'main/post_detail.html', context)

# NOW PostLikeAndComment in utils.py 
def post_like(request, id):
    post = get_object_or_404(Post, id=id)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return redirect(post.get_absolute_url())

# NOW PostCreateView
def post_create(request):
    form = CreatePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        form = CreatePostForm()             # initialize form - the fields are empty after submitting
        return redirect('main:post-list')
    return render(request, 'main/post_create.html', {'form': form})

# NOW PostUpdateView
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    form = CreatePostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST':
        form.save()
        messages.info(request, f"Article {post.title} was updated")
        return redirect(post.get_absolute_url())
    return render(request, 'main/post_update.html', {'form': form})

# NOW PostDeleteView
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        messages.warning(request, f"Post ({post.title}) was deleted!")
        return redirect('main:post-list')
    return render(request, 'main/post_delete.html', {'post': post})


#===============================================================================================================
# PAST URLCONFs:
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home, name='post-list'),
    path('<int:id>', views.post_detail, name='post-detail'),
    path('<int:id>/like/', views.post_like, name='post-like'),
    path('<slug:single_slug>', views.post_sort, name='post-sort'),
    path('post_create/', views.post_create, name='post_create'),
    path('<int:id>/update/', views.post_update, name='post-update'),
    path('<int:id>/delete/', views.post_delete, name='post-delete'),
]