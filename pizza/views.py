from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from datetime import datetime



# Create your views here.
def index(request):
    if "username" in request.session:
        return redirect("menu")
    return render(request,'pizza/index.html',{"msg":""})

def register(request):
    return render(request,'pizza/register.html',{"msg":None})

def login_view(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        email=request.POST["email"]
        k=User.objects.filter(username=username)
        if len(k) == 0:
            User.objects.create_user(username,email,password)
        else:
            return render(request,'pizza/register.html',{"msg":"username already exists choose some other username"})
    return render(request,'pizza/login.html',{"msg":""})

def menu(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]   
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request,'pizza/login.html',{"msg":"wrong credentials"})
        request.session["username"]=username    
    return redirect(menu1)
    print("b")

def menu1(request):
    if "username" not in request.session:
        return redirect("index")
    username=request.session.get("username")
    context = {
        "rpizza" : Regular_pizza.objects.all(),
        "spizza" : Sicilian_pizza.objects.all(),  
        "toppings" : Topping.objects.all(),
        "subs" : Sub.objects.all(),
        "pastas" : Pasta.objects.all(),
        "salads" : Salad.objects.all(),
        "dinnerplatters" : Dinner_platter.objects.all(),
        "username":username,
    }
    if "username" not in request.session:
        return redirect('index')
    return render(request,'pizza/menu.html',context)       

def orders(request):
    if "username" not in request.session:
        return render(request,'pizza/index.html',{"msg":"Login first to place order"})
    item_names=request.POST["item_names"]
    username=request.POST["username"]
    price=request.POST["price"]
    now = datetime.now()
    dt_string = now.strftime("On %d/%m/%Y At %H:%M:%S")	
    counters=counter.objects.get(pk=1)
    k=counters.count
    order = user_order(name=username,items=item_names,order_no=k,time_ordered=dt_string,price=price)
    c=counter.objects.get(pk=1)
    c.count=k+1
    c.save()
    order.save()
    return HttpResponse("hi")

def myorders(request,username):
    if "username" not in request.session:
        return redirect('index')
    orders = user_order.objects.filter(name=username).order_by("order_no")
    if len(orders) == 0:
        context = {
            'msg':"No orders yet"
        }
        return render(request,"pizza/error.html",context)
    orders=orders.reverse()        
    context = {
        'orders':orders,
        'username':username
    }    
    return render(request,"pizza/myorders.html",context)

def logout_view(request):
    if "username" not in request.session:
        return redirect('index')
    request.session.pop("username")
    return redirect("index")

