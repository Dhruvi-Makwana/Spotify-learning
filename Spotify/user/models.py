from django.contrib.auth.models import AbstractUser
from django.db import models
from user.choice import SONG_TYPES, PRIVACY
from django.contrib.auth.hashers import make_password


class User(AbstractUser):
    profile_photo = models.ImageField(upload_to="profile_photo/", blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)


class Song(models.Model):

    name = models.CharField(max_length=200, help_text="enter a song name")
    singer = models.ForeignKey(
        User, on_delete=models.CASCADE, max_length=200, related_name="sung_songs"
    )
    written_by = models.ForeignKey(
        User, on_delete=models.CASCADE, max_length=200, related_name="written_songs"
    )
    release_date = models.DateField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to="cover_photo/", blank=True, null=True)
    types = models.CharField(choices=SONG_TYPES, max_length=20)
    play_song = models.FileField(upload_to="song_list/", blank=True, null=True)

    def __str__(self):
        return f" {self.name}"


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    song = models.ManyToManyField(Song, related_name="playlist_song")
    owned_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="playlist"
    )
    privacy = models.CharField(choices=PRIVACY, max_length=100, default="PRIVATE")

    def __str__(self):
        return f" {self.name}"
