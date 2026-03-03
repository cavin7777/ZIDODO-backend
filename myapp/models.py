import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# =========================
# USER MODEL
# =========================

class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.name


# =========================
# LOCATION MODEL
# =========================

class Location(models.Model):

    class Category(models.TextChoices):
        HERITAGE = "HERITAGE"
        BUSINESS = "BUSINESS"
        NATURE = "NATURE"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    latitude = models.FloatField()
    longitude = models.FloatField()

    category = models.CharField(max_length=20, choices=Category.choices)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# =========================
# QUEST MODEL
# =========================

class Quest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField(default=10)

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="quests"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# =========================
# USER QUEST MODEL
# =========================

class UserQuest(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    quest = models.ForeignKey(
        Quest,
        on_delete=models.CASCADE
    )

    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quest')

    def __str__(self):
        return f"{self.user} completed {self.quest}"


# =========================
# REWARD MODEL
# =========================

class Reward(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# =========================
# USER REWARD MODEL
# =========================

class UserReward(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    reward = models.ForeignKey(
        Reward,
        on_delete=models.CASCADE
    )

    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} redeemed {self.reward}"