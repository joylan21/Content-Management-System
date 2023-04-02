from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer,LoginSerializer,ContentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view,permission_classes
from django.db.models import Q
from .models import Content,Category
from rest_framework.permissions import IsAuthenticated

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def content_list_view(request):
    """
    API view to get a list of contents that match a search query (if provided) or all contents.
    
    To search, send the query parameter 'query' with your search terms in the format:
    /api/contents/?query=search+terms
    """
    try:
        query = request.GET.get('query')
        if query:
            # Filter contents based on search query using OR condition on title, body, summary, and category name fields
            contents = Content.objects.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(summary__icontains=query) | Q(categories__name__icontains=query)).distinct()
        else:
            contents = Content.objects.all()
        #check if user is admin or not
        if not request.user.is_staff:
            contents = contents.filter(author=request.user)
        serializer = ContentSerializer(contents, many=True,context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)