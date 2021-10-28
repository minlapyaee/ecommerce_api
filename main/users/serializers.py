from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'role', 'item_code']
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def create(self, validated_data):
        # extract password
        # django automatic do for hash password
        password = validated_data.pop('password', None)
        # not extract password
        instance = self.Meta.model(**validated_data)
        if password is not None:
            # if not password replace hash password ti not extract password
            instance.set_password(password)
            instance.save()
            return instance
