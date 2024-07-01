from django.db import models
from userauths.models import UserAccount


class UserReview(models.Model):
    user = models.ForeignKey(
        UserAccount, 
        on_delete=models.SET_NULL, 
        null=True
    )

    movieId = models.CharField(max_length=6)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=20, default=0)

    def __str__(self):
        return str(self.user.first_name)
