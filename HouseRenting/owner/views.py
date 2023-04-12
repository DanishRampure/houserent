from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from loginapp.models import user
from owner.models import Property, Files
from django.contrib.auth import logout as signout
from django.contrib.auth.models import User
from rentee.models import Reviews
import math
from django.db.models import Avg
import re
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

def about1(request):
    return render(request,'about1.html')

@login_required(login_url='login')
def home1(request):
    userid=user.objects.get(email=request.session['mail']).user_id
    products=Property.objects.filter(owner_id=userid)
    product_found = True if products.count() > 0 else False
    context={'products':products,'userid':userid,'product_found':product_found}
    return render(request,'home.html',context)




def logoutpage(request):
    try:
        del request.session['mail']
        signout(request)
        messages.success(request,"Logged Out Successfully")
        return home(request)
    except:
        return home(request)




@login_required(login_url='login')
def add(request):
    Errors=[]
    errflag=False
    # arr=["Flat/Apartment","Residential House","Villa","Bachelor rooms","Commercial shops"]
    reg="^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$"
    reg1="^[a-zA-Z0-9 ]*$"
    reg2="[A-Za-z0-9'\.\-\s\,]"
    if request.method=="POST":
            #username=request.POST.get('username')
        saverecord=Property()
        saverecord.owner_id=user.objects.get(email=request.session['mail']).user_id
        values={}



        values['city']=request.POST.get('city')
        values['flat_name']=request.POST.get('flat_name')
        values['address']=request.POST.get('address')
        values['ramount']=request.POST.get('ramount')
        values['area']=request.POST.get('area')
        values['tflat']=request.POST.get('tflat')
        values['flatt']=request.POST.get('flatt')
        values['languages']=request.POST.get('languages')
        values['type']= (request.POST.get('type')=="Full House")
        values['park']=request.POST.get('park')
        values['ftotal']=request.POST.get('ftotal')
        values['status']=request.POST.get('status')
        values['bond']=request.POST.get('bond')
        values['address']=request.POST.get('address')
        values['furnished']= (request.POST.get('furnished')=='Furnished')




        if not re.search(reg,request.POST.get('city')) or len(request.POST.get('city'))<1:
            errflag=True
            error="Invalid City Name"
            Errors.append(error)
        if (not re.search(reg1,request.POST.get('flat_name'))) or (request.POST.get('flat_name').isdigit()) or len(request.POST.get('flat_name'))<1:
            errflag=True
            error="Invalid Property Name"
            Errors.append(error)
        if not re.search(reg2,request.POST.get('address')) or len(request.POST.get('address'))<20:
            errflag=True
            error="Invalid Address"
            Errors.append(error)
        if int(request.POST.get('ramount'))<1:
            errflag=True
            error="Rent Amount can't be zero"
            Errors.append(error)
        if int(request.POST.get('area'))<100:
            errflag=True
            error="Property area can't be so small"
            Errors.append(error)
        if int(request.POST.get('tflat'))<1:
            errflag=True
            error="No.of Flats can't be zero"
            Errors.append(error)
        if int(request.POST.get('flatt'))<1:
            errflag=True
            error="There should be atleast 1BHK"
            Errors.append(error)




        if not errflag:
            saverecord.city=request.POST.get('city')
            saverecord.flat_name=request.POST.get('flat_name')
            if request.POST.get('furnished'):
                saverecord.furnished=True
            else:
                saverecord.furnished=False
            saverecord.address=request.POST.get('address')
            saverecord.ramount=request.POST.get('ramount')
            saverecord.area=request.POST.get('area')
            saverecord.property_type=request.POST.get('languages')
            saverecord.choices=request.POST.get('type')
            saverecord.total_flats=request.POST.get('tflat')
            saverecord.flat_type=request.POST.get('flatt')
            saverecord.parking=request.POST.get('park')
            saverecord.totfloors=request.POST.get('ftotal') 
            saverecord.availability_date=request.POST.get('status')
            saverecord.bond=request.POST.get('bond')
            
            files=request.FILES.getlist('imgs')
            if len(request.FILES)!=0:
                saverecord.myImage=request.FILES['myImage']
            saverecord.save()
            for image in files:
                Files.objects.create(property=saverecord,file=image)


            messages.success(request,"your property has been added")
            return redirect('home1')
        else:
            return render(request,'add.html',{ 'Errors': Errors, 'error':errflag, 'values':values})
    return render(request,'add.html',{ 'Errors': Errors, 'error':errflag})
@login_required(login_url='login')




def profile(request):
    print("Hello")
    data=user.objects.get(email=request.session['mail'])
    bus=User.objects.get(email=request.session['mail'])
    Errors=[]
    reg1="^[a-zA-Z ]*$"
    errflag=False
    if request.method=="POST":
        if not request.POST.get('first_name').isalpha() or len(request.POST.get('first_name'))<2:
            errflag=True
            err="Invalid First Name"
            Errors.append(err)
        if not re.search(reg1,request.POST.get('last_name'))or len(request.POST.get('last_name'))<2:
            errflag=True
            err="Invalid Last Name"
            Errors.append(err)
        if not request.POST.get('phonenumber').isdigit() or len(request.POST.get('phonenumber'))<10:
            errflag=True
            err="Invalid Phone Number"
            Errors.append(err)
        if not errflag:
            data.first_name=request.POST.get('first_name')
            data.last_name=request.POST.get('last_name')
            bus.first_name=request.POST.get('first_name')
            data.phonenumber=request.POST.get('phonenumber')
            bus.save()
            data.save()
            return redirect('home1')
        else:
            return render(request,'profile.html',{'data':data, 'Errors': Errors, 'error': errflag})
    return render(request,'profile.html',{'data':data, 'Errors': Errors, 'error': errflag})



