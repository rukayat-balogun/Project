from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType



class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

class Gender(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non-binary'),
        ('O', 'Other'),
    )

    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)

    def __str__(self):
        return self.get_gender_display()
   
       
class Occupation(models.Model):
    name = models.CharField(max_length=50)
    

class Qualification(models.Model):
    name = models.CharField(max_length=50)
    

class Klass(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(
        "Student",
        related_name="classes",
        blank=True,
        verbose_name=("students"),
        help_text=("The students in this class."),
    )
    teachers = models.ManyToManyField(
        "Teacher",
        related_name="classes",
        blank=True,
        verbose_name=("teachers"),
        help_text=("The teachers in this class."),
    )
    
    def __str__(self):
        return self.name

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField(default=timezone.now)
    klass = models.ForeignKey(Klass, on_delete=models.CASCADE)


class EnrollmentInfo(models.Model):
    date = models.DateField()
    enrollement_class = models.ForeignKey(Klass, on_delete=models.CASCADE)
    
class Admin(AbstractUser):
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non-binary'),
        ('O', 'Other'),
    )
    
    first_name = models.CharField(max_length=100, blank=True, null=True,)
    last_name = models.CharField(max_length=100, blank=True, null=True,)
    street = models.CharField(max_length=100, blank=True, null=True,)
    city = models.CharField(max_length=50, blank=True, null=True,)
    state = models.CharField(max_length=50, blank=True, null=True,)
    country = models.CharField(max_length=50, blank=True, null=True,)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=2, blank=True, null=True , choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    qualification = models.CharField(max_length=50, blank=True, null=True)
   # address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.CASCADE)
    
    class Meta:
        permissions = [
            ("can_view_sensitive_data", "Can view sensitive data"),
            ("can_edit_data", "Can edit data"),
            ("can_delete_data", "Can delete data"),
        ]

    # Add related name and groups
    groups = models.ManyToManyField(
        Group,
        related_name="admin_users",
        blank=True,
        verbose_name=("groups"),
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
    )

    # Add user_permissions
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="admin_users",
        blank=True,
        verbose_name=("user permissions"),
        help_text=("Specific permissions for this user."),
    )

    def __str__(self):
        return self.username
    
class Teacher(AbstractUser):
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    groups = models.ManyToManyField(
        Group,
        related_name="teacher_users",
        blank=True,
        verbose_name=("groups"),
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="teacher_users",
        blank=True,
        verbose_name=("user permissions"),
        help_text=("Specific permissions for this user."),
    )

    def add_student(self, student):
        # Add the student to the teacher's class or section
        pass
    
    def add_class(self, Klass):
        # Add the student to the teacher's class or section
        pass
    
    def add_subject(self, subject):
        # Add the student to the teacher's class or section
        pass
    

    def add_score(self, student, score):
        # Add a score for the student
        pass

    def add_attendance(self, student, date, is_present):
        # Add attendance for the student on the given date
        pass
    
    class Meta:
        permissions = [
            ('view_attendance', 'Can view attendance'),
            ('edit_attendance', 'Can edit attendance'),
            ('delete_attendance', 'Can delete attendance'),
            ('view_grades', 'Can view grades'),
            ('edit_grades', 'Can edit grades'),
            ('delete_grades', 'Can delete grades'),
        ]
    
class Parent(AbstractUser):
    occupation = models.CharField(max_length=100)
    groups = models.ManyToManyField(
        Group,
        related_name="parent_users",
        blank=True,
        verbose_name=("groups"),
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="parent_users",
        blank=True,
        verbose_name=("user permissions"),
        help_text=("Specific permissions for this user."),
    )
    
    def view_result(self, student):
        # Retrieve and return the student's result
        pass
    
    class Meta:
        permissions = [
            ('view_attendance', 'Can view attendance'),
            ('view_grades', 'Can view grades'),
        ]


class Student(AbstractUser):
    enrollment = models.ForeignKey(EnrollmentInfo, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    groups = models.ManyToManyField(
        Group,
        related_name="student_users",
        blank=True,
        verbose_name=("groups"),
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="student_users",
        blank=True,
        verbose_name=("user permissions"),
        help_text=("Specific permissions for this user."),
    )
    
    
    
    def view_result(self, student):
        # Retrieve and return the student's result
        pass
    
    def __str__(self):
        return self.username
    
    class Meta:
        permissions = [
            ('view_attendance', 'Can view attendance'),
            ('view_grades', 'Can view grades'),
        ]


class Grade(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    
