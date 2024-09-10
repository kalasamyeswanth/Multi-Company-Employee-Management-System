from django import forms
from .models import *


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        # fields = ['name', 'address', 'contact_information', 'logo']


class EmployeeForm(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = ['name', 'employee_id', 'company', 'department', 'role', 'joining_date', 'salary']
    
    

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'




class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'



class AttendanceForms(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        

class LeaveRequestForms(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        
        '''widgets = {
            'employee': forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['employee'].initial = self.instance.author.id
    
        #clean funtion for validation purposse
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date and start_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be before start date.")

'''