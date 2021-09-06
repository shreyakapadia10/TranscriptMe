from django.db import models
from accounts.models import User

MEDIA_TYPES = (
    ('text', 'text'),
    ('audio', 'audio'),
    ('video', 'video'),
)

# Create your models here.
class Document(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='files/')
    zip_file = models.FileField(upload_to='zip_files/', blank=True)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    job_id = models.TextField(blank=True)
    conversation_id = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name} by {self.user.first_name}'