from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    bio = models.TextField(blank=True, verbose_name="Биография")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    image = models.ImageField(upload_to='avatars/', blank=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    notifications_enabled = models.BooleanField(default=True, verbose_name="Уведомления включены")

    class Meta:
        verbose_name = "Настройки пользователя"
        verbose_name_plural = "Настройки пользователей"


class AdditionalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    custom_field = models.TextField(blank=True, verbose_name="Дополнительное поле")

    class Meta:
        verbose_name = "Дополнительная информация"
        verbose_name_plural = "Дополнительная информация"


STATUS_CHOICES = [
    ('new', 'Новое'),
    ('in_progress', 'В процессе'),
    ('resolved', 'Решено'),
    ('cancelled', 'Отменено'),
]


class Feedback(models.Model): 
    name = models.CharField(max_length=100, verbose_name='Имя') 
    email = models.EmailField(verbose_name='Электронная почта') 
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', blank=True, null=True) 
    message = models.TextField(verbose_name='Сообщение') 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус') 
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания') 
    cancellation_reason = models.TextField(blank=True, null=True, verbose_name='Причина отмены') 
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

    class Meta: 
        verbose_name = 'Заявки' 
        verbose_name_plural = 'Заявки'

class Chat(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat between {self.user.username} and admin'

    class Meta: 
        verbose_name = 'Чаты' 
        verbose_name_plural = 'Чаты'


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    image = models.ImageField(upload_to='news_images/', null=True, blank=True, verbose_name="Изображение")
    views = models.IntegerField(default=0, null=True, blank=True, verbose_name="Просмотры")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name="Пользователь")
    district = models.ForeignKey('District', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Район")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class District(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название района")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"


class Review(models.Model):
    news_item = models.ForeignKey(News, related_name='reviews', on_delete=models.CASCADE, verbose_name="Новость")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(verbose_name="Рейтинг")
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.user.username} на {self.news_item.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Response(models.Model):
    review = models.ForeignKey(Review, related_name='responses', on_delete=models.CASCADE, verbose_name="Отзыв")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    content = models.TextField(null=True, blank=True, verbose_name="Содержимое")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def clean(self):
        super().clean()
        word_limit = 30
        word_count = len(self.content.split())
        if word_count > word_limit:
            raise ValidationError(f"Содержимое не должно превышать {word_limit} слов. Текущее количество: {word_count}.")

    def __str__(self):
        return f"Ответ от {self.user.username} на комментарий {self.review.id}"

    class Meta:
        verbose_name = "Ответ на комментарий"
        verbose_name_plural = "Ответы на комментарии"


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Название категории")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"


class Service(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Краткое описание", blank=True, null=True)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True, verbose_name="Основное изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    category = models.ForeignKey('ServiceCategory', on_delete=models.CASCADE, null=True, blank=True, related_name="services", verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        
class ServiceDetail(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name="details", verbose_name="Услуга")
    full_description = models.TextField(verbose_name="Полное описание", blank=True, null=True)
    dop_text = models.TextField(null=True, blank=True, verbose_name="Дополнительный текст")

    def __str__(self):
        return f"Детали услуги: {self.service.name}"

    class Meta:
        verbose_name = "Детальная информация об услуге"
        verbose_name_plural = "Детальная информация об услуге"

class ServiceGallery(models.Model):
    service_detail = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE, related_name="gallery", verbose_name="Галерея")
    image = models.ImageField(upload_to='service_gallery/', null=True, blank=True, verbose_name="Изображение")

    def __str__(self):
        return f"Изображение для {self.service_detail.service.name}"
    
    class Meta:
        verbose_name = "Изображение для услуги"
        verbose_name_plural = "Изображения для услуги"

class ServiceDetailDopInfo(models.Model):
    service_detail = models.ForeignKey(ServiceDetail, on_delete=models.CASCADE, related_name="dop_info", verbose_name="Доп. информация для услуги")
    title = models.TextField(null=True, blank=True, verbose_name="Заголовок")
    subtitle = models.TextField(null=True, blank=True,  verbose_name="Подзаголовок")
    content = models.TextField(null=True, blank=True, verbose_name="Информация")

    def __str__(self):
        title = self.title or "Без заголовка"
        service_name = self.service_detail.service.name if self.service_detail and self.service_detail.service else "Нет услуги"
        return f"{title} - {service_name}"

    class Meta:
        verbose_name = "Доп. информация для услуги"
        verbose_name_plural = "Доп. информация для услуги"