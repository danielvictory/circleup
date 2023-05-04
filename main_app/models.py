from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    friends = models.ManyToManyField('Profile', related_name = "profileFriends")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    
class Circle(models.Model):
    title = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    link = models.URLField(max_length=500)
    description = models.TextField()
    tags = models.CharField(max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    allowed = models.ManyToManyField(User, related_name='allowed')  
    requested = models.ManyToManyField(User, related_name='requested')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'circle_id': self.id})

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

# class Friend(models.Model):
#     pass

class Friend_Request(models.Model):
    from_user = models.ForeignKey(Profile, related_name="from_user", on_delete = models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name="to_user", on_delete=models.CASCADE)
