from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.
from django.contrib.auth import get_user_model

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class MRIImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mri_images", null=True, blank=True)  # Attach to User instead of Hospital
    
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"MRI Image {self.id}"



# dto Django's User model
#     name = mef get_default_user():
#      return User.objects.first().id if User.objects.exists() else None

# class Hospital(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="hospital", null=True, blank=True)
#   # Links odels.CharField(max_length=255, unique=True, default="Unknown Hospital")
#     address = models.TextField(default="Not provided")
#     phone_number = models.CharField(max_length=15, default="0000000000")
#     registration_number = models.CharField(max_length=50, unique=True, default="REG123456")
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=now)
    
#     image = models.ImageField(upload_to="hospital_images/", null=True, blank=True)  # Added image field


#     class Meta:
#         verbose_name = "Hospital"
#         verbose_name_plural = "Hospitals"
#         ordering = ["name"]  # Sorts hospitals alphabetically

#     def __str__(self):
#         return self.name



from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="hospital", null=True, blank=True)
    name = models.CharField(max_length=255, unique=True, default="Unknown Hospital")
    address = models.TextField(default="Not provided")
    phone_number = models.CharField(max_length=15, default="0000000000")
    registration_number = models.CharField(max_length=50, unique=True, default="REG123456")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    image = models.ImageField(upload_to="hospital_images/", null=True, blank=True)

    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"
        ordering = ["name"]

    def __str__(self):
        return self.name
