from rest_framework import serializers
from .models import UserProfile, Interest, EmploymentHistory, JobTitle

class EmploymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentHistory
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    employment_history = EmploymentHistorySerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'title', 'first_name', 'surname', 'date_of_birth', 'phone_number', 'employment_history']

    def create(self, validated_data):
        employment_data = validated_data.pop('employment')
        user_profile = UserProfile.objects.create(**validated_data)
        for employment in employment_data:
            EmploymentHistory.objects.create(user_profile=user_profile, **employment)
        return user_profile

class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = '__all__'


class JobTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobTitle
        fields = '__all__'
