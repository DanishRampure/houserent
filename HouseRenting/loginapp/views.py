from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
import re
import smtplib
from email.message import EmailMessage
import random
import string
from loginapp.models import user
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as signout
from django.contrib.auth.models import User
fn = ''
ln = ''
ph = ''
em = ''
pwd = ''
cpwd = ''
utype = ''
xn = ''
d = {}
a=0
# Create your views here.

def home(request):
    return render(request, 'welcome.html')

def about(request):
    return render(request,'about.html')

def send(request):
    msg=EmailMessage()
    msg['Subject']="Email Verification"
    msg['From']="House Rentals"
    msg['To']=em
    print(em)
    ran=''.join(random.choices(string.digits, k=6))
    matt="Hi "+fn+" ,Below is the Confirmation Code to confirm your email address\n"+ran
    msg.set_content(matt)
    mys=smtplib.SMTP(settings.EMAIL_HOST,587)
    mys.starttls()
    mys.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
    mys.send_message(msg)
    mys.quit()
    return ran
def verify(request):
    global xn,d,a
    hars=False
    if request.method=="POST":
        v=request.POST
        if (v['ver'] == xn):
            a+=1
            ins=user(first_name=fn,last_name=ln,email=em,phonenumber=ph,password=pwd,role=utype)
            ins.save()
            uses=User.objects.create_user(username=em.replace('@','1').replace('.','2'),password=pwd,email=em,first_name=fn)
            uses.save()
            print(ins.email)
            messages.success(request,"Your account is successfully Created")
            return redirect('login/')
        else:
            if v['press']=="resend":
                xn=send(request)
            else:
                hars=True
    return render(request,'verify.html',{'hars':hars})

def forgotconfirm(request):
    print("forgotconfirm")
    global xn, em
    if request.method == 'POST':
        print("forgotconfirm post")
        em = request.POST['email']
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not re.search(regex,em):
            return render(request,'forgot_confirm.html',{'error':True,'errormsg':"Invalid Email Address"})
        eerr=False
        try:
            print("forgotconfirm try")

            sd=user.objects.get(email=em)
            xn = ''+send(request)+''
            return redirect('verify1')
        except:
            print("forgotconfirm except")
            return render(request,'forgot_confirm.html',{'error':True, 'error_msg':"Account doesn't exist with this email" })
        
    return render(request, 'forgot_confirm.html')

def verify1(request):
    global xn, d
    hars = False
    if request.method == "POST":
        v = request.POST
        if (v['ver'] == xn):
            return redirect('forgot')
        else:
            hars = True
            if v['press'] == "resend":
                xn = send(request)
    return render(request, 'verify.html', {'hars': hars})


def forgot(request):
    global xn, d
    hars = False
    if request.method == "POST":
        v = request.POST
        passreg = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        pwd = request.POST["password"]
        cpwd = request.POST["cpassword"]
        Errors = []
        errormsg = ''
        errorflag = False
        dict = {}
        if not re.search(passreg, pwd):
            errorflag = True
            errormsg = "Password must contain Minimum eight characters, at least one letter, one number and one special character"
            Errors.append(errormsg)
        if pwd != cpwd:
            errorflag = True
            errormsg = "Passwords doesn't match"
            Errors.append(errormsg)
        if errorflag:
            dict["error"] = errorflag
            dict["errors"] = Errors
            return render(request, 'forgot.html', context=dict)
        print(pwd, em)
        if not errorflag:
            pro=user.objects.get(email=em)
            pro.password=pwd
            pro.save() 
            us=User.objects.get(email=em)
            us.set_password(pwd)
            us.save()
            print(us.password)           
            messages.success(request, "Password reset successful")
            return redirect('login')
    return render(request,'forgot.html')

def signup(request):
    global fn,ln,ph,em,pwd,utype,cpwd,xn,d
    if request.method=="POST":
        d=request.POST
        for key,value in d.items():
            if key=="first_name":
                fn=value
            if key=="last_name":
                ln=value
            if key=="email":
                em=value
            if key=="phonenumber":
                ph=value
            if key=="password":
                pwd=value
            if key=="cpassword":
                cpwd=value
            if key=="type":
                utype=value

        values={}
        values['fname']=fn
        values['lname']=ln
        values['email']=em
        values['phn']=ph
        Errors=[]
        errorflag=False
        dict={}
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        passreg="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if not (fn.isalpha() or ln.isalpha()):
            errorflag=True
            errormsg="Name should contain only alphabets"
            Errors.append(errormsg)
        if not re.search(regex,em):
            errorflag=True
            errormsg="Email address is not Valid"
            Errors.append(errormsg)
        if len(str(ph))!=10 or (not ph.isdigit()):
            errorflag=True
            errormsg="Mobile number must be 10 digits"
            Errors.append(errormsg)
        if not re.search(passreg,pwd):
            errorflag=True
            errormsg="Password must contain Minimum eight characters, at least one letter, one number and one special character"
            Errors.append(errormsg)
        if pwd!=cpwd:
            errorflag=True
            errormsg="Passwords doesn't match"
            Errors.append(errormsg)
        dict["values"]=values
        if errorflag:
            dict["error"]=errorflag
            dict["errors"]=Errors
            print(dict,"hi")
            return render(request,'signup_page.html',context=dict)
        if not errorflag:
            try:
                ss=user.objects.get(email=em)
                print('exists')
                dict['error']=True
                dict['errors']=['Email already exists please do login']
                return render(request,'signup_page.html',dict)
            except:
                xn=''+send(request)+''
                return redirect('verify/')
                
    return render(request,'signup_page.html')


