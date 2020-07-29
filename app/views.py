from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import User, Job
from django.db.models import Q
import bcrypt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request,'index.html')

"""
LOGIN AND REGISTRATION:

"""

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/') # if something doesn't pass validations, redirect to index
        #messages.error(request,'something went wrong')
    else:
        email = request.POST.get('email')
        try: # checking if email already exists
            User.objects.get(email=email)
            messages.error(request, "another user already has this email")
            return redirect('/')
        except:
            firstName = request.POST.get('first_name')
            lastName = request.POST.get('last_name')
            #email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_pw')
            pw_hash = bcrypt.hashpw(password.encode() , bcrypt.gensalt() ).decode() # creates the hash
            # defining the name
            user = User.objects.create(first_name = firstName, last_name = lastName, email = email, password = pw_hash)
            # request session userID
            request.session['userID'] = user.id
            messages.success(request,'registration successful')
            return redirect('/dashboard')

def login(request):
        # checking email
    email = request.POST.get('email')
    try: 
        user = User.objects.get(email = email) 
        if bcrypt.checkpw( request.POST['password'].encode(), user.password.encode() ):
            request.session['userID'] = user.id 
            messages.success(request,"successfully logged in ( or registered )")
            return redirect('/dashboard')
        else:
            messages.error(request, "wrong password???")
            return redirect('/')
        # if that doesn't work , do the following:
    except:
        messages.error(request, "email address not found...")
        return redirect('/')

def destroy(request):
    if 'userID' not in request.session:
        messages.error(request,'nice try')
        return redirect('/')
    else:
        del request.session['userID']
        request.session.clear()
        return redirect('/')

"""
EVERYTHING ELSE:

note:

if 'userID' not in request.session:
        messages.error(request,'nice try')
        return redirect('/')

"""

def dashboard(request):
    if 'userID' not in request.session:
        messages.error(request,'nice try')
        return redirect('/')
    else:
        context = {
            'myjob' : Job.objects.filter(my_job = True),
            'user' : User.objects.get(id = request.session['userID']),
            'alljobs' : Job.objects.all(),
            'allusers' : User.objects.all(),
            'poster_jobs' : Job.objects.filter(poster = request.session['userID']) 
        }
        return render(request,'dashboard.html',context)

# add a job
def add_job(request):
    if 'userID' not in request.session:
        messages.error(request, 'nice try')
        return redirect ('/')
    else:
        context = {
            'user' : User.objects.get(id = request.session['userID']),
            'allusers' : User.objects.all(),
            'alljobs' : Job.objects.all()
        }
    return render(request,'addJob.html',context)

def process_job(request):
    if 'userID' not in request.session:
        messages.error(request, 'nice try')
        return redirect ('/')
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect ('/add_job')
    else:
        new_title = request.POST.get('title')
        new_desc = request.POST.get('description')
        new_location = request.POST.get('location')
        Job.objects.create(title = new_title, desc = new_desc, location = new_location, poster = User.objects.get(id = request.session['userID']))
        # message
        messages.success(request, 'job succesfully added')
        return redirect('/dashboard')
#

def view_job(request,id):
    if 'userID' not in request.session:
        messages.error(request, 'nice try')
        return redirect('/')
    else:
        context = {
            'poster_jobs' : Job.objects.filter(poster = request.session['userID']) ,
            'myjob' : Job.objects.filter(my_job = True),
            'myjoblist' : Job.objects.exclude(my_job = True),
            'user' : User.objects.get(id = request.session['userID']),
            'allusers' : User.objects.all(),
            'alljobs' : Job.objects.all(),
            'thejob' : Job.objects.get(id = id)       
        }
    return render(request,'view.html',context)

# edit a job
def edit_job(request,id):
    if 'userID' not in request.session:
        messages.error(request,'nice try')
        return redirect('/')
    else:
        context = {
            'thejob' : Job.objects.get(id = id),
            'user' : User.objects.get(id = request.session['userID']),
            'allusers' : User.objects.all(),
            'alljobs' : Job.objects.all()
        }
    return render(request,'edit.html',context)

def process_edit(request,id):
    if 'userID' not in request.session:
        messages.error(request,'nice try')
        return redirect('/')
    errors = Job.objects.edit_job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f'/edit/{id}')
    else:
        update = Job.objects.get(id = id)
        update.title = request.POST.get('edit_title')
        update.desc = request.POST.get('edit_description')
        update.location = request.POST.get('edit_location')
        update.save()
        messages.success(request, 'job was successfully updated')
        return redirect('/dashboard')
#

def my_job(request,id):
    if 'userID' not in request.session:
        messages.error(request,'nice try')
        return redirect('/')
    alljobs = Job.objects.all()
    job = Job.objects.get(id=id)
    if not job.my_job:
        job.my_job = True # mark that it is my job now
        job.save()
    myjob = Job.objects.filter(my_job = True)
    return redirect('/dashboard')

def done(request,id):
    if 'userID' not in request.session:
        messages.error(request,'nice try')
    else:
        remove = Job.objects.get(id = id)
        remove.delete()
        return redirect('/dashboard')

def cancel(request,id):
    if 'userID' not in request.session:
        messages.error(request,'nice try')
    else:
        cancel_job = Job.objects.get(id = id)
        cancel_job.delete()
        return redirect('/dashboard')
