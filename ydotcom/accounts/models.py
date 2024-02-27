from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


# Create your models here.
class Interest(models.Model):
    name = models.CharField(max_length=48,
                            blank=False,
                            null=False
                            )

    def __str__(self):
        return self.name


class JobTitle (models.Model):
    title = models.CharField(max_length = 48,
                             blank=False,
                             null=False)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    first_name = models.CharField(max_length=48, blank=True, null=True)
    surname = models.CharField(max_length=48, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, default="")
    date_of_birth = models.DateTimeField(blank=True, null=True, default = timezone.make_aware(datetime(1900, 1, 1)))
    title = models.CharField(max_length=5, blank=True, null=True, default="")
    interests = models.ManyToManyField('Interest', blank=True)

    def __str__(self):
        return f"{self.user}: {self.title}. {self.first_name} {self.surname}'s Profile"
        


class EmploymentHistory(models.Model):
    user_profile = models.ForeignKey(UserProfile, 
                                     on_delete=models.CASCADE, 
                                     related_name='employment_history')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    organisation_name = models.CharField(max_length=140,
                                         blank=False,
                                         )
    position = models.ForeignKey(JobTitle,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True
                                )
    
    def __str__(self):
        return f"{self.position} @ {self.organisation_name} ({self.start_date} - {self.end_date})"
