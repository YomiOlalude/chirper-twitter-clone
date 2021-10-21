from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class ChirpLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chirp = models.ForeignKey("Chirp", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Chirp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(User, related_name="chirp_user", blank=True)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to="images/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    @property
    def is_rechirp(self):
        return self.parent != None

    def __str__(self):
        return self.content
