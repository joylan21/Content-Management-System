from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

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
