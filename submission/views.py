from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Hackathon, Submission, Enrollment
from .serializers import HackathonSerializer, SubmissionSerializer,EnrollmentSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action


class HackathonViewSet(viewsets.ModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Only authorized users can create hackathons.'}, status=status.HTTP_401_UNAUTHORIZED)

        return super().create(request, *args, **kwargs)

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        hackathon_id = self.kwargs['hackathon_id']
        return Submission.objects.filter(hackathon_id=hackathon_id)

    def create(self, request, hackathon_id=None):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        try:
            hackathon = Hackathon.objects.get(id=hackathon_id)
        except Hackathon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(hackathon=hackathon, user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, hackathon_id=None):
        try:
            hackathon = Hackathon.objects.get(id=hackathon_id)
        except Hackathon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        submissions = self.get_queryset()
        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)


class UserRegistrationViewSet(viewsets.ViewSet):
    def create(self, request):
        # Get the registration data from the request
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if the user already exists
        user, created = User.objects.get_or_create(username=username)

        if created:
            # Set the user's password if it's a new user
            user.set_password(password)
            user.save()

        # Generate a new access token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the access token in the response
        return Response({'access_token': access_token}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        # Get the refresh token from the request data
        refresh_token = request.data.get('refresh_token')

        try:
            # Attempt to validate the refresh token
            token = RefreshToken(refresh_token)
            # Check if the refresh token is expired
            if token.is_expired:
                return Response({'error': 'Refresh token has expired.'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate a new access token
            access_token = str(token.access_token)

            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)


class UserHackathonEnrollmentViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, user_id=None):
        # Get the enrollment data from the request
        hackathon_id = request.data.get('hackathon_id')

        try:
            hackathon = Hackathon.objects.get(id=hackathon_id)
        except Hackathon.DoesNotExist:
            return Response({'error': 'Hackathon not found.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an enrollment for the user and hackathon
        enrollment, created = Enrollment.objects.get_or_create(user=user, hackathon=hackathon)

        if not created:
            return Response({'error': 'User already enrolled in the hackathon.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, user_id=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        enrollments = Enrollment.objects.filter(user=user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    


class UserSubmissionViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self, request, user_id=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        submissions = Submission.objects.filter(user=user)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
