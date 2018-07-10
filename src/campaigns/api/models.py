from django.db import models

# Create your models here.


class Campaign(models.Model):
    account = models.CharField(max_length=25)
    title = models.TextField()

    def __str__(self):
        return f"{self.id} - {self.account} - {self.title}"
