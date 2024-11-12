from django.db import models

class Gallery(models.Model):
    title = models.CharField(blank=True, max_length=100, help_text="Title of the image")
    description = models.TextField(blank=True, help_text="Optional description of the image")
    image = models.ImageField(upload_to='gallery_images/', help_text="Upload the image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(blank=True , max_length=200)
    image = models.ImageField(upload_to='events/')
    date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']  # Order by newest first

    def __str__(self):
        return self.title

class NewsEvent(models.Model):
    title = models.CharField(blank=True, max_length=200)
    image = models.ImageField(upload_to='news/')
    date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']  # Order by newest first

    def __str__(self):
        return self.title