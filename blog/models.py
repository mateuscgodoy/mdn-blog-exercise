import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Author(models.Model):
    """Model representing an author, regular users
    become authors after publishing their first article."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(
        verbose_name="Biography",
        help_text="Enter some information about yourself and your background.",
        default="Author has not set any bio information yet.",
        max_length=1000,
    )
    writes_since = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["writes_since", "user"]

    def __str__(self):
        return self.user


class Blog(models.Model):
    """Model representing the blogs that will be created by the users"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID representing this specific blog post",
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "title"]
        get_latest_by = "created_at"

    def __str__(self):
        return f"{self.title} - {self.created_at}"


class Comment(models.Model):
    """Model representing the comments done by users to blog posts"""

    content = models.TextField(
        max_length=1000,
        help_text="Remember to be respectful and polite towards other users. Hateful comments might result in account termination.",
    )
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        get_latest_by = "created_at"

    def __str__(self):
        return f"Comment by {self.creator} ({self.created_at})"
