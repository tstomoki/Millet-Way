from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import Textarea
from django.forms.widgets import TextInput, Select
import math

INSIGHT_TYPES = [('roadway', 'Roadway'),
                 ('sidewalk', 'Sidewalk')]    

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
    # acc_x      = models.DecimalField(max_digits=7, decimal_places=3)
    # acc_y      = models.DecimalField(max_digits=7, decimal_places=3)
    # acc_z      = models.DecimalField(max_digits=7, decimal_places=3)
    acc        = models.DecimalField(max_digits=7, decimal_places=3)
    logged_at  = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "log data at %s" % self.logged_at.strftime('%Y/%m/%d')

    # def get_acc_size(self):
    #     return math.sqrt(math.pow(self.acc_x, 2) + math.pow(self.acc_y, 2) + math.pow(self.acc_z, 2))

class UserInsight(models.Model):
    lat          = models.DecimalField(max_digits=20, decimal_places=17)
    lon          = models.DecimalField(max_digits=20, decimal_places=17)
    user_name    = models.CharField(max_length=200, default='')
    insight_type = models.CharField(max_length=20, choices=INSIGHT_TYPES, default='Roadway')
    location     = models.CharField(max_length=200)
    comment      = models.CharField(max_length=200)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return "Insight data at %s" % self.created_at.strftime('%Y/%m/%d')

class UserInsightForm(ModelForm):
    class Meta:
        model = UserInsight
        exclude = ('created_at', 'updated_at',)
        widgets = {
            'lat': TextInput(attrs={
                'id':'input-lat',
                'class': 'form-control',
                'placeholder': '35.900010'
            }),
            'lon': TextInput(attrs={
                'id':'input-lon',
                'class': 'form-control',
                'placeholder': '139.935685'
            }),
            'insight_type': Select(attrs={
                'class': 'form-control',
            }),            
            'user_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bump Hunter'
            }),
            'location': TextInput(attrs={
                'id':'input-location',
                'class': 'form-control',
                'placeholder': 'Kashiwanoha Station'
            }),
            'comment': Textarea(attrs={
                'class': 'form-control',
                'cols': 80,
                'rows': 20,
                'placeholder': 'There are too many bumps around this point!!!'
            }),
        }
