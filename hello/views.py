from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Greeting
from .models import Submission
from CincyAI.titanic import Postmortem

# Create your views here.
def index(request):
    return HttpResponse('Hello CincyAI!')
# def index(request):
#     # return HttpResponse('Hello from Python!')
#     return render(request, "index.html")


def postmortem(request):
    postmortem = Postmortem()
    return render(request, "postmortem.html", {"postmortem": postmortem})


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})


def submissions(request):
    submission = Submission()
    submission.title = "Test Sub Title"
    submission.submitter = "Robert"
    submission.description = "Test description"
    submission.predictions = "{0,1,0,1}"
    submission.save()
    submissions = Submission.objects.all()
    return render(request, "submissions.html", {"submissions": submissions})
