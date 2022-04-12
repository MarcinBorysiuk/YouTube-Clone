import django
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Video, Channel, Comment, Reply
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm
from django.db.models import Q
from .helpers import (validate_thumbnail_extension, validate_video_extension, validate_video_size, 
validate_video_title, username_exists, email_exists, validate_picture_extension)


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        channel_name = form['username'].value()
        email = form['email'].value()
        password1 = form['password1'].value()
        password2 = form['password2'].value()

        if username_exists(channel_name, Channel):
            messages.success(request, 'Channel name already exists')
            return redirect('register')

        if email_exists(email, Channel):
            messages.success(request, 'E-mail address already exists')
            return redirect('register')

        if password1 != password2:
            messages.success(request, 'Passwords did not match')
            return redirect('register')
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully for ' + channel_name + ', please log in')
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
    videos = videos
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
    subscriptions = 10*[item for item in channel.subscriptions.all()]
    videos = 10*[item for item in channel.videos.all()]
    channel_subscribed = channel.is_subscribing(request.user)
    all_views = sum([video.views for video in videos])
    
    context = {
        'channel': channel, 
        'subscriptions': subscriptions, 
        'videos': videos,
        'current_option': current_option,
        'subscribed': channel_subscribed,
        'views': all_views
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

        if validate_video_title(request, title, Video):
            print(title)
            return redirect('upload-video')

        if validate_video_extension(video, request) and validate_thumbnail_extension(thumbnail, request) and validate_video_size(video, request):
            video_to_create = Video(
                video=video,
                title=title,
                description=desc,
                thumbnail=thumbnail,
                channel=channel
            )
            video_to_create.save()
            video_to_create.get_duration()
            messages.success(request, 'Successfully uploaded ' + title )
            return redirect('channel-details', request.user.id)
        else:
            return redirect('upload-video')
        
    return render(request, 'base/upload-video.html')
    
def watch_video(request, id):
    channel = request.user
    video = Video.objects.get(id=id)
    video.add_one_view()
    comments = video.comments.all()
    side_videos = [v for v in Video.objects.all()[:40] if v != video]
    channel_subscribed = video.channel.is_subscribing(channel)

    if request.method == "POST":
        if channel.is_authenticated:
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
        else:
            messages.success(request, 'Please login to comment or like videos')
            return redirect('login')

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

@login_required(login_url='login')
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


def change_profile(request, id):
    channel = Channel.objects.get(id=id)

    if request.method == "POST":
        profile_picture = request.FILES.get('profile_picture')
        if validate_picture_extension(profile_picture, request):
            channel.picture = profile_picture
            channel.save()
            return redirect('channel-details', id)
        else:
            return redirect('change-profile', id)
    return render(request, 'base/change-profile.html', {'channel': channel})

def delete_video_confirmation(request, id):
    video = Video.objects.get(id=id)
    if request.method == "POST":
        video.delete()
        return redirect('channel-details', video.channel.id)
    return render(request, 'base/delete-video.html', {'video': video})
