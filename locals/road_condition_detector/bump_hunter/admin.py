# -*- coding: utf-8 -*-
from django.contrib import admin
# from bump_hunter.models import LogData, User
from bump_hunter.models import LogData
from bump_hunter.models import UserInsight

# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'created_at', 'updated_at',)
# admin.site.register(User, UserAdmin)

class LogDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'lat', 'lon', 'acc', 'created_at', 'updated_at',)
admin.site.register(LogData, LogDataAdmin)

class UserInsightAdmin(admin.ModelAdmin):
    list_display = ('id', 'lat', 'lon', 'user_name', 'location', 'comment', 'created_at', 'updated_at',)
admin.site.register(UserInsight, UserInsightAdmin)

