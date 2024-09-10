from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import *
from django.utils.timezone import now
from django.http import HttpResponseForbidden

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    try:
        employee = Employee.objects.get(name=user)
        Attendance.objects.create(employee=employee, start_time=now(), date=now().date())
    except Employee.DoesNotExist:
        return HttpResponseForbidden(' the employee is not exist here ')


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    try:
        employee = Employee.objects.get(name=user)
        attendance = Attendance.objects.filter(employee=employee, end_time__isnull=True, date=now().date()).latest('start_time')
        attendance.end_time = now()
        attendance.save()
    except Employee.DoesNotExist:
        return HttpResponseForbidden(' the employee is not exist here ')
    
    except Attendance.DoesNotExist:
        return HttpResponseForbidden(' here the attendance record is not match ')

