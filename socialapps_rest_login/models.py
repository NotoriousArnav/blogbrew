from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from uuid import uuid4
from datetime import date
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def compressImage(uploaded_image, username):
  image_temp = Image.open(uploaded_image)
  outputIoStream = BytesIO()
  image_temp.thumbnail( (800,800) )
  image_temp.save(outputIoStream , format='JPEG', quality=60)
  outputIoStream.seek(0)
  filename = f"{username}.{uploaded_image.name.split('.')[-1]}";print("compressing");
  uploaded_image = InMemoryUploadedFile(
            outputIoStream,
            'ImageField',
            filename,
            'image/jpeg',
            sys.getsizeof(outputIoStream), None
        )
  return uploaded_image

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
    def isDefaultProfile(self):
        default_pfp = self._meta.get_field('pfp').get_default()
        if self.pfp == default_pfp:
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.id:
            self.pfp = compressImage(self.pfp, self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
        profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)
