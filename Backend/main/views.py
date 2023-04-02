from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer,LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegistrationView(generics.CreateAPIView):
    """
    API view to handle user registration.

    POST request with the following data in the request body:
    {
        "email": string,
        "full_name": string,
        "phone": int,
        "address": string,
        "city": string,
        "state": string,
        "country": string,
        "pincode": int,
        "password": string
    }

    Returns a JWT refresh and access token if the user is created successfully.
    """
    serializer_class = UserSerializer

    def post(self, request):
        """
        This function handles post request to the register api
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    """
    API view to handle user login.

    POST request with the following data in the request body:
    {
        "email": string,
        "password": string
    }

    Returns a JWT refresh and access token if the user is authenticated successfully.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        This function handles post request for login api
        """
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data['refresh']
        access_token = response.data['access']
        response.data = {
            'refresh': refresh_token,
            'access': access_token
        }
        return response