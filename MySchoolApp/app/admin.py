from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
import datetime 
from .models import Admin, Teacher, Student, Parent, Gender, Address, Qualification, Klass, EnrollmentInfo


# Define a custom UserAdmin for each user type
class AdminUserAdmin(UserAdmin):
    model = Admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups', 'user_permissions')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'street', 'city', 'state')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super().save_model(request, obj, form, change)

class TeacherUserAdmin(UserAdmin):
    model = Teacher
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups', 'user_permissions')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


class StudentUserAdmin(UserAdmin):
    model = Student
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups', 'user_permissions')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


class ParentUserAdmin(UserAdmin):
    model = Parent
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups', 'user_permissions')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


# Register the models and their custom UserAdmin classes with the admin site
admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)

# Register the remaining models
admin.site.register(Gender)
admin.site.register(Address)
admin.site.register(Qualification)
admin.site.register(Klass)
admin.site.register(EnrollmentInfo)

# Remove the Group model from the admin site
admin.site.unregister(Group)

# create an instance of the related models
# address = Address.objects.create(street='123 Main St', city='New York', state='NY', country='USA')
# gender = Gender.objects.create(gender='F')
# date = datetime.date(2021, 3, 14)
# # create an instance of the Admin model with required fields
# admin = Admin.objects.create(
#     first_name='White',
#     last_name='Black',
#     username='Greenwish',  # Provide a value for the username field
#     email='whitegg@example.com',
#     password='password',
#     dob=date,
#     gender=gender,
#     phone_number='+234-706-807-4131',
#     address=address,
# )



# admin = Admin.objects.filter(username='whitegg').first()
# if admin:
#     print('Username is already taken')
# else:
#    print('Enter another name')


# # create an instance of the related models
# address = Address.objects.create(street='123 Main St', city='New York', state='NY', country='USA')
# gender = Gender.objects.create(gender='F')

# # create an instance of the Admin model with required fields
# admin = Admin.objects.create(
#     first_name='White',
#     last_name='Black',
#     username='whitegg',
#     email='whitegg@example.com',
#     password='password',
#     dob=datetime.date.today(),
#     gender=gender,
#     phone_number='+234-706-807-4131',
#     address=address,
# )