import os
import csv
from django.core.management.base import BaseCommand
from analysis.models import Student, Topic, Activity, Score, TimeSpent

class Command(BaseCommand):
    help = 'Import data from CSV files in the given directory into the database.'

    def add_arguments(self, parser):
        parser.add_argument('csv_dir', type=str, help='The directory containing the CSV files.')

    def handle(self, *args, **kwargs):
        csv_dir = kwargs['csv_dir']
        for filename in os.listdir(csv_dir):
            if filename.endswith('.csv'):
                self.import_csv(os.path.join(csv_dir, filename))

    def import_csv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            topic_name = os.path.splitext(os.path.basename(file_path))[0]
            topic, _ = Topic.objects.get_or_create(name=topic_name)
            cnt = 0
            for row in reader:
                # student_id = row['Student ID']
                fname = row['First name']
                lname = row['Last name']
                student, _ = Student.objects.get_or_create(first_name=fname,last_name=lname)
                cnt += 1
                for key, value in row.items():
                    # Skip the student identifier columns
                    if key in ['Student ID','First name','Last name']:
                        continue
                    if 'total' in key:
                        continue
                    # Determine the type of activity from the column name
                    if ('Participation' in key or 'Challenge' in key or 'Lab' in key) and 'time (min)' not in key:
                                    activity_type = 'PART' if 'Participation' in key else 'CHAL' if 'Challenge' in key else 'LAB'
                                    activity_name = key.split(' (')[0]  # Assuming activity name is before the first '('
                                    score = value
                                    # time_spent = row.get(f"{activity_name} time (min)", None)
                                    
                                    if score:
                                        self.create_or_update_score(student, topic, activity_name, activity_type, score)
                                    # if time_spent:
                                    #     self.create_or_update_time_spent(student, topic, activity_name, activity_type, time_spent)

                    if ('Participation' in key or 'Challenge' in key or 'Lab' in key) and 'time (min)' in key:
                                    activity_type = 'PART' if 'Participation' in key else 'CHAL' if 'Challenge' in key else 'LAB'
                                    activity_name = key.split(' time (')[0]  # Assuming activity name is before the first '('
                                    # score = value
                                    time_spent = value
                                    
                                    # if score:
                                    #     self.create_or_update_score(student, topic, activity_name, activity_type, score)
                                    if time_spent:
                                        self.create_or_update_time_spent(student, topic, activity_name, activity_type, time_spent)

                self.stdout.write(self.style.SUCCESS(f"Data imported for row {cnt} "))

    def create_or_update_score(self, student, topic, activity_name, activity_type, score):
        if score:
            activity, _ = Activity.objects.get_or_create(
                name=activity_name,
                type=activity_type,
                topic=topic
            )
            Score.objects.update_or_create(
                student=student,
                activity=activity,
                defaults={'points': float(score)}
            )

    def create_or_update_time_spent(self, student, topic, activity_name, activity_type, time_spent):
        if time_spent:
            activity, _ = Activity.objects.get_or_create(
                name=activity_name,
                type=activity_type,
                topic=topic
            )
            TimeSpent.objects.update_or_create(
                student=student,
                activity=activity,
                defaults={'duration': float(time_spent)}
            )
