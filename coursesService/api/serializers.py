from rest_framework import serializers
from base.models import Course

#courses-service/coursesService/api/serializers.py
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'