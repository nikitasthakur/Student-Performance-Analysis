from django.contrib import admin
from .models import Student, Topic, Activity, Score, TimeSpent  # Replace with your actual models

admin.site.register(Student)
admin.site.register(Topic)
admin.site.register(Activity)
admin.site.register(Score)
admin.site.register(TimeSpent)
