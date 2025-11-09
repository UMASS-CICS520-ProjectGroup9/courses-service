from django.db import models

# Create your models here.
class Course(models.Model):
    courseID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    credits = models.IntegerField()
    schedule = models.CharField(max_length=100)
    room = models.CharField(max_length=50)
    instructor = models.CharField(max_length=100)
    requirements = models.TextField()
    description = models.TextField()
    instruction_mode = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __repr__(self):
        return f"Course({self.courseID}, {self.title}, {self.instructor})"