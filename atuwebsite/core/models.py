from django.db import models
from django.contrib.auth.models import User 

class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    SEMESTER_CHOICES = (
        ('First Semester', 'First Semester'),
        ('Second Semester', 'Second Semester'),
    )

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='courses')
    course_name = models.CharField(max_length=200)
    # course_year = models.CharField(max_length=4)
    semester = models.CharField(max_length=100, choices=SEMESTER_CHOICES)
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    file = models.FileField(upload_to='courses/')  # For uploading PDF files

    def __str__(self):
        return self.course_name


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    payment_reference = models.CharField(max_length=100)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bought {self.course.course_name}"
