from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.http import HttpResponseForbidden
from .serializers import *
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.db.models import Sum, F
from collections import defaultdict


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redirect to a success page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def role_required(allowed_roles=[]):
    
    def decorator(view_fun):
        def wrapper_func(request,*args,**kwargs):
            global user_role, user_company, user_name
            user_role = request.user.employee.role
            user_company = request.user.employee.company
            user_name = request.user.employee.name
            #print(user_name)
            #print(user_role)
            if user_role in allowed_roles :
                return view_fun(request, *args,**kwargs)
            else:
                return HttpResponseForbidden('you dont have permissions to access this page')
        return wrapper_func
    return decorator


@role_required(allowed_roles=['Admin'])
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'company_list.html', {'companies': companies})


@role_required(allowed_roles=['Admin'])
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk, name = user_company)
    return render(request, 'company_detail.html', {'company': company})


@role_required(allowed_roles=['Admin'])
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'company_form.html', {'form': form})


@role_required(allowed_roles=['Admin'])
def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk, name = user_company)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_detail', pk=pk)
    else:
        form = CompanyForm(instance=company)
    return render(request, 'company_form.html', {'form': form})


@role_required(allowed_roles=['Admin'])
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk, name = user_company)
    if request.method == 'POST':
        company.delete()
        return redirect('company_list')
    return render(request, 'company_confirm_delete.html', {'company': company})
    

@role_required(allowed_roles=['HR Manager', 'Manager'])
def employee_list(request):
    if user_role == 'HR Manager':
        employee = Employee.objects.all()
    if user_role == 'Manager':
        employee = Employee.objects.filter(department = request.user.department)
    if user_role == 'Manager' and employee.department != request.user.department:
        return HttpResponseForbidden('you dont have permissions to access this page')
    return render(request, 'employee_list.html', {'employee': employee})


@role_required(allowed_roles=['HR Manager', 'Employee', 'Manager'])
def employee_detail(request, pk):
    employee = Employee.objects.filter(pk = pk, company = user_company)
    if user_role == 'Manager' and employee.department != request.user.department:
        return HttpResponseForbidden('you dont have permissions to access this page')
    return render(request, 'employee_detail.html', {'employee': employee})


@role_required(allowed_roles=['HR Manager', 'Manager'])
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})


@role_required(allowed_roles=['HR Manager', 'Employee', 'Manager'])
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk, company = user_company)
    if user_role == 'Manager' and employee.department != request.user.department:
        return HttpResponseForbidden('you dont have permissions to access this page')
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', pk=pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})


@role_required(allowed_roles=['HR Manager', 'Employee'])
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk, company = user_company)
    if user_role == 'Manager' and employee.department != request.user.department:
        return HttpResponseForbidden('you dont have permissions to access this page')
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})


@role_required(allowed_roles=['HR Manager'])
def Department_list(request):
    department = Department.objects.all()
    return render(request, 'department_list.html', {'department': department})


@role_required(allowed_roles=[ 'HR Manager'])
def Department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk, company = user_company)
    return render(request, 'department_detail.html', {'department': department})


@role_required(allowed_roles=['HR Manager'])
def Department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Department_list')
    else:
        form = DepartmentForm()
    return render(request, 'department_form.html', {'form': form})


@role_required(allowed_roles=['HR Manager'])
def Department_update(request, pk):
    department = get_object_or_404(Department, pk=pk, company = user_company)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            return redirect('Department_detail', pk=pk)
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'department_form.html', {'form': form})


@role_required(allowed_roles=['HR Manager'])
def Department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk, company = user_company)
    if request.method == 'POST':
        department.delete()
        return redirect('Department_list')
    return render(request, 'department_confirm_delete.html', {'department': department})


@role_required(allowed_roles=['HR Manager'])
def Role_list(request):
    role = Role.objects.all()
    return render(request, 'role_list.html', {'role': role})


@role_required(allowed_roles=['HR Manager'])
def Role_detail(request, pk):
    role = get_object_or_404(Role, pk=pk, company = user_company)
    return render(request, 'role_detail.html', {'role': role})

@role_required(allowed_roles=['HR Manager'])
def Role_create(request):
    if request.method == 'POST':
        form = RoleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Role_list')
    else:
        form = RoleForm()
    return render(request, 'role_form.html', {'form': form})


@role_required(allowed_roles=['HR Manager'])
def Role_update(request, pk):
    role = get_object_or_404(Role, pk=pk, company = user_company)
    if request.method == 'POST':
        form = RoleForm(request.POST, request.FILES, instance=role)
        if form.is_valid():
            form.save()
            return redirect('Role_detail', pk=pk)
    else:
        form = RoleForm(instance=role)
    return render(request, 'role_form.html', {'form': form})


