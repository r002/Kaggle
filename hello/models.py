from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Submission(models.Model):
    title = models.CharField(max_length=200)
    submitter = models.CharField(max_length=200)
    description = models.TextField()
    predictions = models.TextField()
    published = models.DateTimeField('date submitted', auto_now_add=True)

    def __str__(self):
        return f"{self.submitter} | {self.title}"