@login_required(login_url='login')
def prop(request,id):
    Errors=[]
    errflag=False
    property = Property.objects.get(id=id)
    # print("venky ",property)
    images = Files.objects.filter(property=property)
    # print(images)
    try:
            # reviews = Reviews.objects.filter(property_id=prop_id).order_by('-id')[:1]
        reviews = Reviews.objects.filter(property_id=id).select_related('user_id').order_by('-id')[:1]
        remaining_reviews = Reviews.objects.filter(property_id=id).select_related('user_id').order_by('-id')[1:]
            # remaining_reviews = Reviews.objects.filter(property_id=prop_id).order_by('-id')[1:] 
    except Reviews.DoesNotExist:
        reviews=[]
    if len(reviews) == 0:
        review_msg = "No reviews found"
    else:
        review_msg = ""
    show=Reviews.objects.filter(property_id_id=id)
    num_ratings = len(show)
    avg_rating = show.aggregate(Avg('rating'))['rating__avg'] or 0
    # avg_rating_formatted = '{:.1f}'.format(avg_rating)
    five_star = show.filter(rating=5).count()
    four_star = show.filter(rating=4).count()
    three_star = show.filter(rating=3).count()
    two_star = show.filter(rating=2).count()
    one_star = show.filter(rating=1).count()
  
        
    if num_ratings > 0:
        percentage_5_star = math.floor((five_star / num_ratings) * 100)
        percentage_4_star = math.floor((four_star / num_ratings) * 100)
        percentage_3_star = math.floor((three_star / num_ratings) * 100)
        percentage_2_star = math.floor((two_star / num_ratings) * 100)
        percentage_1_star = math.floor((one_star / num_ratings) * 100)
    else:
        percentage_5_star = percentage_4_star = percentage_3_star = percentage_2_star = percentage_1_star = 0
    context={'property':property,'images':images, "remaining_count" : remaining_reviews.count(), "review_msg":review_msg, "remaining_reviews" : remaining_reviews, "reviews": reviews, 'choice': property.choices=="Full House", "furnish": property.furnished , "show": show,"review_count":show.count(), 'avg_rating': avg_rating, 'num_ratings': num_ratings, 'five_star': five_star, 'four_star': four_star, 'three_star': three_star, 'two_star': two_star, 'one_star': one_star, 'percentage_5_star': percentage_5_star, 'percentage_4_star': percentage_4_star, 'percentage_3_star': percentage_3_star, 'percentage_2_star': percentage_2_star, 'percentage_1_star': percentage_1_star,}
    # print(property.choices)
    reg="^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$"
    reg1="^[a-zA-Z0-9 ]*$"
    reg2="[A-Za-z0-9'\.\-\s\,]"
    if request.method=="POST":
        if not re.search(reg,request.POST.get('city')) or len(request.POST.get('city'))<1:
            errflag=True
            error="Invalid City Name"
            Errors.append(error)
        if (not re.search(reg1,request.POST.get('flat_name'))) or (request.POST.get('flat_name').isdigit()) or len(request.POST.get('flat_name'))<1:
            errflag=True
            error="Invalid Property Name"
            Errors.append(error)
        if not re.search(reg2,request.POST.get('address')) or len(request.POST.get('address'))<20:
            errflag=True
            error="Invalid Address"
            Errors.append(error)
        if int(request.POST.get('ramount'))<1:
            errflag=True
            error="Rent Amount can't be zero"
            Errors.append(error)
        if int(request.POST.get('area'))<100:
            errflag=True
            error="Property area can't be so small"
            Errors.append(error)
        if int(request.POST.get('tflat'))<1:
            errflag=True
            error="No.of Flats can't be zero"
            Errors.append(error)
        if int(request.POST.get('flatt'))<1:
            errflag=True
            error="There should be atleast 1BHK"
            Errors.append(error)
        
        context['Errors']=Errors
        context['error']=errflag
        if not errflag:
            property.city=request.POST.get('city')
            property.flat_type=request.POST.get('flatt')
            property.flat_name=request.POST.get('flat_name')
            if request.POST.get('furnished')=="Furnished":
                property.furnished=True
            else:
                property.furnished=False
            property.choices=request.POST.get('type')
            property.ramount=request.POST.get('ramount')
            property.area=request.POST.get('area')
            property.total_flats=request.POST.get('tflat')
            property.totfloors=request.POST.get('ftotal')
            property.parking=request.POST.get('park')
            property.address=request.POST.get('address')
            property.status=request.POST.get('status')
            property.availability_date=request.POST.get('date')
            property.bond=request.POST.get('bond')
            property.save()
            file=request.FILES.getlist('imgs')
            for image in file:
                Files.objects.create(property=property,file=image)
            return redirect('home1')
        else:
            return render(request,'prop.html',context)
    return render(request,'prop.html',context)
