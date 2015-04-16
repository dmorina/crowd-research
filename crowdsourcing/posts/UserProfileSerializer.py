from rest_framework import serializers

from crowdsourcing.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile

        fields = ('id', 'author', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

        fields = ('id', 'email', 'username',
                  'first_name', 'last_name','password')
        read_only_fields = ('id')

        def create(self, validated_data):
            return UserProfile.objects.create(**validated_data)