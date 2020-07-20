from .models import PostCategory

def post_categories(request):
    categories = PostCategory.objects.all()
    return {"categories": categories}

