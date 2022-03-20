from django.shortcuts import render, redirect
from .models import Video, Channel, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm, UploadVideoForm
from django.db.models import Q



def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created successfully for ' + user)

            return redirect('login')

    context = {'form': form}
    return render(request, 'base/register.html', context)

def login_page(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = Channel.objects.get(username=name)
        except:
            messages.warning(request, 'User does not exist')

        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or Password is incorrect')

    return render(request, 'base/login.html', {})


def logout_page(request):
    logout(request)
    return redirect('home')


def home(request):
    videos = Video.objects.all()
    print(videos[0].video.url)
    context = {'videos': videos}
    return render(request, 'base/home.html', context)

def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    videos = Video.objects.filter(
        Q(title__icontains=q)
        )

    videos = sorted(videos, key=lambda video:video.views, reverse=True)
   
    context = {'videos': videos}
    return render(request, 'base/search.html', context)

def channel_details(request, id):
    channel = Channel.objects.get(id=id)
    return render(request, 'base/channel-details.html', {'channel': channel})

def upload_video(request):
    if request.method == "POST":
        title = request.POST.get('title')
        thumbnail = request.FILES.get('thumbnail')
        video = request.FILES.get('video')

        new_video = Video(
            video=video,
            title=title,
            thumbnail=thumbnail,
            views=0,
            channel=request.user
        )
        new_video.save()

    return render(request, 'base/upload-video.html')
    
def watch_video(request, id):
    channel = request.user
    video = Video.objects.get(id=id)
    comments = video.comments.all()

    side_videos = [v for v in Video.objects.all()[:40] if v != video]

    if request.method == "POST":
        body = request.POST.get('comment_body')
        new_comment = Comment(
            channel=channel,
            video=video,
            body=body
        )
        new_comment.save()
        return redirect('watch-video', id)

    context = {'video': video, 'comments': comments, 'side_videos': side_videos}
    return render(request, 'base/watch-video.html', context)