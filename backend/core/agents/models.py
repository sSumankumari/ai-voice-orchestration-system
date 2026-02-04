from django.db import models
from django.contrib.auth.models import User

class Agent(models.Model):
    """
    Persistent representation of an AI agent.
    """

    CATEGORY_CHOICES = [
        ("medical", "Medical"),
        ("nutrition", "Nutrition"),
        ("finance", "Finance"),
        ("legal", "Legal"),
        ("research", "Research"),
        ("interview", "Interview"),
        ("general", "General"),
    ]

    name = models.CharField(
        max_length=100,
        help_text="Human-readable name of the AI agent"
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        help_text="Domain category of the agent"
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
