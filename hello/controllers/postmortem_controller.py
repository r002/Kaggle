from django.shortcuts import render
from django.http import HttpResponse
from hello.models import Submission
from CincyAI.titanic import Postmortem

def postmortem(request, id):
    # Get the submission from the database
    s = Submission.objects.get(id=id)

    postmortem = Postmortem()
    postmortem.id = s.id
    postmortem.title = s.title
    postmortem.description = s.description
    postmortem.predictions = s.predictions
    postmortem.submitter = s.submitter
    postmortem.published = s.published

    return render(request, "postmortem.html", {"p": postmortem})
