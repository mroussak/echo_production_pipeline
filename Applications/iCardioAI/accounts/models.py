from django.db.models.signals import post_save
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.db import models



# class CustomUser(AbstractUser)

#     phone = models.CharField(max_length=20)
#     full_name = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return self.email


class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.email
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()