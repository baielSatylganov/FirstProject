from django.db import models
from students.models import Student
from professors.models import Professors
from datetime import timedelta
import hashlib
import datetime

class Meetings(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_meetings")
    professor = models.ForeignKey(Professors, on_delete=models.CASCADE, related_name="professor_meetings")
    datetime = models.DateTimeField()
    jitsiLink = models.URLField(max_length=200)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined'),
    ]
    subject = models.CharField(max_length=50)
    day_of_week = models.CharField(max_length=50, null=True)
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default='PENDING',
    )
    time_delta = timedelta(hours=1)
    duration = models.DurationField(default=time_delta)
    
    def __str__(self):
        return f'Профессор({self.professor.firstName} {self.professor.surname}) - студент({self.student.firstname} {self.student.surname}) - {self.datetime}'
    
    def generate_hash(student_name, professor_name, date):
        # Соединим все входные данные в одну строку
        data = f'{student_name}{professor_name}{date}'
        # Создадим хеш из данной строки
        hash_object = hashlib.sha256(data.encode())
        # Вернем получившийся хеш в виде строки
        return hash_object.hexdigest()

def save(self, *args, **kwargs):
    date_obj = datetime.datetime.strptime(self.datetime, "%Y-%m-%dT%H:%M:%S").date()
    self.day_of_week = date_obj.strftime('%A')
    self.jitsiLink = "https://meet.jit.si/" + str(self.generate_hash({self.professor.surname},{self.student.surname},{self.datetime}))
    super(Meetings, self).save(*args, **kwargs)
