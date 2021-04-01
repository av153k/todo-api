from django.db import models
from todo_api.models import TimeStampsModel
# Create your models here.


class Profile(TimeStampsModel):
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE)
    phone = models.TextField(max_length=11, blank=True)
    profile_picture = models.URLField(
        default='https://static.productionready.io/images/smiley-cyrus.jpg')

    def __str__(self):
        return self.user.username
