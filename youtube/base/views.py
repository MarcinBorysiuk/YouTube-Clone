from django.shortcuts import render
from .models import Video
from django.db.models import Q


def home(request):
    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, 'base/home.html', context)

def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    videos = Video.objects.filter(
        Q(title__icontains=q)
        )
   
    context = {'videos': videos}
    return render(request, 'base/search.html', context)
