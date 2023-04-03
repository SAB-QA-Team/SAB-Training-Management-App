from django.urls import path, include
from .views import *
from .trainee_views import *
from .manager_views import *

urlpatterns = [
    #Login and Registration
    path('login/', login_view, name='login'),
    path('',login_view),
    path('register/', register_trainee, name='register'),
    #2fa
    path('qr-code/', qr_code, name='qr-code'),
    path('two-factor-auth/', two_factor_auth, name='two-factor-auth'),
    path('two-factor-auth-setup/', two_factor_auth_setup, name='two-factor-auth-setup'),

    path('profile/', profile, name='profile'),
    path('contact/', contact, name='contact'),

    path('logout/', logout_view, name='logout'),

    #Admin Specific Links
    path('dashboard/', dashboard, name='admin-dashboard'),
    path('instructors/', InstructorList.as_view(), name="instructors"),
    path('instructor/<int:pk>/', InstructorDetail.as_view(), name="instructor"),
    path('instructor-create/', InstructorCreate.as_view(), name="instructor-create"),
    path('instructor-update/<int:pk>/', InstructorUpdate.as_view(), name="instructor-update"),
    path('instructor-delete/<int:pk>/', InstructorDelete.as_view(), name="instructor-delete"),
    path('courses/', CourseList.as_view(), name="courses"),
    path('course/<int:pk>/', CourseDetail.as_view(), name="course"),
    path('course-create/', CourseCreate.as_view(), name="course-create"),
    path('course-update/<int:pk>/', CourseUpdate.as_view(), name="course-update"),
    path('course-delete/<int:pk>/', CourseDelete.as_view(), name="course-delete"),
    path('increment_course/<int:course_id>/', increment_session, name="increment-session"),
    path('managers/', manager_list, name="managers"),
    path('manager/<int:pk>/', ManagerDetail.as_view(), name="manager"),
    path('manager-create/', create_manager, name="manager-create"),
    path('manager-update/<int:manager_id>/', edit_manager, name="manager-update"),
    path('manager-delete/<int:pk>/', delete_manager, name="manager-delete"),
    path('trainees/', trainee_list, name="trainees"),
    path('trainee/<int:pk>/', TraineeDetail.as_view(), name="trainee"),
    path('trainee-create/', TraineeCreate.as_view(), name="trainee-create"),
    path('trainee-update/<int:trainee_id>/', edit_trainee, name="trainee-update"),
    path('trainee-delete/<int:pk>/', delete_trainee, name="trainee-delete"),

    #Manager Specific Links
    path('my-trainees/', managerTrainees, name="manager-trainees"),
    path('my-trainees-courses/<int:trainee_id>/', traineeCourses, name="trainee-courses"),
    #Trainee Specific Links
    path('courses_list/', courses_list, name='courses-list'),
    path('course_list/<int:course_id>/', course_details, name='course-details'),
    path('register_course/<int:course_id>/', register_course, name='register-course'),
    path('my-courses/', trainee_courses, name="my-courses"),
    path('attendance-delete/<int:course_id>/', drop_course, name="drop-course"),
    path('enter-class/<int:course_id>/', enter_class, name="enter-class"),
    path('exit-class/<int:course_id>/', exist_class, name="exit-class"),
]