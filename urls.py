from django.urls import path
from . import views



urlpatterns = [
    path('accounts/register/', views.signup, name='signup'),  # Correct path for signup
    path('accounts/login/', views.login, name='login'),  # Correct path for login
    path('staff/', views.staff, name='staff'),
    path('store-student-data/', views.store_student_data, name='store_student_data'),
#    path('attendance/records/<str:staff_name>/<str:course_code>/<str:date>/', RecordAttendanceView.as_view(), name='attendance_records'),
    path('attendance/record/', views.record_attendance, name='record_attendance'),
    path('attendance/view/',views.view_attendance,name='view'),
    path('attendance/update/<str:roll_number>/', views.update_attendance_status, name='update_attendance_status'),
    path('accounts/request-reset-otp/', views.send_reset_otp, name='request_reset_otp'),
    
    # URL for resetting the password with OTP
    path('accounts/reset-password/', views.reset_password, name='reset_password'),
]
