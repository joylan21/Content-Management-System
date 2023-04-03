from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User,Content,Category
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom user model.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    def validate_password(self, value):
        """
        This fucntion validates password for Min 8 length, 1 uppercase, 1 lowercase condition
        """
        validate_password(value)
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        return value
    
    def validate_phone(self,value):
        """
        This function validates phone number for numeric condition
        """
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError("Phone number must be numeric only")
        return value
    
    def validate_pincode(self,value):
        """
        This function validates pincode for numeric condition
        """
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError("Pincode must be numeric only")
        return value


    class Meta:
        model = User
        fields = (
            'email', 'full_name', 'phone', 'address', 'city', 'state',
            'country', 'pincode', 'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    class Meta:
        fields = ('email', 'password')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ContentSerializer(serializers.ModelSerializer):
    categories =CategorySerializer(many=True)
    pdf_file = serializers.FileField()

    class Meta:
        model = Content
        fields = ['id', 'title', 'body', 'summary', 'pdf_file', 'categories']

    def get_pdf_file(self,obj):
        if obj.pdf_file:
            return self.context.get('request').build_absolute_uri(obj.pdf_file.url)
        else:
            return None
        
class ContentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'body', 'summary', 'pdf_file', 'categories']
    
    def create(self, validated_data):
        if 'categories' in validated_data.keys():
            categories_data = validated_data.pop('categories')
        else:
            categories_data=[]
        document = Content.objects.create(**validated_data)
        for category_obj in categories_data:
            category = Category.objects.get(id=category_obj.id)
            document.categories.add(category)
        return document
    
    def update(self, instance, validated_data):
        if 'categories' in validated_data.keys():
            categories_data = validated_data.pop('categories')
        else:
            categories_data=[]
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.pdf_file = validated_data.get('pdf_file', instance.pdf_file)
        if categories_data:
            instance.categories.clear()
            for category_data in categories_data:
                category = Category.objects.get(id=category_data.id)
                instance.categories.add(category)
            instance.save()
        return instance