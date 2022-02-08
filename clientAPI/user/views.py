from rest_framework import generics
from user.serializers import RegisterUserSerializer
from user.models import User

class RegisterUserView(generics.CreateAPIView):
    """Register a new user."""
    serializer_class = RegisterUserSerializer

class UserListView(generics.ListAPIView):
    """List all users registered in the library."""
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    
