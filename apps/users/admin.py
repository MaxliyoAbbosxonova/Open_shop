from django.contrib import admin
from apps.users.models  import  User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id','phone')
