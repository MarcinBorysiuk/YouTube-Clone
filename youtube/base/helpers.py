import cv2
from django.contrib import messages

def get_video_length(video_url):
    cap = cv2.VideoCapture(video_url)
    fps = cap.get(cv2.CAP_PROP_FPS)  
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps

    minutes = int(duration/60)
    seconds = int(duration%60)

    if minutes < 10:
        minutes = f'0{minutes}'
    if seconds < 10:
        seconds = f'0{seconds}'

    return str(minutes) + ':' + str(seconds)
    

def validate_video_title(request, title, instance):
    video = instance.objects.filter(title=title)
    if video:
        messages.warning(request, 'Video with this title already exsist')
        return True
    else:
        return False

def validate_video_size(file, request):
    if file.size < 41943040:
        return True
    else:
        return messages.warning(request, 'Maximum size of Video is 50MB')

def validate_video_extension(file, request):
    valid_extensions = ['mp4', 'mov', 'wmv', 'avi', 'mpeg-1', 'mpeg-2', 'mpeg4', 'mpg', 'flv']
    ext = file.name.split('.')[-1]
    if ext.lower() in valid_extensions:
        return True
    else:
        return messages.warning(request, 'Wrong Video format')

def validate_thumbnail_extension(file, request):
    valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
    ext = file.name.split('.')[-1]
    if ext.lower() in valid_extensions:
        return True
    else:
        return messages.warning(request, 'Wrong Thumbnail format')

def validate_picture_extension(file, request):
    valid_extensions = ['jpg', 'jpeg', 'png']
    ext = file.name.split('.')[-1]
    if ext.lower() in valid_extensions:
        return True
    else:
        return messages.warning(request, 'Wrong Picture format')

def username_exists(username, instance):
    return instance.objects.filter(username=username).exists()

def email_exists(email, instance):
    return instance.objects.filter(email=email).exists()

    

    


