from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    meter_number = models.CharField(max_length=50, null=False)
    user_name = models.CharField(max_length=100, null=False, blank=True)
    token = models.CharField(max_length=100, null=False, blank=True)

    def __str__(self):
        return self.user_name


class Bill(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    amount = models.IntegerField(default=0, null=False)
    volume = models.IntegerField(default=0, null=False)
    date = models.DateTimeField(auto_now_add=True, null=True)
    consumption = models.IntegerField(default=0)

    def __str__(self):
        return self.user.user_name
