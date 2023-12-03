from django.shortcuts import render
from rest_framework import viewsets
from .models import Score, Student, Activity, Topic, TimeSpent
from .serializers import StudentSerializer, ScoreSerializer, TimeSpentSerializer, TopicSerializer, ActivitySerializer
import statistics
from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class TimeSpentViewSet(viewsets.ModelViewSet):
    queryset = TimeSpent.objects.all()
    serializer_class = TimeSpentSerializer

@api_view(['GET'])
def score_distribution(request):
    # Prepare a dictionary to hold the results
    topic_score_distribution = {}

    # Iterate through each topic
    for topic in Topic.objects.all():
        # Retrieve scores for this topic as a list
        scores_list = list(Score.objects.filter(activity__topic=topic).values_list('points', flat=True))

        if scores_list:
            # Calculate median and quartiles using the statistics module
            median = statistics.median(scores_list)
            q1 = statistics.quantiles(scores_list, n=4)[0]  # First quartile
            q3 = statistics.quantiles(scores_list, n=4)[2]  # Third quartile
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # Identifying outliers
            # outliers = [score for score in scores_list if score < lower_bound or score > upper_bound]

            # Add the results to the dictionary
            topic_score_distribution[topic.name] = {
                'median': median,
                'q1': q1,
                'q3': q3,
                'iqr': iqr,
                'min': lower_bound,
                'max': upper_bound,
                'scores': scores_list
            }
        else:
            # Handle the case where no scores are present
            topic_score_distribution[topic.name] = 'No scores available'

    return Response(topic_score_distribution)

@api_view(['GET'])
def topic_wise_totalscores(request, name):
    # Get all students
    students = Student.objects.all()
    topic = get_object_or_404(Topic, name=name)
    res = {}

    # Prepare a dictionary to hold the results
    total_scores_by_topic = []

    # Iterate through each student
    for student in students:
        scores = Score.objects.filter(student=student, activity__topic=topic)
        total_score_for_topic = sum(score.points for score in scores)/len(scores)
        total_scores_by_topic.append(total_score_for_topic)

    res = {
        topic.name : total_scores_by_topic,
    }

    return Response(res)

@api_view(['GET'])
def avg_timespent_per_topic(request):
    avg_timespents = {}
    for topic in Topic.objects.all():
        time_spents = list(TimeSpent.objects.filter(activity__topic=topic).values_list('duration', flat=True))

        if time_spents:
            avg = statistics.mean(time_spents)
            avg_timespents[topic.name] = avg
        else:
            # Handle the case where no scores are present
            avg_timespents[topic.name] = 'No timespent available'

    return Response(avg_timespents)