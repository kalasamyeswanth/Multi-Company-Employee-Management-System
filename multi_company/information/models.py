from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import date

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    contact_information = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/',null = True, blank = True)

    def __str__(self):
        return self.name
    

class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Role(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Employee(models.Model):
    ROLE_CHOICES = (
        ('Admin','Admin'),
        ('Manager','Manager'),
        ('Employee','Employee'),
        ('HR Manager', 'HR Manager'),
    )
    name = models.OneToOneField(User, on_delete=models.CASCADE)  # Assuming you use Django's User #model for authentication
    employee_id = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.CharField(max_length=30,choices=ROLE_CHOICES)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name.username
    

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time= models.DateTimeField(null=True, blank= True)
    end_time= models.DateTimeField(null=True, blank= True)
    date = models.DateField(default=date.today)
    
    def __str__(self):
        return f'{self.employee.name} - {self.start_time} to {self.end_time}'


class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('Sick', 'Sick'),
        ('Vacation', 'Vacation'),
        ('Personal', 'Personal'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reason= models.CharField(max_length=50, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(max_length=30, choices=STATUS_CHOICES,blank= True, null= True)

    def __str__(self):
        return f'{self.employee.name} - {self.start_date} to {self.end_date}'



