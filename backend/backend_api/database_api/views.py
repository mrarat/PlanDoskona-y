from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import CourseGroup

def get_int_param(request, param_name):
    try:
        value = int(request.GET.get(param_name))
    except (TypeError, ValueError):
        value = None
    return value

@require_http_methods(["GET"])
def submit_course_group(request):
    course_unit_id = get_int_param(request, 'course_unit_id')
    group_number = get_int_param(request, 'group_number')

    if course_unit_id is None or group_number is None:
        return JsonResponse({'status': 'error', 'message': 'Invalid or missing course_unit_id or group_number'}, status=400)

    course_group, created = CourseGroup.objects.get_or_create(
        course_unit_id=course_unit_id, group_number=group_number,
        defaults={'submit_count': 1}
    )

    if not created:
        course_group.submit_count += 1
        course_group.save()

    return JsonResponse({'status': 'success'})

@require_http_methods(["GET"])
def get_course_groups(request):
    course_unit_id = get_int_param(request, 'course_unit_id')

    if course_unit_id is None:
        return JsonResponse({'status': 'error', 'message': 'Invalid or missing course_unit_id'}, status=400)

    course_groups = CourseGroup.objects.filter(course_unit_id=course_unit_id)
    data = [{'id': cg.id, 'course_unit_id': cg.course_unit_id, 'group_number': cg.group_number, 'submit_count': cg.submit_count} for cg in course_groups]
    return JsonResponse(data, safe=False)
