from rest_framework import serializers
from base.models import Course

#courses-service/coursesService/api/serializers.py
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {'creator_id': {'read_only': True}}