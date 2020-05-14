from django.contrib.auth.decorators import user_passes_test

def group_required(*group_names):
    def in_group(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)):
                return True
            return False
    return user_passes_test(in_group)

'''
def can_view_profile(requested_user_profile):
    ''''''
    check if the user has permission to view a specific user profile
    students and instructors can only view their own profiles, admins can view any profile
    ''''''
    def can_view(user):
        if user.is_authenticated:
            if user.groups.filter(name__in='Admin'):
                return True
            elif user.pk == requested_user_profile.pk:
                return True
        return False
    return user_passes_test(can_view)
'''