from datetime import timedelta, timezone
from django import template
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test

@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Привязка пользователя
            feedback.save()
            return redirect('/')  # Перенаправление на главную страницу
    else:
        form = FeedbackForm()
    return render(request, 'index.html', {'form': form})

def index(request):
    new = News.objects.all().order_by('-published_at')[:4]
    return render(request, 'index.html', {'new': new})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            Avatar.objects.create(user=user)
            UserSettings.objects.create(user=user)
            AdditionalInfo.objects.create(user=user)
            return redirect('/login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):  # Переименовали функцию здесь
    if request.method == 'POST': 
        form = CustomAuthenticationForm(request, data=request.POST) 
        if form.is_valid(): 
            user = form.get_user() 
            auth_login(request, user)  # Используем переименованное login
            return redirect('/profile') 
    else: 
        form = CustomAuthenticationForm() 
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def profile(request):
    avatar = Avatar.objects.filter(user=request.user).first()
    profile = Profile.objects.get(user=request.user)
    user_settings = UserSettings.objects.get(user=request.user)
    additional_info = AdditionalInfo.objects.get(user=request.user)
    password_form = CustomPasswordChangeForm(user=request.user)
    settings_form = UserSettingsForm(request.POST, instance=user_settings)
    
    if request.method == 'POST':
        if 'save_profile' in request.POST:
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Профиль успешно обновлен.")

        elif 'save_avatar' in request.POST:
            avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, "Аватар успешно обновлен.")

        elif 'save_settings' in request.POST:
            settings_form = UserSettingsForm(request.POST, instance=user_settings)
            if settings_form.is_valid():
                settings_form.save()
                messages.success(request, "Настройки успешно обновлены.")

        elif 'save_additional_info' in request.POST:
            additional_info_form = AdditionalInfoForm(request.POST, instance=additional_info)
            if additional_info_form.is_valid():
                additional_info_form.save()
                messages.success(request, "Дополнительная информация успешно обновлена.")

        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)  # Передаем user корректно
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Пароль успешно изменен.")

        return redirect('profile')

    else:
        profile_form = ProfileForm(instance=request.user.profile)
        avatar_form = AvatarForm(instance=avatar) if avatar else AvatarForm()
        settings_form = UserSettingsForm(instance=user_settings)
        additional_info_form = AdditionalInfoForm(instance=additional_info)

    context = {
        'profile_form': profile_form,
        'avatar_form': avatar_form,
        'settings_form': settings_form,
        'additional_info_form': additional_info_form,
        'avatar': avatar,
        'password_form': password_form,
    }
    return render(request, 'profile.html', context)


# Представление для отображения списка новостей
def news_list(request):
    district_filter = request.GET.get('district', '')
    news = News.objects.all().order_by('-published_at')
    
    if district_filter:
        news = news.filter(district__id=district_filter)
    
    districts = District.objects.all()
    
    # Пагинация
    paginator = Paginator(news, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news_list.html', {
        'news': page_obj,
        'districts': districts,
        'current_district': int(district_filter) if district_filter.isdigit() else None,
    })

@user_passes_test(lambda u: u.is_staff)
def admin_feedback_view(request):
    feedback_list = Feedback.objects.all().order_by('created_at')  # Сортировка от старых к новым
    return render(request, 'admin_feedback.html', {'feedback_list': feedback_list})

@user_passes_test(lambda u: u.is_staff)
def chat_view(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    chats = Chat.objects.filter(feedback=feedback).order_by('created_at')

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.feedback = feedback
            chat_message.user = request.user
            chat_message.save()
            return redirect('chat_view', feedback_id=feedback.id)
    else:
        form = ChatForm()

    return render(request, 'chat.html', {'feedback': feedback, 'chats': chats, 'form': form})

@login_required
def user_chat_view(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'user_feedback.html', {'feedbacks': feedbacks})

@login_required
def user_chat_detail_view(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id, user=request.user)
    chats = Chat.objects.filter(feedback=feedback).order_by('created_at')
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.feedback = feedback
            chat_message.user = request.user
            chat_message.save()
            return redirect('user_chat_detail_view', feedback_id=feedback.id)
    else:
        form = ChatForm()

    return render(request, 'user_chat.html', {'feedback': feedback, 'chats': chats, 'form': form})

# Представление для отображения деталей новости
def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    session_key = f'news_viewed_{pk}'
    if request.user.is_authenticated:
        if not request.session.get(session_key, False):
            # Увеличиваем количество просмотров только если пользователь авторизован и еще не просматривал новость
            news_item.views += 1
            news_item.save()
            request.session[session_key] = True
    reviews = news_item.reviews.all()
    if request.method == 'POST' and 'review_id' in request.POST:
        review_id = request.POST['review_id']
        review = get_object_or_404(Review, id=review_id)
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.review = review
            if request.user.is_authenticated:
                response.user = request.user
                response.save()
            else:
                response.save()
            return redirect('news_detail', pk=pk)
    else:
        form = ResponseForm()
    is_authenticated = request.user.is_authenticated
    return render(request, 'news_detail.html', {
        'news_item': news_item,
        'reviews': reviews,
        'form': form,
        'is_authenticated': is_authenticated,
    })

@login_required
def add_review(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    rating = request.POST.get('rating')
    content = request.POST.get('content')
    Review.objects.create(news_item=news_item, user=request.user, rating=rating, content=content)
    return redirect('news_detail', pk=news_id)

def contacts(request):
    return render(request, 'contacts.html')

def services(request):
    return render(request, 'services.html')

def services(request):
    category_filter = request.GET.get('category')
    categories = ServiceCategory.objects.all()
    if category_filter:
        try:
            selected_category = ServiceCategory.objects.get(id=category_filter)
            services = selected_category.services.all()
        except ServiceCategory.DoesNotExist:
            services = Service.objects.all()
    else:
        services = Service.objects.all()
    return render(request, 'services.html', {
        'categories': categories,
        'services': services,
        'selected_category': int(category_filter) if category_filter else None,  # ID выбранной категории
    })

def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    details = getattr(service, 'details', None)
    gallery_images = details.gallery.all() if details else []
    dop_info = details.dop_info.all() if details else []

    return render(request, 'service_detail.html', {
        'service': service,
        'details': details,
        'gallery_images': gallery_images,
        'dop_info': dop_info,
    })
