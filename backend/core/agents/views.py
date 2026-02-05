from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import Agent
from .serializers import AgentSerializer

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
