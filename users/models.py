from django.db import models


class User(models.Model):
    """
    Custom user model — plain models.Model (NOT AbstractUser).
    Django's built-in auth.User handles session authentication separately.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # stores hashed passwords
    username = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'users'

    def __str__(self):
        return f"{self.username} ({self.email})"


class Post(models.Model):
    """
    Post model linked to the custom User via a model-level FK only.
    db_constraint=False means no DB-level foreign key is enforced.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,  # model-level FK only, NOT enforced at DB level
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'users'

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"
