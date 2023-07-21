from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse, reverse_lazy
from user.models import User, Song, Playlist
from rest_framework.authtoken.models import Token
import pytest

pytestmark = pytest.mark.django_db


class UserTest(APITestCase):
    def test_user_test(self):
        from user.factory import UserFactory

        UserFactory()


class TestRegisterTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            first_name="test_1",
            last_name="test_2",
            profile_photo="a1.jpg",
            password="testpassword",
            email="test@gmail.com",
        )

    def test_register(self):
        url = reverse("user:register-api")
        data = {
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "password": self.user.password,
            "email": self.user.email,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):
    def test_login_api(self):
        url = "api/login/"
        data = {
            "username": "abc",
            "password": "1234",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SongAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_songs(self):
        breakpoint()
        url = "/api/song/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_song(self):
        url = reverse_lazy("user:testcase")
        data = {
            "name": "Test Song",
            "singer": self.user.id,
            "written_by": self.user.id,
            "types": "CLASSICAL",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SongUpdateAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.song = Song.objects.create(
            name="test_song_2",
            singer=User.objects.create_user(username="test_1", password="test1"),
            written_by=User.objects.create_user(username="test_2", password="test2"),
            cover_photo="test_photo.jpg",
            types="CLASSICAL",
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_single_song(self):
        # url = reverse('update-song-api')
        url = f"/api/song/{self.song.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_songs(self):
        # url = reverse('update-song-api')
        url = f"/api/song/{self.song.id}"
        data = {
            "name": "Test Song",
            "singer": self.user.id,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlaylistAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="playlistuser", password="testpassword"
        )
        self.song = Song.objects.create(
            name="test_song1",
            singer=User.objects.create_user(username="test1", password="demo"),
            written_by=User.objects.create_user(username="test2", password="test"),
            cover_photo="test_photo.jpg",
            types="CLASSICAL",
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_all_playlist(self):
        # url = reverse('playlist-api')
        url = "/api/playlist/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_playlist(self):
        # url = reverse('playlist-api')
        url = "/api/playlist/"
        data = {
            "name": "test_playlist1",
            "song": self.song.id,
            "owned_by": self.user.id,
            "types": "PUBLIC",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetPLayListWithoutAuth(APITestCase):
    def test_get_all_playlist(self):
        # url = reverse('playlist-api')
        url = "/api/playlist/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlaylistUpdateAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )
        self.song = Song.objects.create(
            name="test_song_2",
            singer=User.objects.create_user(username="test_1", password="test1"),
            written_by=User.objects.create_user(username="test_2", password="test2"),
            cover_photo="test_photo.jpg",
            types="CLASSICAL",
        )
        self.playlist = Playlist.objects.create(
            name="test_playlist", owned_by=self.user
        )
        self.playlist.song.set([self.song])
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_single_playlist(self):
        url = f"/api/playlist/{self.playlist.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_playlist(self):
        # url = reverse('update-playlist-api')
        url = f"/api/playlist/{self.playlist.id}"
        data = {
            "name": "test_playlist1",
            "song": self.song.id,
            "owned_by": self.user.id,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
