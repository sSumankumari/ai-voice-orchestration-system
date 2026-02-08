from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, register_user  # ✅ Import both

router = DefaultRouter()
router.register(r"agents", AgentViewSet, basename="agent")

urlpatterns = [
    path('register/', register_user, name='register'),  # ✅ Add registration here
] + router.urls