def login(request): 
    print("entered login view")
    global em,pwd,utype
    if request.method=="POST":
        d=request.POST
        for key,value in d.items():
            if key=="email":
                em=value
            if key=="password":
                pwd=value
        try:
            if(user.objects.get(email=em).role=='owner'):
                use=authenticate(username=em.replace('@','1').replace('.','2'),password=pwd)
                print(use)
                if use is not None:
                    auth_login(request,use)
                    request.session['mail'] = em
                    print("session",request.session['mail']," login mail ",em)
                    print('logined')
                    return redirect('home/')
                else:
                    print('not logined')
                    return render(request,'login_page.html',{'error':True,'errormsg':"Invalid Credentials"})
            else:

                use=authenticate(username=em.replace('@','1').replace('.','2'),password=pwd)
                print(use)

                if use is not None:
                    auth_login(request,use)
                    request.session['mail'] = em
                    user_instance=user.objects.get(email=em)
                    request.session['user_id'] = user_instance.pk

                    return redirect('home1/')
                else:
                    print('not logined')
                    return render(request,'login_page.html',{'error':True,'errormsg':"Invalid Credentials"})
        except:
            return render(request,'login_page.html',{'error':True,'errormsg':"Invalid Credentials"})
    return render(request,'login_page.html')






# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib import messages
# from django.conf import settings
# import re
# import smtplib
# from email.message import EmailMessage
# import random
# import string
# from loginapp.models import user
# from django.contrib.auth import authenticate
# from django.contrib.auth import login as auth_login
# from django.contrib.auth import logout as signout
# from django.contrib.auth.models import User
# fn = ''
# ln = ''
# ph = ''
# em = ''
# pwd = ''
# cpwd = ''
# utype = ''
# xn = ''
# d = {}
# a=0
# # Create your views here.

# def home(request):
#     return render(request, 'welcome.html')

# def send(request):
#     msg=EmailMessage()
#     msg['Subject']="Email Verification"
#     msg['From']="House Rentals"
#     msg['To']=em
#     print(em)
#     ran=''.join(random.choices(string.digits, k=6))
#     matt="Hi "+fn+" ,Below is the Confirmation Code to confirm your email address\n"+ran
#     msg.set_content(matt)
#     mys=smtplib.SMTP(settings.EMAIL_HOST,587)
#     mys.starttls()
#     mys.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
#     mys.send_message(msg)
#     mys.quit()
#     return ran
# def verify(request):
#     global xn,d,a
#     hars=False
#     if request.method=="POST":
#         v=request.POST
#         if (v['ver'] == xn):
#             a+=1
#             ins=user(first_name=fn,last_name=ln,email=em,phonenumber=ph,password=pwd,role=utype)
#             ins.save()
#             uses=User.objects.create_user(username=em.replace('@','1').replace('.','2'),password=pwd,email=em,first_name=fn)
#             uses.save()
#             print(ins.email)
#             messages.success(request,"Your account is successfully Created")
#             return redirect('login/')
#         else:
#             if v['press']=="resend":
#                 xn=send(request)
#             else:
#                 hars=True
#     return render(request,'verify.html',{'hars':hars})

# def forgotconfirm(request):
#     print("forgotconfirm")
#     global xn, em
#     if request.method == 'POST':
#         print("forgotconfirm post")
#         em = request.POST['email']
#         regex = '^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$'
#         if not re.search(regex,em):
#             return render(request,'forgot_confirm.html',{'error':True,'errormsg':"Invalid Email Address"})
#         eerr=False
#         try:
# <<<<<<< HEAD
# =======
#             print("forgotconfirm try")

# >>>>>>> 29846bdd8c25b501f33e652145e2ec1691299bdb
#             sd=user.objects.get(email=em)
#             xn = ''+send(request)+''
#             return redirect('verify1')
#         except:
#             print("forgotconfirm except")
#             return render(request,'forgot_confirm.html',{'error':True, 'error_msg':"Account doesn't exist with this email" })
        
#     return render(request, 'forgot_confirm.html')

# def verify1(request):
#     global xn, d
#     hars = False
#     if request.method == "POST":
#         v = request.POST
#         if (v['ver'] == xn):
#             return redirect('forgot')
#         else:
#             hars = True
#             if v['press'] == "resend":
#                 xn = send(request)
#     return render(request, 'verify.html', {'hars': hars})


