from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import MyUser

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('is_subscribed', 'avatar', 'favourites')}),
)
admin.site.register(MyUser, UserAdmin)
