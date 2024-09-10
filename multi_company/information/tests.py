from django.test import TestCase
from .models import *
from .forms import *
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from .models import Company, Department, Employee, Attendance
from datetime import datetime



# Create your tests here.
class CompanyModelTests(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            address="123 Test Street",
            contact_information="123-456-7890",
            logo=None
        )

    def test_company_creation(self):
        self.assertEqual(self.company.name, "Test Company")
        self.assertEqual(self.company.address, "123 Test Street")
        self.assertEqual(self.company.contact_information, "123-456-7890")
        self.assertIsNone(self.company.logo)



class CompanyFormTests(TestCase):

    def test_valid_form(self):
        form_data = {
            'name': 'Valid Company',
            'address': '456 Valid Road',
            'contact_information': '987-654-3210',
            'logo': None
        }
        form = CompanyForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Company.objects.count(), 1)

    def test_invalid_form(self):
        form_data = {
            'name': 'yeswanth',  
            'address': '456 Invalid Road',
            'contact_information': '987-654-3210',
            'logo': None
        }
        form = CompanyForm(data=form_data)
        self.assertFalse(form.is_valid())


class DepartmentModelTests(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            address="123 Test Street",
            contact_information="123-456-7890",
            logo=None
        )
        self.department = Department.objects.create(
            name="HR",
            company=self.company
        )

    def test_department_creation(self):
        self.assertEqual(self.department.name, "HR")
        self.assertEqual(self.department.company, self.company)
        self.assertEqual(Department.objects.count(), 1)

    def test_department_str(self):
        self.assertEqual(str(self.department), "HR") 


class DepartmentFormTests(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            address="123 Test Street",
            contact_information="123-456-7890",
            logo=None
        )

    def test_valid_form(self):
        form_data = {
            'name': 'HR',
            'company': self.company.id
        }
        form = DepartmentForm(data=form_data)
        self.assertTrue(form.is_valid())
        department = form.save()
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(department.name, 'HR')
        self.assertEqual(department.company, self.company)

    def test_invalid_form(self):
        form_data = {
            'name': '',  # Invalid because name is required
            'company': self.company.id
        }
        form = DepartmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)




class RoleAPITests(APITestCase):

    def setUp(self):
        self.company = Company.objects.create(
            name="API Company",
            address="456 API Road",
            contact_information="987-654-3210",
            logo=None
        )
        self.role = Role.objects.create(
            title="Manager",
            company=self.company
        )
        self.api_url = '/api/roles/'  # Adjust to your actual API endpoint

    def test_get_role(self):
        response = self.client.get(f'{self.api_url}{self.role.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['title'], 'Manager')

    def test_create_role(self):
        data = {
            'title': 'Developer',
            'company': self.company.id
        }
        response = self.client.post(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 2)

    def test_update_role(self):
        data = {'title': 'Updated Manager'}
        response = self.client.patch(f'{self.api_url}{self.role.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.title, 'Updated Manager')

    def test_delete_role(self):
        response = self.client.delete(f'{self.api_url}{self.role.title}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Role.objects.count(), 0)


class RoleFormTests(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            address="123 Test Street",
            contact_information="123-456-7890",
            logo=None
        )

    def test_valid_form(self):
        form_data = {
            'title': 'HR Manager',
            'company': self.company.id
        }
        form = RoleForm(data=form_data)
        self.assertTrue(form.is_valid())
        role = form.save()
        self.assertEqual(Role.objects.count(), 1)
        self.assertEqual(role.title, 'HR Manager')
        self.assertEqual(role.company, self.company)

    def test_invalid_form(self):
        form_data = {
            'title': '',  # -> Invalid because title is required
            'company': self.company.id
        }
        form = RoleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class EmployeeAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.company = Company.objects.create(
            name="Test Company",
            address="123 Test Street",
            contact_information="123-456-7890",
            logo=None
        )
        self.department = Department.objects.create(
            name="HR",
            company=self.company
        )
        self.employee = Employee.objects.create(
            name=self.user,
            employee_id="EMP001",
            company=self.company,
            department=self.department,
            role="Manager",
            joining_date="2024-01-01",
            salary=60000.00
        )
        self.api_url = '/api/employees/'  

    def test_get_employee(self):
        response = self.client.get(f'{self.api_url}{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee_id'], 'EMP001')

    def test_create_employee(self):
        data = {
            'name': self.user.username,
            'employee_id': 'EMP002',
            'company': self.company.id,
            'department': self.department.id,
            'role': 'Admin',
            'joining_date': '2024-02-01',
            'salary': 70000.00
        }
        response = self.client.post(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_update_employee(self):
        data = {'salary': 65000.00}
        response = self.client.patch(f'{self.api_url}{self.employee.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.salary, 65000.00)

    def test_delete_employee(self):
        response = self.client.delete(f'{self.api_url}{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)


class EmployeeFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.company = Company.objects.create(
            name="Test Company",
            address="123 Test Street",
            contact_information="123-456-7890",
            logo=None
        )
        self.department = Department.objects.create(
            name="HR",
            company=self.company
        )

    def test_valid_form(self):
        form_data = {
            'name': self.user.id,
            'employee_id': 'EMP003',
            'company': self.company.id,
            'department': self.department.id,
            'role': 'Employee',
            'joining_date': '2024-03-01',
            'salary': 50000.00
        }
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid())
        employee = form.save()
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(employee.employee_id, 'EMP003')

    def test_invalid_form(self):
        form_data = {
            'name': self.user.id,
            'employee_id': '',  # ->Invalid because employee_id is required
            'company': self.company.id,
            'department': self.department.id,
            'role': 'Employee',
            'joining_date': '2024-03-01',
            'salary': 50000.00
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class AttendanceAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='abc_hr', password='password')
        self.company = Company.objects.create(
            name="Test Company",
            address="123 Test Street",
            contact_information="123-456-7890",
            logo=None
        )
        self.department = Department.objects.create(
            name="HR",
            company=self.company
        )
        self.employee = Employee.objects.create(
            name=self.user,
            employee_id="EMP001",
            company=self.company,
            department=self.department,
            role="Manager",
            joining_date="2024-01-01",
            salary=60000.00
        )
        self.attendance = Attendance.objects.create(
            employee=self.employee,
            start_time="2024-09-10T09:00:00Z",
            end_time="2024-09-10T17:00:00Z",
            date="2024-09-10"
        )
        self.api_url = '/api/attendances/'  # Adjust to your actual API endpoint

    def test_get_attendance(self):
        response = self.client.get(f'{self.api_url}{self.attendance.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee'], self.employee.id)

    def test_create_attendance(self):
        data = {
            'employee': self.employee.name,
            'start_time': '2024-09-11T09:00:00Z',
            'end_time': '2024-09-11T17:00:00Z',
            'date': '2024-09-11'
        }
        response = self.client.post(self.api_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 2)

    def test_update_attendance(self):
        data = {'end_time': '2024-09-10T18:00:00Z'}
        response = self.client.patch(f'{self.api_url}{self.attendance.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attendance.refresh_from_db()
        self.assertEqual(self.attendance.end_time, '2024-09-10T18:00:00Z')

    def test_delete_attendance(self):
        response = self.client.delete(f'{self.api_url}{self.attendance.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Attendance.objects.count(), 0)


