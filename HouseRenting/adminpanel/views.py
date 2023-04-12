from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth. models import User
from django.contrib import messages
import datetime
import requests
import re
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from rentee.models import Reviews
from owner.models import Property, Files
from loginapp.models import user
from adminpanel.constants import *


def index(request):
    return render(request, "admin/Admin_login.html")


@csrf_exempt
def connect(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/adminpanel/dashboard')
        else:
            error_mess=[]
            error_mess.append("Invalid Username or Password")
            return render(request,"admin/Admin_login.html",{'error':error_mess})
    else:
        return HttpResponse("Something is wrong")


def dashboard(request):
    users = user.objects.all()
    rentee = 0
    rentee = 0
    owner = 0
    house = 0
    house = len(Property.objects.all())
    Total_Rented_House = 0
    Available_for_Rent = 0
    admin = len(User.objects.all())
    property_data = Property.objects.all()
    for i in users:
        if i.role == "rentee":
            rentee += 1
        if i.role == "owner":
            owner += 1
    for i in property_data:
        if i.status == "Available":
            Available_for_Rent += 1
        else:
            Total_Rented_House += 1
    admin=admin-rentee-owner        
    context = {
        'Total_admin': admin,
        'Total_owner': owner,
        'Total_rentee': rentee,
        'Total_Rented_House': Total_Rented_House,
        'Available_for_Rent': Available_for_Rent,
        'Total_House': house,
        'Total_reviews': len(Reviews.objects.all()),
    }
    return render(request, "admin/dashboard.html", context)


def handellogout(request):
    logout(request)
    return redirect('/adminpanel/logoutpage')


def logoutpage(request):
    return render(request,"admin/Logout.html")


def handellogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("unsuceessfull login")
    else:
        return HttpResponse("404 page not found")

# user info section


def userinfo(request):
    userlist = user.objects.all()
    return render(request, 'admin/User_info.html', {'userlist': userlist})


def user_info_search_id(request):
    if request.method == "GET":
        user_id = request.GET.get('user_id')
        user_data = user.objects.all()
        res = []
        for i in user_data:
            if str(i) == str(user_id):
                res.append(i)
        return render(request, 'admin/User_info.html', {'userlist': res})
    else:
        return HttpResponse("Something is Wrong!!!")


def user_info_search_first_name(request):
    if request.method == "GET":
        first_name = request.GET.get('first_name')
        user_data = user.objects.all()
        res = []
        for i in user_data:
            if str(i.first_name).lower() == str(first_name).lower():
                res.append(i)
        return render(request, 'admin/User_info.html', {'userlist': res})
    else:
        return HttpResponse("Something is Wrong!!!")


def user_info_search_last_name(request):
    if request.method == "GET":
        last_name = request.GET.get('last_name')
        user_data = user.objects.all()
        res = []
        for i in user_data:
            if str(i.last_name).lower() == str(last_name).lower():
                res.append(i)
        return render(request, 'admin/User_info.html', {'userlist': res})
    else:
        return HttpResponse("Something is Wrong!!!")


def user_info_search_email(request):
    if request.method == "GET":
        email = request.GET.get('email')
        user_data = user.objects.all()
        res = []
        for i in user_data:
            if str(i.email) == str(email):
                res.append(i)
        return render(request, 'admin/User_info.html', {'userlist': res})
    else:
        return HttpResponse("Something is Wrong!!!")


def user_info_search_phone_numeber(request):
    if request.method == "GET":
        phone_numeber = request.GET.get('phone_numeber')
        user_data = user.objects.all()
        res = []
        for i in user_data:
            if str(i.phonenumber) == str(phone_numeber):
                res.append(i)
        return render(request, 'admin/User_info.html', {'userlist': res})
    else:
        return HttpResponse("Something is Wrong!!!")


def user_info_search_role(request):
    if request.method == "GET":
        role = request.GET.get('role')
        user_data = user.objects.all()
        res = []
        data = (role.lower())
        for i in user_data:
            if str(i.role).lower() == str(data).lower():
                res.append(i)
        return render(request, 'admin/User_info.html', {'userlist': res})
    else:
        return HttpResponse("Something is Wrong!!!")


def user_info_delete(request, user_id):
    newdata = user.objects.get(user_id=user_id)
    newproperty_data = Property.objects.filter(owner_id=user_id)
    data=User.objects.get(email=newdata.email)
    data.delete()
    newdata.delete()
    newproperty_data.delete()
    return redirect('/adminpanel/userinfo')


def user_info_update(request, user_id):
    userlist = user.objects.get(user_id=user_id)
    error_mess = []
    isrentee = False
    if userlist.role == "rentee":
        isrentee = True
    return render(request, "admin/User_info_update.html", {'userlist': userlist, 'error': error_mess, 'isrentee': isrentee})


def user_info_submit_updated_data(request, user_id):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
       

        user_data = user.objects.get(user_id=user_id)
        data=User.objects.get(email=user_data.email)
        error_mess = []
        count = 0
        
        for i in first_name:
            if (i>='a' and i<='z') or (i>='A' and i<='Z'):
                continue
            else:
                error_mess.append("First_Name should contain only alphabets")
                count+=1
                break
        for i in last_name:
            if (i>='a' and i<='z') or (i>='A' and i<='Z'):
                continue
            else: 
                error_mess.append("Last_Name should contain only alphabets")
                count+=1
                break   

        if len(first_name) <= 2:
            error_mess.append("First Name is too small")
            count += 1
        if len(last_name) <= 2:
            error_mess.append("Last Name is too small")
            count += 1

         
        if count == 0:
            user_data.first_name = first_name
            user_data.last_name = last_name
            data.first_name=first_name
            data.last_name=last_name
            data.save()
            user_data.save()
            return redirect('/adminpanel/userinfo')
        else:
            userlist = user.objects.get(user_id=user_id)
            isrentee = False
            if userlist.role == "rentee":
                isrentee = True
            return render(request, "admin/User_info_update.html", {'userlist': userlist, 'error': error_mess, 'isrentee': isrentee})
    else:
        return HttpResponse("something is wrong")


def user_info_adduser(request):
    error_mess = []
    return render(request, "admin/User_info_add.html", {'error': error_mess})


def add_data(request):
    if request.method == "POST":


        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        role = request.POST.get('role')
        password = request.POST.get('password')
        error_mess = []
        user_data = user.objects.all()
        count = 0

        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        passreg="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"

        if not (first_name.isalpha() or last_name.isalpha()):
            error_mess.append("Name should contain only alphabets")
            count+=1   
        if len(first_name) <= 2:
            error_mess.append("First Name is too small")
            count += 1
        if len(last_name) <= 2:
            error_mess.append("Last Name is too small")
            count += 1
        if not re.search(regex,email): 
            error_mess.append("Email address is not Valid")
            count+=1
        for i in user_data:
            if i.email == email:
                error_mess.append("This Email is already Exit!")
                count += 1
        if len(str(phonenumber))!=10 or (not phonenumber.isdigit()):
            count+=1
            error_mess.append("Mobile number must be 10 digits")
        if not re.search(passreg,password):
            count+=1
            error_mess.append("Password must contain Minimum eight characters, at least one letter, one number and one special character")        


        if count == 0:
            data = user(
                first_name=first_name,
                last_name=last_name,
                role=role,
                email=email,
                password=password,
                phonenumber=phonenumber,
            )
            data.save()
            uses=User.objects.create_user(username=email.replace('@','1').replace('.','2'),password=password,email=email,first_name=first_name)
            uses.save()
        else:
            return render(request, "admin/User_info_add.html", {'error': error_mess})
    return redirect('/adminpanel/userinfo')


# manage Reviews section


def managereviews(request):
    data = Reviews.objects.all()
    return render(request, 'admin/Manage_reviews.html', {'data': data})


def managereview_search_rating_id(request):
    if request.method == "GET":
        rating_id = request.GET.get('rating_id')
        data = Reviews.objects.filter(id=rating_id)
        return render(request, 'admin/Manage_reviews.html', {'data': data})
    else:
        return HttpResponse("PASS")
    

def managereview_search_user_name(request):

    if request.method == "GET":
        user_name = request.GET.get('user_name')
        reviews_table=Reviews.objects.all()
        user_table=user.objects.all()
        data=[]
        arr=[]
        word=""
        for i in user_name:
            if i==' ':
                if len(word)!=0:
                    arr.append(word)
                    word=""
            else: word+=i
        if len(word)!=0:
            arr.append(word)

        if(len(arr)!=2):
            return render(request, 'admin/Manage_reviews.html', {'data': data})
        else:
             first_name=arr[0].lower()
             last_name=arr[1].lower()
             for i in user_table:
                 f_name=(i.first_name).lower()
                 l_name=(i.last_name).lower()
                 if f_name == first_name and l_name == last_name:
                     for j in reviews_table:
                         if str(j.user_id)==str(i.user_id):
                             data.append(j)
    return render(request, 'admin/Manage_reviews.html', {'data': data})


def managereview_search_user_id(request):
    if request.method == "GET":
        user_id = request.GET.get('user_id')
        data = Reviews.objects.filter(user_id=user_id)
        return render(request, 'admin/Manage_reviews.html', {'data': data})
    else:
        return HttpResponse("PASS")   
    
    
def managereview_search_property_id(request):
    if request.method == "GET":
        property_id = request.GET.get('property_id')
        Reviews_data = Reviews.objects.all()
        data=[]
        for i in Reviews_data:
            if str(i.property_id.id)==str(property_id):
                data.append(i)
        return render(request, 'admin/Manage_reviews.html', {'data': data})
    else:
        return HttpResponse("PASS")


def managereview_search_flat_name(request):
    if request.method == "GET":
        flat_name = request.GET.get('flat_name')
        Reviews_data = Reviews.objects.all()
        data=[]
        for i in Reviews_data:
            if str(i.property_id.flat_name)==str(flat_name):
                data.append(i)
        return render(request, 'admin/Manage_reviews.html', {'data': data})
    else:
        return HttpResponse("PASS")
    

def managereview_search_rating(request):
    if request.method == "GET":
        rating = request.GET.get('rating')
        data = Reviews.objects.filter(rating=rating)
        return render(request, 'admin/Manage_reviews.html', {'data': data})
    else:
        return HttpResponse("PASS")
    

def managereviews_update(request, id):
    data = Reviews.objects.get(id=id)
    error_mess = []
    return render(request, 'admin/Manage_reviews_update.html', {'data': data, 'error': error_mess})


def managereviews_delete(request, id):
    newdata = Reviews.objects.get(id=id)
    newdata.delete()
    return redirect('/adminpanel/managereviews')


def managereviews_adddata(request):
    data = Property.objects.all()
    user_data = user.objects.all()
    review_data=[]
    for i in user_data:
        if i.role=="rentee":
            review_data.append(i)
    error_mess = []
    return render(request, 'admin/Manage_reviews_add.html', {'data': data, 'data1': review_data, 'error': error_mess})


def managereviews_add_data(request):
    if request.method == "POST":

        property_id = request.POST.get('property_id')
        user_id = request.POST.get('user_id')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        all_reviews_data = Reviews.objects.all()
        count = 0
        error_mess = []


        for i in all_reviews_data:
            if str(i.user_id) == str(user_id) and str(i.property_id.id)==str(property_id):
                count += 1
                error_mess.append("This user is already give a Review")
        if property_id == None:
            count += 1
            error_mess.append("No property is Available")

        count_alpha=0
        count_number=0
        for i in review:
            if (i>='a' and i<='z') or (i>='A' and i<='Z'):
                count_alpha+=1
            else:
                count_number+=1    
        if count_alpha<=count_number:
            count+=1
            error_mess.append("Invalid Review")        
        if len(review) <= 10:
            count += 1
            error_mess.append("Reviews Length is less")
        count_word=0
        s=""
        for i in review:
            if i==' ':
                if len(s)!=0:
                    count_word+=1
                    s=""
            else: 
                s+=i
        if len(s)!=0:
            count_word+=1       
        if count_word<=3:
            count+=1
            error_mess.append("Number of  word in Reviews is vary less . Write atleast 4 words ")   
        if rating < "1":
            count += 1
            error_mess.append("Rating Must be in Range of 1 to 5")
        if rating > "5":
            count += 1
            error_mess.append("Rating Must be in Range of 1 to 5")
        if len(review) >= 500:
            error_mess.append("Review Length is vary High")
            count += 1


        if count == 0:
            data = Reviews(
                user_id=user.objects.get(user_id=user_id),
                property_id=Property.objects.get(id=property_id),
                review=review,
                rating=rating,
                time_created=datetime.datetime.now(),
            )
            data.save()
        else:
            data = Property.objects.all()
            user_data = user.objects.all()
            review_data=[]
            for i in user_data:
                if i.role=="rentee":
                    review_data.append(i)

            return render(request, 'admin/Manage_reviews_add.html', {'data': data, 'data1': review_data, 'error': error_mess})
        return redirect('/adminpanel/managereviews')
    else:
        return HttpResponse("PASS")


def managereviews_submit_updated_data(request, id):

    if request.method == "POST":
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        data = Reviews.objects.get(id=id)
        error_mess = []
        count = 0
    
        if rating < "1":
            count += 1
            error_mess.append("Rating Must be in Range of 1 to 5")
        if rating > "5":
            count += 1
            error_mess.append("Rating Must be in Range of 1 to 5")
        
        count_alpha=0
        count_number=0
        for i in review:
            if (i>='a' and i<='z') or (i>='A' and i<='Z'):
                count_alpha+=1
            else:
                count_number+=1    
        if count_alpha<=count_number:
            count+=1
            error_mess.append("Invalid Review")        
        if len(review) <= 10:
            count += 1
            error_mess.append("Reviews Length is less")
        count_word=0
        s=""
        for i in review:
            if i==' ':
                if len(s)!=0:
                    count_word+=1
                    s=""
            else: 
                s+=i
        if len(s)!=0:
            count_word+=1       
        if count_word<=3:
            count+=1
            error_mess.append("Number of  word in Reviews is vary less . Write atleast 4 words ")                
        if len(review) >= 500:
            error_mess.append("Review Length is vary High")
            count += 1
        if count == 0:
            data.rating = rating
            data.review = review
            data.save()
            return redirect('/adminpanel/managereviews')
        else:
            data = Reviews.objects.get(id=id)
            return render(request, 'admin/Manage_reviews_update.html', {'data': data, 'error': error_mess})

    else:
        return HttpResponse("PASS")

# manage properties section


def manageproperties(request):
    data = Property.objects.all()
    return render(request, 'admin/Manage_properties_Available.html', {'data': data})


def manageproperties_adddata(request):
    all_data = user.objects.all()
    data = []
    error_mess = []
    for i in all_data:
        if i.role == "owner":
            data.append(i)
    return render(request, 'admin/Manage_properties_Available_add.html', {'data': data, 'error': error_mess})


def manageproperties_submit_data(request):
    if request.method == "POST":
        
        reg="^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$"
        reg1="^[a-zA-Z0-9 ]*$"
        reg2="[A-Za-z0-9'\.\-\s\,]"


        city = request.POST.get('city')
        flat_name = request.POST.get('flat_name')
        furnished = request.POST.get('furnished')
        avg_rating = request.POST.get('avg_rating')
        
        address = request.POST.get('address')
        ramount = request.POST.get('ramount')
        area = request.POST.get('area')
        property_type = request.POST.get('property_type')

        choices = request.POST.get('choices')
        total_flats = request.POST.get('total_flats')
        totfloors = request.POST.get('totfloors')

        flat_type = request.POST.get('flat_type')
        parking = request.POST.get('parking')
        status = request.POST.get('status')
        owner_id = request.POST.get('owner_id')

        availability_date = request.POST.get('availability_date')
        bond = request.POST.get('bond')
        is_wishlist = request.POST.get('is_wishlist')

        if furnished == "on":
            furnished = True
        else:
            furnished = False

        if is_wishlist == "on":
            is_wishlist = True
        else:
            is_wishlist = False

        Errors = []
        count = 0
        errflag=False

        if not re.search(reg,request.POST.get('city')) or len(request.POST.get('city'))<1:
            errflag=True
            error="Invalid City Name"
            Errors.append(error)
        if not re.search(reg1,request.POST.get('flat_name')) or len(request.POST.get('flat_name'))<1 or not request.POST.get('flat_name').isalnum():
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
        if int(request.POST.get('total_flats'))<1:
            errflag=True
            error="No.of Flats can't be zero"
            Errors.append(error)
        if int(request.POST.get('flat_type'))<1:
            errflag=True
            error="There should be atleast 1BHK"
            Errors.append(error)        
        if avg_rating <= "0.00":
            Errors.append("Rating Must Be in 1 to 5")
            count += 1
        if avg_rating > "5.00":
            Errors.append("Rating Must Be in 1 to 5")
            count += 1
        if owner_id == None:
            count += 1
            Errors.append("owner_id is Not Present")
        if bond<="0" and bond>"60":
            count+=1
            Errors.append("Bond Must be 1 months to 60 months")
        if errflag == False and count==0:
            data = Property(
                city=city,
                flat_name=flat_name,
                furnished=furnished,
                avg_rating=avg_rating,
                address=address,
                ramount=ramount,
                area=area,
                property_type=property_type,
                choices=choices,
                total_flats=total_flats,
                totfloors=totfloors,
                flat_type=flat_type,
                parking=parking,
                status=status,
                owner_id=owner_id,
                availability_date=availability_date,
                bond=bond,
                is_wishlist=is_wishlist,
            )
            
            data.myImage=request.FILES['myImage']            
                
            data.save()    
            
            file=request.FILES.getlist('imgs')
            for image in file:
                Files.objects.create(property=data,file=image)
            return redirect('/adminpanel/manageproperties')
        

        else:
            all_data = user.objects.all()
            data = []
            for i in all_data:
                if i.role == "owner":
                    data.append(i)
            return render(request, 'admin/Manage_properties_Available_add.html', {'data': data, 'error': Errors})
    else:
        return HttpResponse("PASS")


def manageproperties_delete(request, id):
    newdata = Property.objects.get(id=id)
    newdata.delete()
    return redirect('/adminpanel/manageproperties')


def manageproperties_update(request, id):
    error_mess = []
    data = Property.objects.get(id=id)
    status = False
    if data.status == "Available":
        status = True
    return render(request, "admin/Manage_properties_Available_update.html", {'data': data, 'error': error_mess, 'status': status})


def manageproperties_submit_updated_data(request, id):

    if request.method == "POST":
        data = Property.objects.get(id=id)
        error_mess = []
        count = 0
        for col in PROPERTY_COL:
            d = request.POST.get(col)

            # data[col] = d
        # city=request.POST.get('city')
        # flat_name=request.POST.get('flat_name')
        # furnished=request.POST.get('furnished')
        # avg_rating=request.POST.get('avg_rating')

        # address=request.POST.get('address')
        # ramount=request.POST.get('ramount')
        # area=request.POST.get('area')
        # property_type=request.POST.get('property_type')

        # choices=request.POST.get('choices')
        # total_flats=request.POST.get('total_flats')
        # totfloors=request.POST.get('totfloors')

        # flat_type=request.POST.get('flat_type')
        # parking=request.POST.get('parking')
        # status=request.POST.get('status')

        # availability_date=request.POST.get('availability_date')
        # bond=request.POST.get('bond')
        # is_wishlist=request.POST.get('is_wishlist')

            if col == FURNISHED or col == IS_WISHLIST:
                if d == "on":
                    d = True
                else:
                    d = "False"

        # if furnished=="on":
        #     furnished=True
        # else:
        #     furnished=False

        # if is_wishlist=="on":
        #     is_wishlist=True
        # else:
        #     is_wishlist=False

            if col == CITY and len(d) <= 2:
                error_mess.append("City name is invalid")
                count += 1
            elif col == FLAT_NAME and len(d) <= 1:
                error_mess.append("Flat Name is vary Less")
                count += 1
            elif col == AVG_RATING and d <= "0":
                error_mess.append("Rating Must Be in 1 to 5")
                count += 1
            elif col == AVG_RATING and d >= "6":
                error_mess.append("Rating Must Be in 1 to 5")
                count += 1
            elif col == ADDRESS and len(d) <= 10:
                error_mess.append("Address is Too Small")
                count += 1

        # if len(city)<=2:
        #     error_mess.append("City name is invalid")
        #     count+=1
        # if len(flat_name)<=1:
        #     error_mess.append("Flat Name is vary Less")
        #     count+=1
        # if avg_rating<="0":
        #     error_mess.append("Rating Must Be in 1 to 5")
        #     count+=1
        # if avg_rating>="6":
        #     error_mess.append("Rating Must Be in 1 to 5")
        #     count+=1
        # if len(address)<=10:
        #     error_mess.append("Address is Too Small")
        #     count+=1
            setattr(data, col, d)

        # data=Property.objects.get(id=id)
        if count == 0:
            #     data.city=city
            #     data.flat_name=flat_name
            #     data.furnished=furnished
            #     data.avg_rating=avg_rating
            #     data.address=address
            #     data.ramount=ramount
            #     data.area=area
            #     data.property_type=property_type
            #     data.choices=choices
            #     data.total_flats=total_flats
            #     data.totfloors=totfloors
            #     data.flat_type=flat_type
            #     data.parking=parking
            #     data.status=status
            #     data.availability_date=availability_date
            #     data.bond=bond
            #     data.is_wishlist=is_wishlist
            data.save()
            file=request.FILES.getlist('imgs')
            for image in file:
                Files.objects.create(property=data,file=image)
            return redirect('/adminpanel/manageproperties')
        else:
            data = Property.objects.get(id=id)
            status = False
            if data.status == "Available":
                status = True
            return render(request, "admin/Manage_properties_Available_update.html", {'data': data, 'error': error_mess, 'status': status})
    else:
        return HttpResponse("PASS")


def manageproperties_search_id(request):
    if request.method == "GET":
        id = request.GET.get('id')
        data = Property.objects.filter(id=id)
        return render(request, 'admin/Manage_properties_Available.html', {'data': data})
    else:
        return HttpResponse("PASS")


def manageproperties_search_city(request):
    if request.method == "GET":
        city = request.GET.get('city')
        data = Property.objects.filter(city=city)
        return render(request, 'admin/Manage_properties_Available.html', {'data': data})
    else:
        return HttpResponse("PASS")


def manageproperties_search_flat_name(request):
    if request.method == "GET":
        flat_name = request.GET.get('flat_name')
        data = Property.objects.filter(flat_name=flat_name)
        return render(request, 'admin/Manage_properties_Available.html', {'data': data})
    else:
        return HttpResponse("PASS")


def manageproperties_search_ramount(request):
    if request.method == "GET":
        ramount = request.GET.get('ramount')
        data = Property.objects.filter(ramount=ramount)
        return render(request, 'admin/Manage_properties_Available.html', {'data': data})
    else:
        return HttpResponse("PASS")


def manageproperties_search_area(request):
    if request.method == "GET":
        area = request.GET.get('area')
        data = Property.objects.filter(area=area)
        return render(request, 'admin/Manage_properties_Available.html', {'data': data})
    else:
        return HttpResponse("PASS")


def manageproperties_search_status(request):
    if request.method == "GET":
        status = request.GET.get('status')
        data = Property.objects.filter(status=status)
        return render(request, 'admin/Manage_properties_Available.html', {'data': data})
    else:
        return HttpResponse("PASS")


def manageproperties_search_owner_id(request):

    if request.method == "GET":
        owner_id = request.GET.get('owner_id')
        data = Property.objects.filter(owner_id=owner_id)
        return render(request, 'admin/Manage_properties_Available.html', {'data': data})
    else:
        return HttpResponse("PASS")


def manageproperties_search_bond(request):

    if request.method == "GET":
        bond = request.GET.get('bond')
        data = Property.objects.filter(bond=bond)
        return render(request, 'admin/Manage_properties_Available.html', {'data': data})
    else:
        return HttpResponse("PASS")

# manage rental properties


def managerental(request):
    all_data = Property.objects.all()
    data = []
    for i in all_data:
        if i.status != "Available":
            data.append(i)
    return render(request, 'admin/Manage_Rental_properties.html', {'data': data})


def managerental_update(request, id):
    data = Property.objects.get(id=id)
    error_mess = []
    status = False
    if data.status == "Available":
        status = True
    return render(request, "admin/Manage_Rental_properties_update.html", {'data': data, 'error': error_mess, 'status': status})


def managerental_submit_updated_data(request, id):
    if request.method == "POST":
        data = Property.objects.get(id=id)
        error_mess = []
        count = 0
        for col in PROPERTY_COL:
            d = request.POST.get(col)

            # data[col] = d
        # city=request.POST.get('city')
        # flat_name=request.POST.get('flat_name')
        # furnished=request.POST.get('furnished')
        # avg_rating=request.POST.get('avg_rating')

        # address=request.POST.get('address')
        # ramount=request.POST.get('ramount')
        # area=request.POST.get('area')
        # property_type=request.POST.get('property_type')

        # choices=request.POST.get('choices')
        # total_flats=request.POST.get('total_flats')
        # totfloors=request.POST.get('totfloors')

        # flat_type=request.POST.get('flat_type')
        # parking=request.POST.get('parking')
        # status=request.POST.get('status')

        # availability_date=request.POST.get('availability_date')
        # bond=request.POST.get('bond')
        # is_wishlist=request.POST.get('is_wishlist')

            if col == FURNISHED or col == IS_WISHLIST:
                if d == "on":
                    d = True
                else:
                    d = "False"

        # if furnished=="on":
        #     furnished=True
        # else:
        #     furnished=False

        # if is_wishlist=="on":
        #     is_wishlist=True
        # else:
        #     is_wishlist=False

            if col == CITY and len(d) <= 2:
                error_mess.append("City name is invalid")
                count += 1
            elif col == FLAT_NAME and len(d) <= 1:
                error_mess.append("Flat Name is vary Less")
                count += 1
            elif col == AVG_RATING and d <= "0":
                error_mess.append("Rating Must Be in 1 to 5")
                count += 1
            elif col == AVG_RATING and d >= "6":
                error_mess.append("Rating Must Be in 1 to 5")
                count += 1
            elif col == ADDRESS and len(d) <= 10:
                error_mess.append("Address is Too Small")
                count += 1
            
        # if len(city)<=2:
        #     error_mess.append("City name is invalid")
        #     count+=1
        # if len(flat_name)<=1:
        #     error_mess.append("Flat Name is vary Less")
        #     count+=1
        # if avg_rating<="0":
        #     error_mess.append("Rating Must Be in 1 to 5")
        #     count+=1
        # if avg_rating>="6":
        #     error_mess.append("Rating Must Be in 1 to 5")
        #     count+=1
        # if len(address)<=10:
        #     error_mess.append("Address is Too Small")
        #     count+=1
            setattr(data, col, d)

        # data=Property.objects.get(id=id)
        if count == 0:
            #     data.city=city
            #     data.flat_name=flat_name
            #     data.furnished=furnished
            #     data.avg_rating=avg_rating
            #     data.address=address
            #     data.ramount=ramount
            #     data.area=area
            #     data.property_type=property_type
            #     data.choices=choices
            #     data.total_flats=total_flats
            #     data.totfloors=totfloors
            #     data.flat_type=flat_type
            #     data.parking=parking
            #     data.status=status
            #     data.availability_date=availability_date
            #     data.bond=bond
            #     data.is_wishlist=is_wishlist
            data.save()
            file=request.FILES.getlist('imgs')

            print("Hello")
            print(file)

            for image in file:
                Files.objects.create(property=data,file=image)
            return redirect('/adminpanel/managerental')
        else:
            data = Property.objects.get(id=id)
            
            return render(request, "admin/Manage_Rental_properties_update.html", {'data': data, 'error': error_mess})
    else:
        return HttpResponse("PASS")


def managerental_search_id(request):
    if request.method == "GET":
        id = request.GET.get('id')
        all_data = Property.objects.all()
        data = []
        for i in all_data:
            if i.status != "Available":
                if str(i.id) == str(id):
                    data.append(i)
        return render(request, 'admin/Manage_Rental_properties.html', {'data': data})
    else:
        return HttpResponse("PASS")


def managerental_search_city(request):
    if request.method == "GET":
        city = request.GET.get('city')
        all_data = Property.objects.all()
        data = []
        for i in all_data:
            if i.status != "Available":
                if str(i.city) == str(city):
                    data.append(i)
        return render(request, 'admin/Manage_Rental_properties.html', {'data': data})
    else:
        return HttpResponse("PASS")


def managerental_search_flat_name(request):
    if request.method == "GET":
        flat_name = request.GET.get('flat_name')
        all_data = Property.objects.all()
        data = []
        for i in all_data:
            if i.status != "Available":
                if str(i.flat_name) == str(flat_name):
                    data.append(i)
        return render(request, 'admin/Manage_Rental_properties.html', {'data': data})
    else:
        return HttpResponse("PASS")


def managerental_search_ramount(request):
    if request.method == "GET":
        ramount = request.GET.get('ramount')
        all_data = Property.objects.all()
        data = []
        for i in all_data:
            if i.status != "Available":
                if str(i.ramount) == str(ramount):
                    data.append(i)
        return render(request, 'admin/Manage_Rental_properties.html', {'data': data})
    else:
        return HttpResponse("PASS")


def managerental_search_area(request):
    if request.method == "GET":
        area = request.GET.get('area')
        all_data = Property.objects.all()
        data = []
        for i in all_data:
            if i.status != "Available":
                if str(i.area) == str(area):
                    data.append(i)
        return render(request, 'admin/Manage_Rental_properties.html', {'data': data})
    else:
        return HttpResponse("PASS")


def managerental_search_status(request):
    if request.method == "GET":
        status = request.GET.get('status')
        all_data = Property.objects.all()
        data = []
        for i in all_data:
            if i.status != "Available":
                if str(i.status) == str(status):
                    data.append(i)
        return render(request, 'admin/Manage_Rental_properties.html', {'data': data})
    else:
        return HttpResponse("PASS")


def managerental_search_owner_id(request):
    if request.method == "GET":
        owner_id = request.GET.get('owner_id')
        all_data = Property.objects.all()
        data = []
        for i in all_data:
            if i.status != "Available":
                if str(i.owner_id) == str(owner_id):
                    data.append(i)
        return render(request, 'admin/Manage_Rental_properties.html', {'data': data})
    else:
        return HttpResponse("PASS")


def managerental_search_bond(request):
    if request.method == "GET":
        bond = request.GET.get('bond')
        all_data = Property.objects.all()
        data = []
        for i in all_data:
            if i.status != "Available":
                if str(i.bond) == str(bond):
                    data.append(i)
        return render(request, 'admin/Manage_Rental_properties.html', {'data': data})
    else:
        return HttpResponse("PASS")