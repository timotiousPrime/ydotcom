from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,
                             on_delete= models.CASCADE,
                             related_name= "posts",
                             blank= False,
                             null= False,
                             )
    timestamp= models.DateTimeField(auto_now_add=True,
                                    blank=False,
                                    null= False,
                                    )
    message= models.TextField(max_length= 140,
                              default="",
                              blank=False,
                              null= False,
                              )
    
    def __str__(self):
        return f"{self.user} @ {self.timestamp}: {self.message}"