from django.urls import path, include
from rest_framework import routers
from .views import HackathonViewSet, SubmissionViewSet, UserHackathonEnrollmentViewSet, UserSubmissionViewSet, UserRegistrationViewSet

router = routers.DefaultRouter()
router.register(r'hackathons', HackathonViewSet, basename='hackathon')
router.register(r'hackathons/(?P<hackathon_id>\d+)/submissions', SubmissionViewSet, basename='submission')
#router.register(r'register', HackathonRegistrationViewSet, basename='register')
router.register(r'register', UserRegistrationViewSet, basename='user-registration')
router.register(r'users/(?P<user_id>\d+)/enrollments', UserHackathonEnrollmentViewSet, basename='enrollment')
router.register(r'users/(?P<user_id>\d+)/submissions', UserSubmissionViewSet, basename='user_submission')

urlpatterns = [
    path('', include(router.urls)),
    path('refresh-token/', UserRegistrationViewSet.as_view({'post': 'refresh_token'}), name='refresh-token'),
]


