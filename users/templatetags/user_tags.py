from django import template

'''
Create a custom template tag for determining a user's group, e.g. Admin, Instructor, or Student
'''

register = template.Library()

@register.filter('has_group')
def has_group(user, group_name):
    if user.groups.filter(name=group_name).exists():
        return True
    else:
        return False
