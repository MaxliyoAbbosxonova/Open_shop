from django.contrib import admin
from django.contrib.admin import ModelAdmin
from users.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    model = User
    list_display = ('id', 'phone', 'email', 'is_active', 'is_staff')
    ordering = ('phone',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )