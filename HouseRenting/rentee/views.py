#-----NEW CODE-----#

from django.shortcuts import render,get_object_or_404
from  owner.models import Property,Files
from loginapp.models import user
from rentee.models import Reviews , About
from django.http import JsonResponse
import json
from django.views import View
from django.db.models import Avg,Q
import math
from django.urls import reverse
from rentee.models import WishList
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

def show(request):
    try:
       user_id = request.session["user_id"]
    except:
        return  redirect("http://127.0.0.1:8000/rentee/session/")
    user_id = request.session["user_id"]
    favs = WishList.objects.filter(user_id=user_id)
    
    properties = []
    for fav in favs:
        
        prop = Property.objects.get(id=fav.property_id.id)
        avg = Reviews.objects.filter(property_id=prop).aggregate(Avg('rating'))
        prop.avg_rating = avg["rating__avg"]
        single_prop  ={}
        single_prop["id"]  = prop.id
        single_prop["city"] = prop.city
        single_prop["flat_name"] = prop.flat_name
        single_prop["furnished"] = prop.furnished
        single_prop["avg_rating"]= prop.avg_rating
        single_prop["address"]= prop.address
        single_prop["ramount"] = prop.ramount
        single_prop["area"]    = prop.area
        single_prop["property_type"] = prop.property_type
        single_prop["choices"]   =  prop.choices
        single_prop["myImage"]   = prop.myImage
        single_prop["total_flats"] = prop.total_flats
        single_prop["totfloors"]   = prop.totfloors
        single_prop["flat_type"]   = prop.flat_type
        single_prop["parking"]     = prop.parking
        single_prop["status"]      = prop.status
        single_prop["availabilty_date"] = prop.availability_date
        single_prop["owner_id"]      = prop.owner_id
        single_prop["bond"]   = prop.bond
        single_prop["is_wishlist"]  = True
        print(prop.id)
        #property.is_wishlist= True
        properties.append(single_prop)
   
    return render(request,"rentee/wishlist.html",{"properties":properties,"count":len(properties)})


def aboutus(request):
    try:
       user_id = request.session["user_id"]
    except:
        return  redirect("http://127.0.0.1:8000/rentee/session/")
    about = About.objects.last()
    template = 'rentee/about.html'
    context = {
        "about": about
    }

    return render(request, template, context)



def wishlist(request):
    try:
       user_id = request.session["user_id"]
    except:
        return  redirect("http://127.0.0.1:8000/rentee/session/")
    if(request.method=="POST"):
        data = json.loads(request.body)
        prop_id = data["prop_id"]
        status =  data["status"]
        user_id = request.session["user_id"]
        curr_user = user.objects.get(user_id=user_id)
        prop      = Property.objects.get(id=prop_id)
        if(status=="add"):
            wish= WishList(user_id=curr_user,property_id=prop)
            wish.save()
            return JsonResponse({"status":"successfully added"})
        else:
            wish = WishList.objects.filter(user_id=curr_user,property_id=prop).delete()
            return JsonResponse({"status":"successfully removed"})

# def home(request):
#     property_list = Property.objects.all()
#     template = 'rentee/home.html'
#     context = {
#         'property_list': property_list,
#     }
#     return render(request, template, context)



def list(request):
    try:
       user_id = request.session["user_id"]
    except:
        return  redirect("http://127.0.0.1:8000/rentee/session/")
    property_list = Property.objects.all()
    print(property_list)
    template = 'rentee/properties.html'
    context = {
        'property_list': property_list,
    }
    return render(request, template, context)


def location(request):
    try:
       user_id = request.session["user_id"]
    except:
        return  redirect("http://127.0.0.1:8000/rentee/session/")
    location = request.GET.get("location")
    furnished_query = request.GET.get("type", None)
    minprice_query = request.GET.get("minprice")
    maxprice_query = request.GET.get("maxprice")
    bedroom_query = request.GET.get("bedroom", None)
    print(bedroom_query)
    user_id = request.session["user_id"]
    loggedin_user = user.objects.filter(user_id=user_id)
    first_name=   loggedin_user[0].first_name
    sort_query = request.GET.get('sortby', None)
    properties = Property.objects.filter(city = location)
    if sort_query:
        print(sort_query) #prints the value of the sortby query
        if sort_query == 'asc':
            properties = Property.objects.filter(city=location).order_by('ramount')
        elif sort_query == 'dsc':
            properties = Property.objects.filter(city=location).order_by('-ramount') 
        elif sort_query == 'rating':
            properties = Property.objects.filter(city=location).order_by('avg_rating')
        elif sort_query == '':
            properties = Property.objects.all()
    else:
        properties = Property.objects.filter(city = location)

    if furnished_query: 
        properties = Property.objects.filter(Q(furnished = furnished_query))

    if minprice_query and maxprice_query:
        properties = Property.objects.filter(Q(ramount__gte = minprice_query) & Q(ramount__lte = maxprice_query))

    if bedroom_query:
        properties = Property.objects.filter(Q(flat_type = bedroom_query))
    props = []
    print(properties)
    for prop  in properties:
       avg = Reviews.objects.filter(property_id= prop).aggregate(Avg('rating'))
       prop.avg_rating = avg["rating__avg"]
       single_prop  ={}
       single_prop["id"]  = prop.id
       single_prop["city"] = prop.city
       single_prop["flat_name"] = prop.flat_name
       single_prop["furnished"] = prop.furnished
       single_prop["avg_rating"]= prop.avg_rating
       single_prop["address"]= prop.address
       single_prop["ramount"] = prop.ramount
       single_prop["area"]    = prop.area
       single_prop["property_type"] = prop.property_type
       single_prop["choices"]   =  prop.choices
       single_prop["myImage"]   = prop.myImage
       single_prop["total_flats"] = prop.total_flats
       single_prop["totfloors"]   = prop.totfloors
       single_prop["flat_type"]   = prop.flat_type
       single_prop["parking"]     = prop.parking
       single_prop["status"]      = prop.status
       single_prop["availabilty_date"] = prop.availability_date
       single_prop["owner_id"]      = prop.owner_id
       single_prop["bond"]   = prop.bond
      
       wish =  WishList.objects.filter(user_id=user_id,property_id=prop)
       if(wish.count()!=0):
           single_prop["is_wishlist"] =True
       else:
           single_prop["is_wishlist"] =False
       props.append(single_prop)
    return render(request,"rentee/properties.html",{
          "props" : props,
         "properties" : properties, "location": location,"first_name":first_name
    })

def Property_type(request):
    try:
       user_id = request.session["user_id"]
    except:
        return  redirect("http://127.0.0.1:8000/rentee/session/")
    Prop_type=request.GET.get("Property_type")
    properties = Property.objects.filter(property_type= Prop_type)
    for prop  in properties:
       avg = Reviews.objects.filter(property_id= prop).aggregate(Avg('rating'))
       prop.avg_rating = avg["rating__avg"]
    return render(request,"rentee/properties.html",{
         "properties" : properties
    })

 
def Property_reviews(request):
       
    try:
       user_id = request.session["user_id"]
    except:
        return  redirect("http://127.0.0.1:8000/rentee/session/")
    property_id = request.GET.get("id")
    # print(property_id)
    prop=get_object_or_404(Property,id=property_id)
    mydata = get_object_or_404(Property, pk=property_id)
    images = Files.objects.filter(property_id=property_id)
    owner=mydata.owner_id
    owner_det=get_object_or_404(user,user_id=owner)
    
    ca=0
    if images.count()<=4:
        Count=images.count()
        Count=True
        images=images.order_by('id')[:]
        ca=images.count()
    else:
        Count=images.count()
        Count=False
        images=images.order_by('id')[:5]
    # recently_viewed
    if 'recently_viewed' in request.session:
        if property_id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(property_id)

        request.session['recently_viewed'].insert(0, property_id)
        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [property_id]

    request.session.modified = True

    # reviws code
    try:
        # reviews = Reviews.objects.filter(property_id=prop_id).order_by('-id')[:1]
        reviews = Reviews.objects.filter(property_id=property_id).select_related('user_id').order_by('-id')[:1]
        remaining_reviews = Reviews.objects.filter(property_id=property_id).select_related('user_id').order_by('-id')[1:]
        # remaining_reviews = Reviews.objects.filter(property_id=prop_id).order_by('-id')[1:] 
    except Reviews.DoesNotExist:
        reviews=[] 
    if len(reviews) == 0:
        review_msg = "No reviews found"
    else:
        review_msg = ""
    # overall rating code
    ratings = Reviews.objects.filter(property_id=property_id)
    num_ratings = len(ratings)
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    # avg_rating_formatted = '{:.1f}'.format(avg_rating)
    five_star = ratings.filter(rating=5).count()
    four_star = ratings.filter(rating=4).count()
    three_star = ratings.filter(rating=3).count()
    two_star = ratings.filter(rating=2).count()
    one_star = ratings.filter(rating=1).count()

    
    if num_ratings > 0:
        percentage_5_star = math.floor((five_star / num_ratings) * 100)
        percentage_4_star = math.floor((four_star / num_ratings) * 100)
        percentage_3_star = math.floor((three_star / num_ratings) * 100)
        percentage_2_star = math.floor((two_star / num_ratings) * 100)
        percentage_1_star = math.floor((one_star / num_ratings) * 100)
    else:
        percentage_5_star = percentage_4_star = percentage_3_star = percentage_2_star = percentage_1_star = 0
    return render(request,'rentee/property.html',{'property':prop,
    "remaining_reviews" : remaining_reviews,
    "reviews"      : reviews,
    "property_id"  : property_id,
    "remaining_count" : remaining_reviews.count(),
    "review_msg":review_msg,
    'mydata': mydata,
    'owner':owner_det,
    'images': images,
    'images_actual_count': images.count()-4,
    'images_less':Count,
    'images_actual_count2': ca,
    'avg_rating': avg_rating,
    'num_ratings': num_ratings,
    'five_star': five_star,
    'four_star': four_star,
    'three_star': three_star,
    'two_star': two_star,
    'one_star': one_star,
    'percentage_5_star': percentage_5_star,
    'percentage_4_star': percentage_4_star,
    'percentage_3_star': percentage_3_star,
    'percentage_2_star': percentage_2_star,
    'percentage_1_star': percentage_1_star,                                                   
    })
  


def home(request):
    try:
       user_id = request.session["user_id"]
    except:
        print("Redirect")
        return  redirect("http://127.0.0.1:8000/rentee/session/")
    user_id = request.session["user_id"]
    loggedin_user = user.objects.filter(user_id=user_id)
    first_name=   loggedin_user[0].first_name
    recently_viewed_properties = None
    if 'recently_viewed' in request.session:
        properties = Property.objects.filter(pk__in=request.session['recently_viewed'])
        recently_viewed_properties = sorted(properties, 
            key=lambda x: request.session['recently_viewed'].index(str(x.id))
            )

    # if recently_viewed_products is not None:
    #     for recent_product in recently_viewed_products:
    #         print(recent_product)       
    return render(request,"rentee/home.html", {"first_name":first_name,'recently_viewed_properties': recently_viewed_properties})


def create_review(request):
    try:
       user_id = request.session["user_id"]
    except:
        return  redirect("http://127.0.0.1:8000/rentee/session/")
    if(request.method=="POST"):
            data = json.loads(request.body)
            #   print(data)
            review = data["review"]
            rating = data["rating"]
            id     = data["id"]
            property_instance  = Property.objects.get(id=id)
            user_id = request.session["user_id"]
            user_instance  =  user.objects.get(user_id=user_id)
            try:
                review = Reviews.objects.get(property_id=property_instance,user_id=user_instance)
                return JsonResponse({"status" : "You have already submitted a review for this property."})
            except Reviews.DoesNotExist:
                review = Reviews(review=review,rating=rating,property_id=property_instance,user_id=user_instance,)
                review.save()
                return JsonResponse({"status" : "Your review has been successfully posted."})  


def detail(request):
    try:
       user_id = request.session["user_id"]
    except:
        return  redirect("http://127.0.0.1:8000/rentee/session/")

    mydata_id=request.GET.get("id")
    mydata = get_object_or_404(Property, id=mydata_id)
    reviews = Reviews.objects.filter(property_id=mydata_id).select_related('user_id').order_by('-id')[:1]
    remaining_reviews = Reviews.objects.filter(property_id=mydata_id).select_related('user_id').order_by('-id')[1:]
    images = Files.objects.filter(property_id=mydata_id)
    c=0
    if images.count()<=4:
        Count=images.count()
        Count=True
        images=images.order_by('id')[:]
        c=images.count()
    else:
        Count=images.count()
        Count=False
        images=images.order_by('id')[:6]
       
        
    context = {
        'mydata': mydata,
        'images': images,
        'mydata_id':mydata_id,
        'images_actual_count': images.count()-4,
        'images_less':Count,
        'images_actual_count2': c-1,
        "remaining_reviews" : remaining_reviews,
        "reviews"      : reviews,
        }
  
    return render(request, 'rentee/property.html', context)

def session(request):
    return render(request, 'rentee/session.html')


def images(request):
    try:
       user_id = request.session["user_id"]
    except:
        return  redirect("http://127.0.0.1:8000/rentee/session/")
    myimg_id=request.GET.get("id")
    #images = get_object_or_404(Files,property_id=myimg_id)
    images=Files.objects.filter(property_id=myimg_id)
    context = {
        'images': images,
        'prop_id':myimg_id,
       }
    return render(request, 'rentee/images.html', context)


