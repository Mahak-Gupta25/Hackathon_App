from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Hackathon(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.ImageField(upload_to='hackathon_backgrounds')
    hackathon_image = models.ImageField(upload_to='hackathon_images')
    SUBMISSION_TYPES = (
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link'),
    )
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_TYPES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.DecimalField(max_digits=10, decimal_places=2)


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'hackathon']

class Submission(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    summary = models.TextField()
    submission = models.FileField(upload_to='submissions')