# def forgot(request):
#     global xn, d
#     hars = False
#     if request.method == "POST":
#         v = request.POST
#         passreg = "^(?=.[A-Za-z])(?=.\d)(?=.[@$!%#?&])[A-Za-z\d@$!%*#?&]{8,}$"
#         pwd = request.POST["password"]
#         cpwd = request.POST["cpassword"]
#         Errors = []
#         errormsg = ''
#         errorflag = False
#         dict = {}
#         if not re.search(passreg, pwd):
#             errorflag = True
#             errormsg = "Password must contain Minimum eight characters, at least one letter, one number and one special character"
#             Errors.append(errormsg)
#         if pwd != cpwd:
#             errorflag = True
#             errormsg = "Passwords doesn't match"
#             Errors.append(errormsg)
#         if errorflag:
#             dict["error"] = errorflag
#             dict["errors"] = Errors
#             return render(request, 'forgot.html', context=dict)
#         print(pwd, em)
#         if not errorflag:
#             pro=user.objects.get(email=em)
#             pro.password=pwd
#             pro.save() 
#             us=User.objects.get(email=em)
#             us.set_password(pwd)
#             us.save()
#             print(us.password)           
#             messages.success(request, "Password reset successful")
#             return redirect('login')
#     return render(request,'forgot.html')

# def signup(request):
#     global fn,ln,ph,em,pwd,utype,cpwd,xn,d
#     if request.method=="POST":
#         d=request.POST
#         for key,value in d.items():
#             if key=="first_name":
#                 fn=value
#             if key=="last_name":
#                 ln=value
#             if key=="email":
#                 em=value
#             if key=="phonenumber":
#                 ph=value
#             if key=="password":
#                 pwd=value
#             if key=="cpassword":
#                 cpwd=value
#             if key=="type":
#                 utype=value

#         values={}
#         values['fname']=fn
#         values['lname']=ln
#         values['email']=em
#         values['phn']=ph
#         Errors=[]
#         errorflag=False
#         dict={}
#         regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
#         passreg="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
#         if not (fn.isalpha() or ln.isalpha()):
#             errorflag=True
#             errormsg="Name should contain only alphabets"
#             Errors.append(errormsg)
#         if not re.search(regex,em):
#             errorflag=True
#             errormsg="Email address is not Valid"
#             Errors.append(errormsg)
#         if len(str(ph))!=10 or (not ph.isdigit()):
#             errorflag=True
#             errormsg="Mobile number must be 10 digits"
#             Errors.append(errormsg)
#         if not re.search(passreg,pwd):
#             errorflag=True
#             errormsg="Password must contain Minimum eight characters, at least one letter, one number and one special character"
#             Errors.append(errormsg)
#         if pwd!=cpwd:
#             errorflag=True
#             errormsg="Passwords doesn't match"
#             Errors.append(errormsg)
#         dict["values"]=values
#         if errorflag:
#             dict["error"]=errorflag
#             dict["errors"]=Errors
#             print(dict,"hi")
#             return render(request,'signup_page.html',context=dict)
#         if not errorflag:
#             try:
#                 ss=user.objects.get(email=em)
#                 print('exists')
#                 dict['error']=True
#                 dict['errors']=['Email already exists please do login']
#                 return render(request,'signup_page.html',dict)
#             except:
#                 xn=''+send(request)+''
#                 return redirect('verify/')
                
#     return render(request,'signup_page.html')


# def login(request): 
#     print("entered login view")
#     global em,pwd,utype
#     if request.method=="POST":
#         d=request.POST
#         for key,value in d.items():
#             if key=="email":
#                 em=value
#             if key=="password":
#                 pwd=value
# <<<<<<< HEAD
#         if(user.objects.get(email=em).role=='owner'):
#             use=authenticate(username=em.replace('@','1').replace('.','2'),password=pwd)
#             print(use)
#             if use is not None:
#                 auth_login(request,use)
#                 request.session['mail'] = em
#                 print("session",request.session['mail']," venky ",em)
#                 print('logined')
#                 return redirect('home/')
#             else:
#                 print('not logined')
#                 return render(request,'login_page.html',{'error':True,'errormsg':"Invalid Credentials"})
#         else:
#             user_instance=user.objects.get(email=em)
#             request.session['user_id'] = user_instance.pk
#             # print(user_instance)
#             # print(request.session['user_id'])
#             return HttpResponse('Page under construction')
# =======
#         try:
#             if(user.objects.get(email=em).role=='owner'):
#                 use=authenticate(username=em.replace('@','1').replace('.','2'),password=pwd)
#                 print(use)
#                 if use is not None:
#                     auth_login(request,use)
#                     request.session['mail'] = em
#                     print("session",request.session['mail']," login mail ",em)
#                     print('logined')
#                     return redirect('home/')
#                 else:
#                     print('not logined')
#                     return render(request,'login_page.html',{'error':True,'errormsg':"Invalid Credentials"})
#             else:
#                 return HttpResponse('Page under construction')
#         except:
#             return render(request,'login_page.html',{'error':True,'errormsg':"Invalid Credentials"})
# >>>>>>> 29846bdd8c25b501f33e652145e2ec1691299bdb
#     return render(request,'login_page.html')


