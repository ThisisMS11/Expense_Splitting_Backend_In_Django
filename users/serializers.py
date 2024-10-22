from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    mobile_number = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['name', 'password', 'email', 'mobile_number']

    def create(self, validated_data):
        user = User(
            username=validated_data['name'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    