@role_required(allowed_roles=['HR Manager'])
def Role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk, company = user_company)
    if request.method == 'POST':
        role.delete()
        return redirect('Role_list')
    return render(request, 'role_confirm_delete.html', {'role': role})



@role_required(allowed_roles=['HR Manager', 'Admin', 'Manager', 'Employee'])
def Leave_Request_list(request):
    leave = LeaveRequest.objects.all()
    return render(request, 'leave_request_list.html', {'leave': leave})

@role_required(allowed_roles=['HR Manager', 'Admin', 'Manager', 'Employee'])
def Leave_Request_create(request):
    if request.method == 'POST':
        form = LeaveRequestForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Leave_Request_list')
    else:
        form = RoleForm()
    return render(request, 'leave_request_form.html', {'form': form})

@role_required(allowed_roles=['HR Manager', 'Admin', 'Manager', 'Employee'])
def Leave_Request_update(request, pk):
    leave = get_object_or_404(LeaveRequest, pk = pk)
    if request.method == 'POST':
        form = LeaveRequestForms(request.POST, request.FILES, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('Leave_Request_list')
    else:
        form = LeaveRequestForms(instance = leave)
    return render(request, 'leave_request_form.html', {'form': form})

@role_required(allowed_roles=['HR Manager', 'Admin', 'Manager', 'Employee'])
def Leave_Request_delete(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        leave.delete()
        return redirect('Leave_Request_list')
    return render(request, 'leave_request_confirm_delete.html', {'leave': leave})



@role_required(allowed_roles=['Admin', 'HR Manager'])
def Manage_Leave_Requests(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'manage_leave_requests.html', {'leave_requests': leave_requests})


def Approve_Leave_Request(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    leave_request.approved = 'Approved'
    leave_request.save()
    return redirect('Manage_Leave_Requests')

@role_required(allowed_roles=['Admin', 'HR Manager'])
def Reject_Leave_Request(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    leave_request.approved = 'Rejected'
    leave_request.save()
    return redirect('Manage_Leave_Requests')


def Attendance_list(request):
    attendance = Attendance.objects.all()
    return render(request, 'attendance_list.html', {'attendance': attendance})


def Attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Attendance_list')
    else:
        form = AttendanceForms()
    return render(request, 'attendance_form.html', {'form': form})


def Attendance_update(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = LeaveRequestForms(request.POST, request.FILES, instance = attendance)
        if form.is_valid():
            form.save()
            return redirect('Attendance_list')
    else:
        form = LeaveRequestForms(instance=attendance)
    return render(request, 'attendance_form.html', {'form': form})



def Attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('Attendance_list')
    return render(request, 'attendance_confirm_delete.html', {'attendance': attendance})



class Company_API(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


class Department_API(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class Role_API(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class Employee_API(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class Attendance_API(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    

class LeaveRequest_API(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]


def get_attendance_data(employee_id, start_date, end_date):
    return Attendance.objects.filter(
        employee_id=employee_id,
        start_time__date__range=[start_date, end_date]
    ).annotate(
        total_hours=F('end_time') - F('start_time')
    ).values('start_time__date').annotate(total_hours=Sum('total_hours'))


def format_attendance_data(attendance_data):
    formatted_data = {
        'dates': [],
        'hours': []
    }
    for record in attendance_data:
        formatted_data['dates'].append(record['start_time__date'])
        formatted_data['hours'].append(record['total_hours'])
    return formatted_data

def attendance_report(request):
    employee_id = request.GET.get('employee_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    attendance_data = get_attendance_data(employee_id, start_date, end_date)
    formatted_data = format_attendance_data(attendance_data)

    return render(request, 'attendance_report.html', {
        'dates': formatted_data['dates'],
        'hours': formatted_data['hours'],
    })


def get_leave_data(employee_id, start_date, end_date):
    return LeaveRequest.objects.filter(
        employee_id=employee_id,
        start_date__lte=end_date,
        end_date__gte=start_date
    ).values('start_date', 'end_date', 'reason', 'approved')



def format_leave_data(leave_data):
    leave_summary = defaultdict(int)
    for record in leave_data:
        start = record['start_date']
        end = record['end_date']
        # Assuming all leaves are taken in full days
        total_days = (end - start).days + 1
        current_date = start
        while current_date <= end:
            leave_summary[current_date.strftime('%Y-%m-%d')] += 1
            current_date += timedelta(days=1)

    formatted_data = {
        'dates': list(leave_summary.keys()),
        'days': list(leave_summary.values())
    }
    return formatted_data


def leave_report(request):
    employee_id = request.GET.get('employee_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    leave_data = get_leave_data(employee_id, start_date, end_date)
    formatted_data = format_leave_data(leave_data)

    return render(request, 'leave_report.html', {
        'dates': formatted_data['dates'],
        'days': formatted_data['days'],
    })
