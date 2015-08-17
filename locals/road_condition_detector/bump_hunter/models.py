from django.db import models
from django.contrib.auth.models import User

import math

# class User(models.Model):
#     name       = models.CharField(max_length=200)
#     password   = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     def __unicode__(self):
#         return self.name

class LogData(models.Model):
    user       = models.ForeignKey(User)
    lat        = models.DecimalField(max_digits=12, decimal_places=9)
    lon        = models.DecimalField(max_digits=12, decimal_places=9)
    acc_x      = models.DecimalField(max_digits=7, decimal_places=3)
    acc_y      = models.DecimalField(max_digits=7, decimal_places=3)
    acc_z      = models.DecimalField(max_digits=7, decimal_places=3)
    logged_at  = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "log data at %s" % self.logged_at.strftime('%Y/%m/%d')

    def get_acc_size(self):
        return math.sqrt(math.pow(self.acc_x, 2) + math.pow(self.acc_y, 2) + math.pow(self.acc_z, 2))

class UserInsight(models.Model):
    lat        = models.DecimalField(max_digits=12, decimal_places=9)
    lon        = models.DecimalField(max_digits=12, decimal_places=9)
    user_name  = models.CharField(max_length=200, default='John Doe')
    location   = models.CharField(max_length=200)
    comment    = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "insight data at %s" % self.created_at.strftime('%Y/%m/%d')
