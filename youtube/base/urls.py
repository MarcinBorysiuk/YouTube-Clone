from django.urls import path
from .views import home, search, login_page, logout_page, register, channel_details, upload_video, watch_video

urlpatterns = [
    path('', home, name="home"),
    path('search/', search, name="search"),
    path('register/', register, name="register"),
    path('login/', login_page, name="login"),
    path('logout/', logout_page, name="logout"),
    path('channel-details/<int:id>', channel_details, name="channel-details"),
    path('upload/', upload_video, name="upload-video"),
    path('watch-video/<int:id>', watch_video, name="watch-video"),
]