# create groups for each user type
# admin_group = Group.objects.create(name='Admin')
# teacher_group = Group.objects.create(name='Teacher')
# parent_group = Group.objects.create(name='Parent')
# student_group = Group.objects.create(name='Student')

# # add admin user to the admin group
# admin_user = Admin.objects.create(username='admin')
# admin_user.set_password('password')
# admin_user.save()
# admin_group.user_set.add(admin_user)

# # add permissions for teachers to add students, subjects, and classes
# permission = Permission.objects.get(name='Can add student')
# teacher_group.permissions.add(permission)
# permission = Permission.objects.get(codename='Can add subject')
# teacher_group.permissions.add(permission)
# permission = Permission.objects.get(codename='Can add class')
# teacher_group.permissions.add(permission)

# # remove permissions for parents to add or change any models
# parent_group.permissions.clear()




# content_types = ContentType.objects.all()
# permissions = Permission.objects.filter(content_type__in=content_types)
# admin_group.permissions.set(permissions)

# assignment_ct = ContentType.objects.get_for_model(Assignment)
# grade_ct = ContentType.objects.get_for_model(Grade)
# assignment_permissions = Permission.objects.filter(content_type=assignment_ct)
# grade_permissions = Permission.objects.filter(content_type=grade_ct)

# teacher_group.permissions.set(list(assignment_permissions) + list(grade_permissions))
