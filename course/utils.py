from .models import CourseUnit

def map_course_units(course_sections):
    '''
    maps course units to their parent course sections
    '''
    course_units = {}
    for section in course_sections:
        section_units = CourseUnit.objects.filter(section=section).order_by('unit_order_num')
        course_units[section] = section_units
    return course_units
