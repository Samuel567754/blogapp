from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag
from .forms import PostForm  # This should match the exact name of the form class
from django.contrib import messages
# import sweetify
from django.core.paginator import Paginator
from django.db.models import Q 


def tag_posts(request, tag_name):
    # Filter posts that are associated with the selected tag
    posts = Post.objects.filter(tags__name=tag_name, is_published=True)

    categories = Category.objects.all()

    # Set up pagination
    paginator = Paginator(posts, 3)  # 5 posts per page
    page_number = request.GET.get('page', 1)  # Default to page 1 if no page number is provided
    posts_page = paginator.get_page(page_number)  # Get the posts for the current page

    return render(request, 'posts/tag_posts.html', {'posts': posts_page, 'categories': categories, 'tag_name': tag_name,})




def post_list(request):
    search_query = request.GET.get('q', '')  # Get the search query from the URL
    posts = Post.objects.filter(is_published=True)


    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))  # Filter by title or content

    categories = Category.objects.all()

    tags = Tag.objects.all()

    # Set up pagination
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page', 1)  # Default to page 1 if no page number is provided
    posts_page = paginator.get_page(page_number)  # Get the posts for the current page

    return render(request, 'posts/post_list.html', {'posts': posts_page, 'categories': categories, 'search_query': search_query, 'tags': tags,})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post-list')
        else:
            messages.error(request, 'There was an error creating the post.')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post-detail', pk=post.pk)
        else:
            messages.error(request, 'There was an error updating the post.')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('post-list')
    else:
        messages.error(request, 'There was an error deleting the post.')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})


def category_posts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    search_query = request.GET.get('q', '')  # Get the search query from the URL
    posts = Post.objects.filter(categories=category, is_published=True)

    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))  # Filter by title or content

    # Set up pagination
    paginator = Paginator(posts, 3)  # 3 posts per page
    page_number = request.GET.get('page', 1)  # Default to page 1 if no page number is provided
    posts_page = paginator.get_page(page_number)  # Get the posts for the current page

    return render(request, 'posts/category_posts.html', {'category': category, 'posts': posts_page, 'search_query': search_query,'no_results': not posts.exists()})