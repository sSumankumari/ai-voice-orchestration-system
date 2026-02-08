from django.db import models
from django.contrib.auth.models import User

class Agent(models.Model):
    """
    Persistent representation of an AI agent.
    """

    name = models.CharField(
        max_length=100,
        help_text="Human-readable name of the AI agent"
    )

    category = models.CharField(
        max_length=50,  # Increased from 20 to allow longer categories
        help_text="Domain category of the agent (open-ended)",
        db_index=True  # Add index for faster queries
    )

    system_prompt = models.TextField(
        help_text="System prompt defining agent behavior"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="agents",
        help_text="User who created this agent"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} ({self.category})"
