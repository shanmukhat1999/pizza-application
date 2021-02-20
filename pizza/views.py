from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from datetime import datetime

def func(x):
    i=0
    s=""
    a=[]
    for i in range(len(x)):
        if x[i]==',':
            a.append(s)
            s=""
            continue
        s=s+x[i]
    if s != "":    
        a.append(s)
    return a        

# Create your views here.
def index(request):
    if "username" in request.session:
        return redirect("menu")
    return render(request,'pizza/index.html',{"msg":""})

def register(request):
    return render(request,'pizza/register.html',{"msg":""})

def login_view(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        door_no=request.POST["door_no"]
        street=request.POST["street"]
        city=request.POST["city"]
        k=User.objects.filter(username=username)
        if len(k) == 0:
            if username == "" or password == "" or email == "" or phone =="" or door_no == "" or street == "" or city == "":
                return render(request,'pizza/register.html',{"msg":"all fields are mandatory"})
            User.objects.create_user(username,email,password)
            u = User.objects.filter(username=username)   
            u_p = UserProfile(user=u[0],phone=phone,door_no=door_no,street=street,city=city)
            u_p.save()
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
        "rpizza" : Item.objects.filter(item_type="Regular-pizza").order_by("item_name"),
        "spizza" : Item.objects.filter(item_type="Sicilian-pizza").order_by("item_name"),
        "toppings" : Item.objects.filter(item_type="Toppings").order_by("item_name"),
        "salads" : Item.objects.filter(item_type="Salads").order_by("item_name"),  
        "pasta" : Item.objects.filter(item_type="Pasta").order_by("item_name"),
        "subs" : Item.objects.filter(item_type="Subs").order_by("item_name"),
        "dinnerplatters" : Item.objects.filter(item_type="Dinner-platters").order_by("item_name"),
        "username":username,
    }
    if "username" not in request.session:
        return redirect('index')
    return render(request,'pizza/menu.html',context)       

"""def orders(request):
    if "username" not in request.session:
        return render(request,'pizza/index.html',{"msg":"Login first to place order"})
    item_names=request.POST["item_names"]
    item_types=request.POST["item_types"]
    item_sizes=request.POST["item_sizes"]
    item_costs=request.POST["item_costs"]
    item_quans=request.POST["item_quans"]
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
    return HttpResponse("hi")"""

def orders(request):
    if "username" not in request.session:
        return render(request,'pizza/index.html',{"msg":"Login first to place order"})
    item_names=request.POST["item_names"]
    item_types=request.POST["item_types"]
    item_sizes=request.POST["item_sizes"]
    item_costs=request.POST["item_costs"]
    item_quans=request.POST["item_quans"]
    username=request.POST["username"]
    price=request.POST["price"]

    item_names=func(item_names)
    item_types=func(item_types)
    item_sizes=func(item_sizes)
    item_costs=func(item_costs)
    item_quans=func(item_quans)

    for i in range(len(item_names)):
        print(item_names[i])
        print(item_types[i])


    now = datetime.now()
    x=0
    dt_string = now.strftime("On %d/%m/%Y At %H:%M:%S")
    for i in range(len(item_costs)):
        k=Item.objects.filter(item_name=item_names[i],item_type=item_types[i],item_size=item_sizes[i])
        if len(k)==0 or len(k)>1:
            print("a")
            return HttpResponse("Something went wrong, Try again")
        elif round((k[0].price)*int(item_quans[i])*100)/100 != float(item_costs[i]):
            print((k[0].price)*int(item_quans[i]))
            print("b")
            return HttpResponse("Something went wrong, Try again")
        elif username!=request.session["username"]:
            print("c")
            return HttpResponse("Something went wrong, Try again")
        x=x+float(item_costs[i])    
    if x != float(price):
        print("d")
        return HttpResponse("Something went wrong, Try again")
    u = User.objects.filter(username=request.session["username"])    
    u_o = User_order(user=u[0],time_ordered=dt_string,price=float(price))
    u_o.save()
    for i in range(len(item_costs)):
        k = Item.objects.filter(item_name=item_names[i],item_type=item_types[i],item_size=item_sizes[i])
        o = Order(order=u_o,item=k[0],quantity=item_quans[i],item_cost=item_costs[i])
        o.save()    
    return HttpResponse("Ordered Succesfully, Go to Myorders to see updates on status")    

def myorders(request,username):
    if "username" not in request.session:
        return redirect('index')
    u = User.objects.filter(username=request.session["username"])        
    u_o = User_order.objects.filter(user=u[0]).order_by("id")
    u_o=u_o.reverse()    
    o = []
    for i in range(len(u_o)):
        o.append(Order.objects.filter(order=u_o[i]))
        print(o[i])
    if len(u_o) == 0:
        context = {
            'msg':"No orders yet"
        }
        return render(request,"pizza/error.html",context)    
    context = {
        'user_orders':u_o,
        'orders':o,
        'l':range(len(u_o)),
        'username':request.session["username"]
    }    
    return render(request,"pizza/myorders.html",context)

def logout_view(request):
    if "username" not in request.session:
        return redirect('index')
    request.session.pop("username")
    return redirect("index")
