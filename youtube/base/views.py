from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Video, Channel, Comment, Reply
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist



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
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Channel.objects.get(email=email)
        except:
            messages.warning(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'E-mail or Password is incorrect')

    return render(request, 'base/login.html', {})


def logout_page(request):
    logout(request)
    return redirect('home')


def home(request):
    videos = Video.objects.all()
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
    subscriptions = 6*[item for item in channel.subscriptions.all()]
    videos = 6*[item for item in channel.videos.all()]
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

@login_required(login_url='login')
def like_video(request, id):
    channel = request.user
    like = False
    if request.method == "POST":
        video_id = request.POST.get('video_id')
        video_to_like = get_object_or_404(Video, id=video_id)
        if channel in video_to_like.likes.all():
            video_to_like.likes.remove(channel)
            like = False
        else:
            if channel in video_to_like.dislikes.all():
                video_to_like.dislikes.remove(channel)
            video_to_like.likes.add(channel)
            like = True

        data = {
            'like': like,
            'total_likes': video_to_like.total_likes(),
            'total_dislikes': video_to_like.total_dislikes()
        }

        return JsonResponse(data, safe=False)
    return redirect(reverse("watch-video", args=[str(id)]))

@login_required(login_url='login')
def dislike_video(request, id):
    channel = request.user
    dislike = False
    if request.method == "POST":
        video_id = request.POST.get('video_id')
        video_to_dislike = get_object_or_404(Video, id=video_id)
        if channel in video_to_dislike.dislikes.all():
            video_to_dislike.dislikes.remove(channel)
            dislike = False
        else:
            if channel in video_to_dislike.likes.all():
                video_to_dislike.likes.remove(channel)
            video_to_dislike.dislikes.add(channel)
            dislike = True

        data = {
            'dislike': dislike,
            'total_dislikes': video_to_dislike.total_dislikes(),
            'total_likes': video_to_dislike.total_likes()
        }

        return JsonResponse(data, safe=False)
    return redirect(reverse("watch-video", args=[str(id)]))


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

