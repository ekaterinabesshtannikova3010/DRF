from .models import User
from django.contrib import admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'city', 'is_staff', 'is_active')
    search_fields = ('email', 'phone', 'city')

