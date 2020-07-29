from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    #
    path('register',views.register), # register
    path('login',views.login), # login 
    path('logout',views.destroy), # logout
    #
    path('dashboard',views.dashboard), # dashboard
    #
    path('add_job',views.add_job), # add a job
    path('add_job/add',views.process_job), # process the addition of job
    #
    path('view/<id>',views.view_job), # view a job
    #
    # add to my jobs path needed
    path('done/<id>',views.done),
    path('cancel/<id>',views.cancel),
    path('my_job/<id>',views.my_job), # my job now
    #
    path('edit/<id>',views.edit_job), # edit a job posting
    path('edit/<id>/update',views.process_edit)
]
