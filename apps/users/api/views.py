# thirdparty imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

# local imports
from apps.users.api.serializers import UserLoginSerializer, UserSerializer, UserSignupSerializer
from apps.users.models import User


class UserAuthViewSet(ViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny,]
    
    def get_serializer_class(self):
        if self.action == 'signup':
            return UserSignupSerializer
        return UserLoginSerializer
        
    @action(detail=False, methods=["post"], url_path="signup")
    def signup(self, request):
        """User signup"""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "User created successfully",
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        """User login"""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserDetailViewset(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user
