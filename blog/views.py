from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Blog
from .froms import BlogImageForm

from utils.decorators import login_required_rest_api

@require_http_methods(['GET'])
def get_blog(request, slug):
    try:
        
        blog = Blog.objects.get(slug=slug, draft=False)


        return render(request, 'html/blog/blog-view.html', {
                                            'blog': blog,
                                        })

    except Blog.DoesNotExist:
        return render(request, '404.html', status=404)


@require_http_methods(['GET'])
def list_blogs(request):

    page_number = request.GET.get("page", 1)
    blogs = Blog.objects.filter(draft=False).order_by('-datetime')

    paginator = Paginator(blogs, per_page=15)
    page = paginator.get_page(page_number)
    
    return render(request, 'html/blog/blog-list.html', {
                                                'blogs': page,
                                            })


BLOG_PERMISSIONS = ['blog.add_blog', 'blog.change_blog']


@login_required_rest_api
@require_http_methods(['POST'])
def upload_image(request):
    
    if request.user.has_perms(BLOG_PERMISSIONS):
        form = BlogImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return JsonResponse({'url': image.image.url}, status=201)

        else: 
            return JsonResponse({'error': form.errors.as_text()}, status=400)


    return JsonResponse({'error': 'Invalid form submission'}, status=401)