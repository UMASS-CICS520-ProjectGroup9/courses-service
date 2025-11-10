from django.db import models

# Create your models here.
class Course(models.Model):
    courseID = models.AutoField(primary_key=True)
    courseSubject = models.CharField(max_length=100, default="")
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    credits = models.IntegerField()
    schedule = models.CharField(max_length=100)
    room = models.CharField(max_length=50)
    requirements = models.TextField()
    description = models.TextField()
    instruction_mode = models.CharField(max_length=50)


    def __repr__(self):
        return f"Course({self.courseID}, {self.title}, {self.credits}, {self.schedule}, {self.room}, {self.instructor}, {self.requirements}, {self.description}, {self.instruction_mode})"

    class Meta:
        # Default ordering when querying Course objects: first by subject, then by id
        ordering = ["courseSubject", "courseID"]