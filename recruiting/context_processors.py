def active_user(request):
    current_user = request.user
    displayed_name = current_user.username
    if current_user.is_authenticated:
        user_is_active = True
        if current_user.first_name and current_user.last_name:
            displayed_name = current_user.first_name + ' ' + current_user.last_name
    else:
        user_is_active = False
    return {
        'user_is_active': user_is_active,
        'displayed_name': displayed_name
    }
