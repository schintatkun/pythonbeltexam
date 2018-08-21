from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import User, Job
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'log_in/index.html')

def register(request):
    response = User.objects.basic_validator(request.POST)
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = response['user_id']
        return redirect('/userdashboard')
def login(request):
    response = User.objects.login_validator(request.POST)
    if response['user_status'] == False:
        if 'errors' in response:
            for error in response['errors']:
                messages.error(request, error)
            return redirect('/')
    else: 
        request.session['user_id'] = response['user_id']
        return redirect('/userdashboard')
def createjob(request):
    response = Job.objects.job_validator(request.POST, request.session['user_id'])
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/addjob')
    else:
        return redirect('/userdashboard')

def userdashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'job_list': Job.objects.all()
        }

    # a = User.objects.filter(id = request.session['user_id']).

    return render (request, 'log_in/dashboard.html', context)
def addjob(request):
    return render(request, 'log_in/addjob.html')

def view(request,id):
    show_job= Job.objects.get(id=id)
    return render(request,'log_in/view.html',{'job': show_job})
def getjob(request):

    return redirect('/userdashboard') 
def cancel(request,id):
    del_job = Job.objects.get(id=id)   
    del_job.delete()
    return redirect ('/userdashboard')
def edit(request,id):
    edit_job = Job.objects.get(id=id)
    context = {
        'job': edit_job
    }
    return render(request, 'log_in/edit.html', context)
def editjob(request,id):
    response = Job.objects.editjob_validator(request.POST)
    # if response['user_status'] == False:
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request, error)
        print('i am in errors')
        return redirect('/edit/'+id)
    else: 
        edit_job = Job.objects.get(id=id)
        edit_job.title= request.POST['title']
        edit_job.desc= request.POST['desc']        
        edit_job.location = request.POST['location']
        edit_job.save()
    return redirect('/userdashboard')
def addtomyjob(request,id):
    user= User.objects.get(id=request.session['user_id'])
    job = Job.objects.get(id=id)
    job.taken_by = user
    job.save()
    print('------- ',job)
    return redirect('/userdashboard')
def logout(request):
    request.session.clear()
    return redirect('/')