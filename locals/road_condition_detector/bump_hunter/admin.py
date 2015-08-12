# -*- coding: utf-8 -*-
from django.contrib import admin
from bump_hunter.models import LogData, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at',)
admin.site.register(User, UserAdmin)

class LogDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'lat', 'lon', 'acc_x', 'acc_y', 'acc_z', 'created_at', 'updated_at',)
admin.site.register(LogData, LogDataAdmin)
