from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор кастомного юзера"""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ['password',]
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]
