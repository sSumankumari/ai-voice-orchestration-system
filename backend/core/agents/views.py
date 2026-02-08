from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Agent
from .serializers import AgentSerializer


# ✅ Registration endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user.
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Validation
    if not username or not email or not password:
        return Response(
            {"detail": "Username, email, and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {"detail": "Username already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if email already exists
    if User.objects.filter(email=email).exists():
        return Response(
            {"detail": "Email already registered."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate password strength
    try:
        validate_password(password)
    except ValidationError as e:
        return Response(
            {"detail": list(e.messages)},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create user
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response(
            {
                "detail": "User created successfully.",
                "username": user.username,
                "email": user.email
            },
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {"detail": f"Error creating user: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class AgentViewSet(ModelViewSet):
    """
    REST API for managing AI agents.
    - Read access: public (for FastAPI streaming service)
    - Write access: authenticated users only
    """

    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user as creator.
        """
        serializer.save(created_by=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Safe override to return clean JSON error
        instead of Django HTML error.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            return Response(
                {"detail": "Agent not found."},
                status=status.HTTP_404_NOT_FOUND
            )