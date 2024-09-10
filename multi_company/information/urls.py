from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from two_factor.urls import urlpatterns as tf_urls
from two_factor.views import SetupView, ProfileView

router = DefaultRouter()
router.register(r'company', Company_API)
router.register(r'employee', Employee_API)
router.register(r'department', Department_API)
router.register(r'role', Role_API)
router.register(r'attendance', Attendance_API)
router.register(r'leaverequest', LeaveRequest_API)


urlpatterns = [
    path('account/', include(tf_urls)),

    path('account/two_factor/setup/', SetupView.as_view(), name='setup'),
    path('account/two_factor/profile/', ProfileView.as_view(), name='profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('companies/', company_list, name='company_list'),
    path('companies/<int:pk>/', company_detail, name='company_detail'),
    path('companies/create/', company_create, name='company_create'),
    path('companies/<int:pk>/update/', company_update, name='company_update'),
    path('companies/<int:pk>/delete/', company_delete, name='company_delete'),


    path('api/',include(router.urls)),

    
    path('employee/', employee_list, name='employee_list'),
    path('employee/<int:pk>/', employee_detail, name='employee_detail'),
    path('employee/create/', employee_create, name='employee_create'),
    path('employee/<int:pk>/update/', employee_update, name='employee_update'),
    path('employee/<int:pk>/delete/', employee_delete, name='employee_delete'),


    path('department/', Department_list, name='Department_list'),
    path('department/<int:pk>/', Department_detail, name='Department_detail'),
    path('department/create/', Department_create, name='Department_create'),
    path('department/<int:pk>/update/', Department_update, name='Department_update'),
    path('department/<int:pk>/delete/', Department_delete, name='Department_delete'),


    path('role_list/', Role_list, name='Role_list'),
    path('role_list/<int:pk>/', Role_detail, name='Role_detail'),
    path('role_list/create/', Role_create, name='Role_create'),
    path('role_list/<int:pk>/update/', Role_update, name='Role_update'),
    path('role_list/<int:pk>/delete/', Role_delete, name='Role_delete'),


    path('leave/', Leave_Request_list, name='Leave_Request_list'),
    path('leave/create/', Leave_Request_create, name='Leave_Request_create'),
    path('leave/<int:pk>/update/', Leave_Request_update, name='Leave_Request_update'),
    path('leave/<int:pk>/delete/', Leave_Request_delete, name='Leave_Request_delete'),


    path('attendance/', Attendance_list, name='Attendance_list'),
    path('attendance/create/', Attendance_create, name='Attendance_create'),
    path('attendance/<int:pk>/update/', Attendance_update, name='Attendance_update'),
    path('attendance/<int:pk>/delete/', Attendance_delete, name='Attendance_delete'),

    path('manage_leave/',Manage_Leave_Requests, name = 'Manage_Leave_Requests'),

    path('leave-report/', leave_report, name='leave_report'),
    path('attendance-report/', attendance_report, name='attendance_report'),
]
