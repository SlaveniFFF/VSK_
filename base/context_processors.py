# from .models import Chat, UserSettings

# def global_chat_notifications(request):
#     chats = Chat.objects.filter(user__is_staff=True).order_by('-created_at')
#     return {'chat_notifications': chats}

# def user_settings(request):
#     if request.user.is_authenticated:
#         user_settings = UserSettings.objects.get(user=request.user)
#         return {'user_settings': user_settings}
#     return {}