# def images(request,id):
   
#     images = Files.objects.all()
#     context = {
#         'images': images,
#        }
#     return render(request, 'rentee/images.html', context)


# def about(request):
#     template = 'rentee/property.html'
#     context = {}

#     return render(request, template, context)




#----- OLD CODE-----#

# from django.shortcuts import render
# # from book_outlet.models import user,property,Reviews
# from loginapp.models import user
# from ownerapp.models import Property as property
# from rentee.models import Reviews
# from django.shortcuts import render
# from django.http import HttpResponse,HttpResponseRedirect
# from django.views.decorators.csrf import csrf_exempt,csrf_protect,requires_csrf_token
# from django.shortcuts import render,get_object_or_404
# # from rest_framework import status
# # from rest_framework.decorators import api_view
# # import rest_framework
# from django.http import JsonResponse


# import json
# from django.http import JsonResponse
# from django.db.models import Q
# from django.views import View

   
# class signup(View):
#    def get(self,request):
#       return render(request,"rentee/register.html")
#    def post(self,request):
#       data = json.loads(request.body)
#       print(data)
#       name = data['name']
#       email = data['email']
#       password = data['password']
#       role   = data['role']
#       phone =   data['phoneNumber']
#       u  = user(name=name,email=email,password=password,role=role,phone=phone)
#       try:
#         u.save() 
#       except:
#          return HttpResponse("you have already an account")
#       print(data)
#       return HttpResponse("successful")


# class login(View):
#    def get(self,request):
#       return render(request,"rentee/login.html")
#    def post(self,request):
#       data = json.loads(request.body)
#       email = data['email']
#       password = data['password']
#       print(data)
#       us = user.objects.filter(Q(email=email),Q(password=password))
#       print(us.count())
#       if(us.count()==1):
         
#          print(us[0].email)
#          us = us[0]
#          print(us.pk)
#          request.session["id"]=us.pk
#          #request.id = us.id
#          dict = {
#             "status":  True,
#             "name"  :  us.name

#          }
         
#          return HttpResponse(json.dumps(
#             dict
#          ))
#       else:
#          return HttpResponse(json.dumps({
#             "status" : False,
#             "message" : "Entered Email and password are not matching"
#          }))

# def home(request):
#    print(request.session['id'])
#    if(request.method == "GET"):
#       name = request.GET.get("name")      
#       return render(request,"rentee/home.html",{
#          "name" : name
#       })


# def Property(request):
#    #if(request.method=="GET"):
#       # prop_id =  request.GET.get("id")
#       # prop_id = int(prop_id)
#       # prop = property.objects.filter(id=prop_id)
#       # prop = prop[0]
#       # return render(request,"rentee/detail.html",{
#       #    "property" : prop
#       # })
#         prop_id = request.GET.get("id")
#         print(prop_id)
#         prop=get_object_or_404(property,id=prop_id)
#         print(prop.flat_name)
#         reviews = Reviews.objects.filter(property_id=prop_id).order_by('-id')[:1]
#         remaining_reviews = Reviews.objects.filter(property_id=prop_id).order_by('-id')[1:]
#         return render(request,'product_new.html',{'property':prop,
#         "remaining_reviews" : remaining_reviews,
#         "reviews"      : reviews,
#         "property_id"  : prop_id,
#         "remaining_count" : remaining_reviews.count()       
                                                              
#         })



# class review(View):
#    def post(self,request):
#       data = json.loads(request.body)
#       print(data)
#       review = data["review"]
#       rating = data["rating"]
#       id     = data["id"]
#       prop  = property.objects.get(id=1)
#       user_id = request.session["id"]
#       us  =  user.objects.get(id=user_id)
#       print(user_id)
#       print(us.name)
#       revw = Reviews(review=review,rating=rating,property_id=prop,user_id=user_id,user_name =us.name)
#       revw.save()
#       return JsonResponse({
#          "status" : "You review is successfully posted"
#       })
      
# def location(request):
#     location = request.GET.get("location")
#     print(location)
#     properties = property.objects.filter(city = location)
#     return render(request,"rentee/list.html",{
#          "properties" : properties
#     })


# def reviews(request,property_id):
#     reviews = Reviews.objects.filter(property_id=property_id).order_by('-id')[:1]
#     remaining_reviews = Reviews.objects.filter(property_id=property_id).order_by('-id')[1:]
#     #remaining_reviews = Reviews.objects.filter(property_id=property_id).count() - 2
#     context = {
#         'reviews': reviews,
#         'remaining_reviews': remaining_reviews,
#         'property_id': property_id,
#     }
#     return context