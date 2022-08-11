from django.contrib import admin

from NurseryApp.models import Pet, UserProfile


class PetAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'shelter', 'is_active']
    actions = ['mark_as_active', 'mark_as_not_active']

    def mark_as_active(self, request, queryset):
        """ Изменение статуса запси на активную"""
        queryset.update(is_active='True')

    def mark_as_not_active(self, request, queryset):
        """ Изменение статуса запси на неактивная """
        queryset.update(is_active='False')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'shelter']


admin.site.register(Pet, PetAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
