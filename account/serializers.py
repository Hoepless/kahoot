from rest_framework import serializers

from .utils import send_activation_code
from .models import User

from django.contrib.auth.models import Group
from django.db.models import Count
from collections import Counter


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, required=True)
    password_confirmation = serializers.CharField(min_length=4, required=True)

    class Meta:
        model = User
        fields = (
            'email', 'password',
            'password_confirmation',
            'first_name', 'last_name', 'phone',
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError(
                "Password doesn't match"
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user


class UserSerializer(serializers.ModelSerializer):
    tests_passed = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'group', 'phone',
                  'email', 'final_score', 'rating_place', 'group_rating_place',
                  'tests_passed')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # User.set_group_rating_place(instance)
        # User.set_rating_place()
        return representation


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('name', )
