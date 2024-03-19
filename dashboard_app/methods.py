from datetime import timedelta

def get_duration_in_minutes(start_time, end_time):
    duration = end_time - start_time
    duration_in_minutes = duration.total_seconds() / 60
    return duration_in_minutes