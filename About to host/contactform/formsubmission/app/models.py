from django.db import models

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    title = models.CharField(max_length = 200)
    description = models.TextField()
        
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + self.message
