from django.shortcuts import render, redirect
from .models import Video, Channel, Comment, Reply
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm
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

    current_option = request.GET.get('q') if request.GET.get('q') != None else ''
    channel = Channel.objects.get(id=id)
    subscriptions = [item for item in channel.subscriptions.all()]
    videos = [item for item in channel.videos.all()]
    channel_subscribed = channel.is_subscribing(request.user)
    
    context = {
        'channel': channel, 
        'subscriptions': subscriptions, 
        'videos': videos,
        'current_option': current_option,
        'subscribed': channel_subscribed
    }
    return render(request, 'base/channel-details.html', context)


@login_required(login_url='login')
def upload_video(request):

    if request.method == "POST":
        video = request.FILES.get('video')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        thumbnail = request.FILES.get('thumbnail')
        channel = request.user

        video_to_create = Video(
            video=video,
            title=title,
            description=desc,
            thumbnail=thumbnail,
            channel=channel
        )

        video_to_create.save()
        return redirect('channel-details', request.user.id)
    

    return render(request, 'base/upload-video.html')
    
def watch_video(request, id):
    channel = request.user
    video = Video.objects.get(id=id)
    video.add_one_view()
    comments = video.comments.all()
    side_videos = [v for v in Video.objects.all()[:40] if v != video]
    channel_subscribed = video.channel.is_subscribing(channel)


    if request.method == "POST":
        if 'comment_body' in request.POST:
            body = request.POST.get('comment_body')
            new_comment = Comment(
                channel=channel,
                video=video,
                body=body
            )
            new_comment.save()
            return redirect('watch-video', id)

        elif 'reply_body' in request.POST:
            body = request.POST.get('reply_body')
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.get(id=comment_id)
            new_reply = Reply(
                channel=channel,
                comment=comment,
                body=body
            )
            new_reply.save()
            return redirect('watch-video', id)

    context = {'video': video, 'comments': comments, 'side_videos': side_videos, 'subscribed': channel_subscribed}
    return render(request, 'base/watch-video.html', context)

def subscribe_channel(request, id):
    current_channel = request.user
    channel_to_subscribe = Channel.objects.get(id=id)

    if channel_to_subscribe in current_channel.subscriptions.all():
        current_channel.subscriptions.remove(channel_to_subscribe)
        channel_to_subscribe.subscribers.remove(current_channel)
    else:
        current_channel.subscriptions.add(channel_to_subscribe)
        channel_to_subscribe.subscribers.add(current_channel)

    return redirect(request.META.get('HTTP_REFERER'))

