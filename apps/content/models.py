from django.db import models


from apps.accounts.models import User
from config.utils import CustomAutoField

class Tag(models.Model):
    id = CustomAutoField(primary_key=True, editable=False, start_value=10**6+1)
    name = models.CharField(max_length=255, unique=True)

    start_id = 10 ** 6 + 1
    
    class Meta:
        db_table = 'content_tags'
        ordering = ('name', )
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
    
    def __str__(self):
        return self.name
