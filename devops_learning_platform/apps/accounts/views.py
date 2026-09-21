"""
Accounts Views.

WHAT IS A DRF VIEW?
--------------------
A view handles an HTTP request and returns an HTTP response.
DRF provides several base classes:

  APIView           → Manual, full control
  GenericAPIView    → Adds queryset, serializer_class, etc.
  Mixins            → ListMixin, CreateMixin, etc.
  ViewSets          → Combines multiple views into one class (CRUD)
  ModelViewSet      → Full CRUD automatically from a model

LEVEL 1 LEARNING: We start with simple generic views.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, UserPublicSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/v1/accounts/register/
    Create a new user account.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Auto-generate JWT tokens on registration
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Account created successfully!',
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/v1/accounts/profile/  → Get current user profile
    PUT  /api/v1/accounts/profile/  → Update current user profile
    PATCH /api/v1/accounts/profile/ → Partial update
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """POST /api/v1/accounts/change-password/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': 'Password changed successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPublicProfileView(generics.RetrieveAPIView):
    """
    GET /api/v1/accounts/users/{username}/
    View another user's public profile.
    """
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """
    GET /api/v1/accounts/dashboard-stats/
    Returns a summary of the user's learning activity.
    """
    from apps.progress.models import UserProgress
    from apps.courses.models import Course

    user = request.user
    completed = UserProgress.objects.filter(user=user, completed=True).count()
    in_progress = UserProgress.objects.filter(user=user, completed=False).count()

    return Response({
        'username': user.username,
        'skill_level': user.skill_level,
        'total_points': user.total_points,
        'completed_items': completed,
        'in_progress_items': in_progress,
        'is_premium': user.is_premium,
    })
