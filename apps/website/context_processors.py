def profile_picture(request):
    profile_picture_url = None
    try:
        if request.user.is_authenticated:
            profile_picture_url = request.user.userprofile.profile_picture.url if request.user.userprofile.profile_picture else None
    except:
        pass

    return {'profile_picture_url': profile_picture_url}