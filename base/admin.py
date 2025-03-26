from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'website')
    search_fields = ('user__username',)

class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'notifications_enabled')

class AdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'custom_field')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Avatar, AvatarAdmin)
admin.site.register(UserSettings, UserSettingsAdmin)
admin.site.register(AdditionalInfo, AdditionalInfoAdmin)

@admin.register(Feedback) 
class FeedbackAdmin(admin.ModelAdmin): 
    list_display = ('name', 'email', 'phone_number', 'created_at', 'status') 
    list_filter = ('status',) 
    search_fields = ('name', 'email', 'phone_number') 
    
    fieldsets = ( 
        (None, { 
            'fields': ('name', 'email', 'phone_number', 'message', 'status', 'cancellation_reason', 'user') 
        }), 
    ) 
     
    def get_fieldsets(self, request, obj=None): 
        fieldsets = super().get_fieldsets(request, obj) 
         
        if obj and obj.status == 'cancelled':  # Используем правильное значение статуса 
            additional_fields = ( 
                (None, { 
                    'fields': ('cancellation_reason',) 
                }), 
            ) 
            return fieldsets + additional_fields 
         
        return fieldsets
    

admin.site.register(Chat)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'views', 'user')
    search_fields = ('title',)
    list_filter = ('district', 'user')

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'news_item', 'rating', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('rating', 'created_at')

admin.site.register(News, NewsAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Review, ReviewAdmin)


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'content', 'created_at') 
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)
admin.site.register(Response, ResponseAdmin)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    search_fields = ('name',)
    list_filter = ('category',)

@admin.register(ServiceDetail)
class ServiceDetailAdmin(admin.ModelAdmin):
    list_display = ('service',)
    search_fields = ('service__name',)
    list_filter = ('service__category',)

    fieldsets = (
        (None, {
            'fields': ('service', 'full_description', 'dop_text')
        }),
    )

@admin.register(ServiceGallery)
class ServiceGalleryAdmin(admin.ModelAdmin):
    list_display = ('service_detail', 'image')
    search_fields = ('service_detail__service__name',)

@admin.register(ServiceDetailDopInfo)
class ServiceDetailDopInfoAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'display_subtitle', 'service_detail')
    search_fields = ('title', 'subtitle', 'service_detail__service__name')
    empty_value_display = 'Не указано'

    def display_title(self, obj):
        return obj.title or "Без заголовка"

    display_title.short_description = "Заголовок"
    def display_subtitle(self, obj):
        return obj.subtitle or "Без подзаголовка"

    display_subtitle.short_description = "Подзаголовок"
