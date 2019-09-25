from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Avatar
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import get_user_model

# Register your models here.

#admin.site.register(User, UserAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('description', 'totalComments', 'totalMods')}),
    )
    list_display = ['email', 'username', 'description', 'totalComments', 'totalMods']


def mark_as_safe(modeladmin, request, queryset):
    queryset.update(avatarApproved=True)


mark_as_safe.short_description = "Mark has approved"


def mark_as_unsafe(modeladmin, request, queryset):
    queryset.update(avatarApproved=False)


mark_as_unsafe.short_description = "Mark has non-approved"


class AvatarAdmin(admin.ModelAdmin):
    list_display = ['avatarID', 'avatarUserID', 'avatarTime', 'avatarImage', 'avatarApproved', 'avatarIP']
    actions = [mark_as_safe, mark_as_unsafe]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Avatar, AvatarAdmin)
