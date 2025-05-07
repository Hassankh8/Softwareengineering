from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=18)
    user_password = models.CharField(max_length=8)
    user_email = models.EmailField(max_length=50, unique=True)
    user_role = models.CharField(max_length=10)


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="searches")
    query = models.CharField(max_length=255)
    media_type = models.CharField(
        max_length=10,
        choices=[("image", "Image"), ("audio", "Audio"), ("video", "Video")],
    )
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_name} - {self.query} ({self.media_type})"


# Media Item Model (to store fetched media)
class MediaItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="media_items")
    query = models.CharField(max_length=255)
    media_type = models.CharField(max_length=10)
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} - {self.title or self.url}"
