from django.contrib import admin
from .models import User, Song, Playlist


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "profile_photo")


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "play_song",
        "singer",
        "written_by",
        "release_date",
        "cover_photo",
        "types",
    )


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owned_by", "privacy")
