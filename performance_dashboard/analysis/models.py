from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " +self.last_name

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('PART', 'Participation'),
        ('CHAL', 'Challenge'),
        ('LAB', 'Lab'),
        # Add more activity types as needed
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=4, choices=ACTIVITY_TYPES)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.student} - {self.activity} - {self.points}"

class TimeSpent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return f"{self.student} - {self.activity} - {self.duration}"
