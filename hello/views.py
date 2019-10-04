from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import requests
import re
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
    # submission = Submission()
    # submission.title = "Test Sub Title"
    # submission.submitter = "Robert"
    # submission.description = "Test description"
    # submission.predictions = "{0,1,0,1}"
    # submission.save()
    submissions = Submission.objects.all()
    return render(request, "submissions.html", {"submissions": submissions})


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "upload_csv.html", data)

    # # if not GET, then proceed
    try:
        print("Attempt upload!")
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return redirect("/upload_csv?e=wrong_format")

        file_data = csv_file.read().decode("utf-8")

        # Remove header and all whitespace formatting
        file_data = file_data.replace("PassengerId,Survived", "")
        file_data = re.sub(r"\s+", ';', file_data)

        # Check if beginning and end are semicolons. If so, remove.
        if ";"==file_data[0]:
            file_data = file_data[1:]
        if ";"==file_data[-1]:
            file_data = file_data[:-1]

        submission = Submission()
        submission.title = "Test Sub Title"
        submission.submitter = "Robert"
        submission.description = "Test description"
        submission.predictions = file_data
        submission.save()
        return redirect("/submissions")

    except Exception as e:
        print(f"Failed upload! {e}")


    # try:
    #     csv_file = request.FILES["csv_file"]
    #     if not csv_file.name.endswith('.csv'):
    #         messages.error(request,'File is not CSV type')
    #         return HttpResponseRedirect(reverse("hello:upload_csv"))
    #     #if file is too large, return
    #     if csv_file.multiple_chunks():
    #         messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
    #         return HttpResponseRedirect(reverse("hello:upload_csv"))
    #
    # 	file_data = csv_file.read().decode("utf-8")
    #
    # 	lines = file_data.split("\n")
    #
	# 	#loop over the lines and save them in db. If error , store as string and then display
    #     for line in lines:
    #         fields = line.split(",")
    #         data_dict = {}
    #         data_dict["name"] = fields[0]
    #         data_dict["start_date_time"] = fields[1]
    #         data_dict["end_date_time"] = fields[2]
    #         data_dict["notes"] = fields[3]
    #         try:
    #             form = EventsForm(data_dict)
    #             if form.is_valid():
    #                 print("******* SUCCESS!!!!")
    #                 print(data_dict)
    #                 # form.save()
    #             else:
    #                 print(form.errors.as_json())
    #                 # logging.getLogger("error_logger").error(form.errors.as_json())
    #         except Exception as e:
    #             print(repr(e))
    #             pass
    #             # logging.getLogger("error_logger").error(repr(e))
    #
    # except Exception as e:
    #     print("Unable to upload file. "+repr(e))
    # 	# logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
    # 	# messages.error(request,"Unable to upload file. "+repr(e))

    return redirect("/upload_csv?e=failed_upload")

    # return HttpResponseRedirect(reverse("hello:upload_csv"))
