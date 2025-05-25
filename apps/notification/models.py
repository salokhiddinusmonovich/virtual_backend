from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from config.utils import CustomAutoField


class Notification(models.Model):

    class NotificationTypeEnum(models.TextChoices):
        FOLLOW = 'follow', 'Follow'
        CONTENT = 'content', 'Content'
        MENTION = 'mention', 'Mention'

    id = CustomAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    body = models.TextField()
    type = models.CharField(max_length=10, choices=NotificationTypeEnum)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ('-created_at',)

    def __str__(self):
        return f'@{self.user.username}: {self.title}'