from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer,LoginSerializer,ContentSerializer,ContentViewSerializer,CategorySerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view,permission_classes
from django.db.models import Q
from .models import Content,Category
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

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
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def content_detail_view(request, pk):
    """
    API view to get a content detail by primary key.
    """
    try:
        if request.user.is_staff:
            content = get_object_or_404(Content, pk=pk)
        else :
            content = get_object_or_404(Content, pk=pk,author=request.user)
        serializer = ContentSerializer(content,context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def content_create_view(request):
    """
    API view to create a new content. Required fields:
    - title (string)
    - body (string)
    - summary (string)
    - pdf_file (pdf)
    - categories (list of category ids)
    """
    try:
        serializer = ContentViewSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response('Object created successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def content_update_view(request, pk):
    """
    API view to update an existing content.
    """
    try:
        if request.user.is_staff:
            content = get_object_or_404(Content, pk=pk)
        else:
            content = get_object_or_404(Content, pk=pk,author=request.user)
        serializer = ContentViewSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def content_delete_view(request, pk):
    """
    API view to delete an existing content.
    """
    try:
        if request.user.is_staff:
            content = get_object_or_404(Content, pk=pk)
        else:
            content = get_object_or_404(Content, pk=pk,author=request.user)
        content.delete()
        return Response('Content deleted successfully',status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list_view(request):
    """
    API view to get a list of all categories.
    """
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_detail_view(request, pk):
    """
    API view to get a category detail by primary key.
    """
    try:
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def category_create_view(request):
    """
    API view to create a new cattegory. Required fields:
    - name (string)
    """
    try:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Object created successfully', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def category_delete_view(request, pk):
    """
    API view to delete an existing category.
    """
    try:
        content = get_object_or_404(Category, pk=pk)
        content.delete()
        return Response('Category deleted successfully',status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)