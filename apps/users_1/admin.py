from django.contrib import admin

from users_1.models.user import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone')