from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from uuid import uuid4
from datetime import date
from django.urls import reverse

# Create your models here.
class UserProfile(models.Model):
    MALE, FEMALE, OTHER, PNS = "M", "F", "OTH", "PNS"
    GENDERS = (
        (MALE, "MALE",),
        (FEMALE, "FEMALE",),
        (OTHER, "OTHER",),
        (PNS, "PREFER NOT TO SAY"),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    gender = models.CharField(
        max_length = 3,
        choices = GENDERS,
        default = PNS,
    )
    bio = models.TextField()
    pfp = models.ImageField(
        upload_to="uploads/",
        default = "av.jpg",
        null=True
    )
    def __str__(self):  
        return "%s's profile" % self.user
    
    def get_absolute_url(self):
        return reverse('profile_view', args=[str(self.user.username)])

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)
