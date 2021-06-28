from enum import auto
from re import sub
from django.shortcuts import render,redirect
from . models import *
#from .forms import StudentRegistration
from MCQ_Test.models import *
from django.contrib import messages
from django.views import View
from django.http import HttpResponse
# Create your views here.

def student_login(request):
    if request.POST:
        global suser
        username=request.POST['username']
        upass=request.POST['upass']

        count = Student.objects.filter(username=username,password=upass).count()
        if count >0:
            suser=Student.objects.get(username=username)
            return redirect('studentdash')
        else:
            messages.warning(request,'Username Or Password not correct ')

    return render(request,'Student/studentlog.html')

def student_signup(request):
    if request.POST:
        username=request.POST['username']          
        uname=request.POST['uname']
        uemail=request.POST['uemail']
        umobile=request.POST['umobile']
        upass=request.POST['upass']
        if Student.objects.filter(username=username).exists():
            messages.warning(request,'Username is already exists')
        else :
            obj=Student(username=username,name=uname,email=uemail,mobile=umobile,password=upass)
            obj.save()
            messages.success(request,'User has been created Successfully')
    return render(request,'Student/studentsignup.html')


def student_dash(request):
    sub= Subject.objects.all()
    return render(request,'Student/studentdash.html',{'sub':sub})

def student_result(request):
    re=Result.objects.filter(student=suser)
    return render(request,'Student/studentresult.html',{'res':re})

def student_profile(request):
    p=suser
    return render(request,'Student/studentprofile.html',{'pr':p})


def exam_instruction(request,id):
    sub=Subject.objects.get(id=id)
    qdata=Question.objects.filter(subject=sub)
    fz=len(qdata)
    count=0
    for i in qdata:
        count+=i.marks

    if count==0:
            messages.warning(request,'This subject have No Any Question')
            return redirect('noquestion')
    else:
            return render(request,'Student/examinstruction.html',{'ftt':sub,'ft':fz,'co':count})


    

def exam_take(request,subject):
    global sub_id
    sub_id=Subject.objects.get(subject=subject)
    fm=Question.objects.filter(subject=sub_id)
    return render(request,'Student/examtake.html',{'ftt':fm})

def exam_result(request):
    if request.POST:
        ca=request.POST['cans']
        wa=request.POST['wans']
        sco=request.POST['score']
        Result.objects.create(student=suser,subject=sub_id,marks=sco)
    return render(request,'Student/examresult.html',{'cas':ca,'was':wa,'sc':sco})



def noquestion(request):
    return render(request,'Student/noquestion.html')
        
