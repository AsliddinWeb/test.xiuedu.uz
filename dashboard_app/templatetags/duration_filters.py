from django import template

register = template.Library()

@register.filter(name='duration_in_minutes')
def get_duration_in_minutes(start_time, end_time):
    if start_time is None or end_time is None:
        return None  # Agar start_time yoki end_time None bo'lsa, natija ham None bo'ladi

    duration = end_time - start_time
    duration_in_minutes = duration.total_seconds() // 60
    return duration_in_minutes
