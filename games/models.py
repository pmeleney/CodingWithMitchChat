from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.
User = get_user_model()

class Game(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    creator = models.ForeignKey(User,related_name='game_creator',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('games:game',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['-created_at']

class Entry(models.Model):
    creator = models.ForeignKey(User,related_name='entry_creator',on_delete=models.CASCADE)
    game = models.ForeignKey(Game,related_name='entry_game',on_delete=models.CASCADE)
    slug = models.SlugField(allow_unicode=True)
    entry = models.CharField(max_length=255, blank=False)
    place = models.IntegerField()
    is_used = models.BooleanField(default=False)
    used_now = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entry

    def save(self, *args, **kwargs):
        self.slug = slugify(self.game.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('games:newentry',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['-created_at']
        unique_together = ('game', 'entry')
