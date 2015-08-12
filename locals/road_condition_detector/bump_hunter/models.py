from django.db import models

class User(models.Model):
    name       = models.CharField(max_length=200)
    password   = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name

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
