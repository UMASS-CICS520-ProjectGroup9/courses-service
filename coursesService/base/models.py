from django.db import models

# Create your models here.

class Course(models.Model):
    """
    Represents a university course with all relevant details.
    Fields:
        courseID (AutoField): Primary key for the course.
        courseSubject (CharField): Subject code (e.g., COMPSCI, BIOLOGY).
        title (CharField): Course title.
        instructor (CharField): Name of the instructor.
        credits (IntegerField): Number of credits for the course.
        schedule (CharField): Schedule information (e.g., MWF 10:00-10:50).
        room (CharField): Room location.
        requirements (TextField): Prerequisites or requirements.
        description (TextField): Course description.
        instruction_mode (CharField): Mode of instruction (e.g., In Person, Online).
    """
    courseID = models.IntegerField(primary_key=True)
    creator_id = models.IntegerField(null=True, blank=True) # user ID comes from token
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
        """Return a readable string representation of the course object."""
        return (f"Course({self.courseID}, {self.title}, {self.credits}, "
                f"{self.schedule}, {self.room}, {self.instructor}, "
                f"{self.requirements}, {self.description}, {self.instruction_mode})")

    class Meta:
        # Default ordering when querying Course objects: first by subject, then by id
        ordering = ["courseSubject", "courseID"]