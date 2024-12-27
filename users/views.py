from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, UserEditForm
from django.contrib.auth.decorators import login_required
from blog.models import Post  # Importing Post from blog app
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import JsonResponse




@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')  # Redirect after saving
        else:
            print(form.errors) 
            messages.error(request, f'profile update failed!')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def profile_overview(request):
    user = request.user
    post_count = Post.objects.filter(author=user).count()  # Count user's posts
    
    context = {
        'post_count': post_count,
        'user': user,
    }
    return render(request, 'users/profile_overview.html', context)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to login after registration
        # else:
        #     messages.error(request, f'Account creation failed!')
        #     return redirect('register')  # Redirect to login after registration
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def user_posts(request):
    # Fetch posts by the logged-in user
    user_posts = Post.objects.filter(author=request.user)
    post_count = user_posts.count()  # Count the number of posts

    # Set up pagination
    paginator = Paginator(user_posts, 2)  # 2 posts per page
    page_number = request.GET.get('page', 1)  # Default to page 1 if no page number is provided
    posts_page = paginator.get_page(page_number)  # Get the posts for the current page

    # Pass the posts and count to the template
    context = {
        'user_posts': posts_page,
        'post_count': post_count,
    }

    return render(request, 'users/user_posts.html', context)

@login_required
def profile(request):
    # Retrieve all posts by the logged-in user
    user_posts = Post.objects.filter(author=request.user)
    
    # Get the count of the user's posts
    post_count = user_posts.count()
    
    # Pass the posts and count to the template
    context = {
        'user_posts': user_posts,
        'post_count': post_count
    }
    
    return render(request, 'users/profile.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('profile')  # Redirect to profile after login
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# Create your views here.









