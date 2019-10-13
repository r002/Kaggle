from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import titanic.views
import titanic.controllers.home_controller
import titanic.controllers.postmortem_controller

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", titanic.controllers.home_controller.index, name="index"),
    path("postmortem/<int:id>", titanic.controllers.postmortem_controller.postmortem, name="postmortem"),
    path("submissions/", titanic.views.submissions, name="submissions"),
    path("db/", titanic.views.db, name="db"),
    path("admin/", admin.site.urls),
    path('upload_csv/', titanic.views.upload_csv, name='upload_csv'),
]
