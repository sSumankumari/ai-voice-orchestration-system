from rest_framework import serializers
from .models import Agent

class AgentSerializer(serializers.ModelSerializer):
    """
    Converts Agent model instances to JSON and vice versa.
    """

    class Meta:
        model = Agent
        fields = [
            "id",
            "name",
            "category",
            "system_prompt",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]
