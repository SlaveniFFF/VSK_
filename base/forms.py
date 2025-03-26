from django import forms    
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm    
from django.contrib.auth.models import User 
from django.utils.translation import gettext_lazy as _  
from django.contrib.auth.forms import PasswordChangeForm 
from .models import * 


class CustomUserCreationForm(UserCreationForm):    
    username = forms.CharField(label="Имя пользователя", max_length=150, required=True)   
    email = forms.EmailField(label="Электронная почта", required=True)   
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput, help_text=" ")   
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput, help_text=" ")   

class CustomAuthenticationForm(AuthenticationForm):    
    username = forms.CharField(label="Имя пользователя")   
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)   

class ProfileForm(forms.ModelForm): 
    class Meta: 
        model = Profile 
        fields = ['bio', 'website'] 
        widgets = { 
            'bio': forms.Textarea(attrs={'placeholder': 'Введите вашу биографию'}), 
        } 
        labels = {
            'bio': 'Биография',
            'website': 'Вебсайт',
        }

class AvatarForm(forms.ModelForm): 
    class Meta: 
        model = Avatar 
        fields = ['image'] 
        labels = {
            'image': 'Изображение',
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)


class UserSettingsForm(forms.ModelForm): 
    class Meta: 
        model = UserSettings 
        fields = ['notifications_enabled'] 
        labels = {
            'notifications_enabled': 'Уведомления',
        }

class AdditionalInfoForm(forms.ModelForm): 
    class Meta: 
        model = AdditionalInfo 
        fields = ['custom_field'] 
        labels = {
            'custom_field': 'Пользовательское поле',
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone_number', 'message']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.status == 'отменён':
            self.fields['cancellation_reason'].required = True
        

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'district']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['message']