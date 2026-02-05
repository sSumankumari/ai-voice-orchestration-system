from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Agent
from .serializers import AgentSerializer

class AgentViewSet(ModelViewSet):
    """
    REST API for managing AI agents.
    """

    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
