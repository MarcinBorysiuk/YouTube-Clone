from django.urls import path
from .views import (
    delete_video_confirmation, home, search, login_page, logout_page, register, 
    channel_details, subscribe_channel, upload_video, 
    watch_video, like_video, dislike_video, change_profile,
    delete_video_confirmation, search_view_mobile
    )

urlpatterns = [
    path('', home, name="home"),
    path('search/', search, name="search"),
    path('search-mobile/', search_view_mobile, name="search-mobile"),
    path('register/', register, name="register"),
    path('login/', login_page, name="login"),
    path('logout/', logout_page, name="logout"),
    path('channel-details/<int:id>', channel_details, name="channel-details"),
    path('upload/', upload_video, name="upload-video"),
    path('watch-video/<int:id>', watch_video, name="watch-video"),
    path('subscribe-channel/<int:id>', subscribe_channel, name="subscribe-channel"),
    path('like/<int:id>/', like_video, name="like-video"),
    path("dislike/<int:id>/", dislike_video, name="dislike-video"),
    path("change-profile/<int:id>/", change_profile, name="change-profile"),
    path("delete-video/<int:id>/", delete_video_confirmation, name="delete-video"),
]