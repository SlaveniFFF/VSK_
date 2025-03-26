from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='loginn'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('feedback/', feedback_view, name='your_feedback_view'),
    path('chatadm/', admin_feedback_view, name='admin_feedback_view'),
    path('chatadm/<int:feedback_id>/', chat_view, name='chat_view'),
    path('chatusr/', user_chat_view, name='user_chat_view'),
    path('chatusr/<int:feedback_id>/', user_chat_detail_view, name='user_chat_detail_view'),
    path('news/', news_list, name='news_list'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('news/<int:news_id>/add_review/', add_review, name='add_review'),
    path('contacts/', contacts, name='contacts'),
    path('services/', services, name='services'),
    path('service/<int:id>/', service_detail, name='service_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
