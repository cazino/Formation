from django.db import models
from django.contrib.auth.models import User
     
class UserProfile(models.Model):
    url = models.URLField()
    home_address = models.TextField()
    phone_numer = models.PhoneNumberField()
    user = models.ForeignKey(User, unique=True)