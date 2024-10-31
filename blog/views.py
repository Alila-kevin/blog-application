from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # Fetch posts
    return render(request, 'blog/post_list.html', {'posts': posts})  # Pass posts to template

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save yet
            post.author = request.user  # Assign the logged-in user as the author
            post.save()  # Now save the post
            return redirect('post_list')  # Redirect to the post list view after saving
    else:
        form = PostForm()
    
    return render(request, 'blog/add_post.html', {'form': form})
