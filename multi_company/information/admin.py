from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Role)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_time', 'end_time', 'date')



@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reason', 'start_date', 'end_date', 'approved') 
    #list_filter = ('approved', 'reason')
    #search_fields = ('employee__user__username', 'reason')


