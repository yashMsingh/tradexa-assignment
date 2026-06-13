from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PostForm
from .models import Post, User as CustomUser


def login_view(request):
    """Handle login with Django's built-in auth system."""
    if request.user.is_authenticated:
        return redirect('create_post')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_post')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login.html')


@login_required
def create_post(request):
    """
    Display the post creation form and list of all posts.
    Requires the user to be logged in via Django auth.
    Links to our custom User model by matching username.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Fetch (or auto-create) the matching custom User record
            try:
                custom_user = CustomUser.objects.get(username=request.user.username)
            except CustomUser.DoesNotExist:
                custom_user = CustomUser.objects.create(
                    username=request.user.username,
                    email=request.user.email or f"{request.user.username}@tradexa.local",
                    first_name=request.user.first_name,
                    last_name=request.user.last_name,
                    password=request.user.password,
                )

            post = form.save(commit=False)
            post.user = custom_user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('create_post')
    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'users/create_post.html', {'form': form, 'posts': posts})


def logout_view(request):
    """Log out the current user and redirect to login."""
    logout(request)
    return redirect('login')
