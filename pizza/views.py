from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from datetime import datetime

def index(request):
    if "username" in request.session:
        return redirect("menu")
    return render(request,'pizza/index.html',{"msg":""})

def register(request):
    return render(request,'pizza/register.html',{"msg":""})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        door_no = request.POST["door_no"]
        street = request.POST["street"]
        city = request.POST["city"]
        if len(User.objects.filter(username=username)) == 0:
            if username == "" or password == "" or email == "" or phone =="" or door_no == "" or street == "" or city == "":
                return render(request,'pizza/register.html',{"msg":"All fields are mandatory while registering"})
            User.objects.create_user(username,email,password)
            user = User.objects.filter(username=username)   
            user_profile = UserProfile(user=user[0],phone=phone,door_no=door_no,street=street,city=city)
            user_profile.save()
        else:
            return render(request,'pizza/register.html',{"msg":"Username already exists choose a different username"})
    return render(request,'pizza/login.html',{"msg":""})

def menu(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if username == "" or password == "":
            return render(request,'pizza/login.html',{"msg":"Username or Password cannot be empty"})
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request,'pizza/login.html',{"msg":"Wrong Credentials"})
        request.session["username"] = username    
    return redirect(menu1)

def menu1(request):
    if "username" not in request.session:
        return redirect("index")
    username = request.session.get("username")
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

def orders(request):
    if "username" not in request.session:
        return render(request,'pizza/index.html',{"msg":"You need to login to place orders"})
    item_names = request.POST["item_names"]
    item_types = request.POST["item_types"]
    item_sizes = request.POST["item_sizes"]
    item_costs = request.POST["item_costs"]
    item_quans = request.POST["item_quans"]
    username = request.POST["username"]
    price = request.POST["price"]

    item_names = convert_string_to_list(item_names)
    item_types = convert_string_to_list(item_types)
    item_sizes = convert_string_to_list(item_sizes)
    item_costs = convert_string_to_list(item_costs)
    item_quans = convert_string_to_list(item_quans)

    for i in range(len(item_names)):
        print(item_names[i])
        print(item_types[i])


    now = datetime.now()
    totalCost = 0
    dt_string = now.strftime("On %d/%m/%Y At %H:%M:%S")
    for i in range(len(item_costs)):
        item = Item.objects.filter(item_name=item_names[i],item_type=item_types[i],item_size=item_sizes[i])
        if len(item) == 0 or len(item) > 1:
            return HttpResponse("Something went wrong,  please login again and try")
        elif round((item[0].price) * int(item_quans[i]) * 100) / 100 != float(item_costs[i]):
            print((item[0].price) * int(item_quans[i]))
            return HttpResponse("Something went wrong,  please login again and try")
        elif username != request.session["username"]:
            return HttpResponse("Something went wrong,  please login again and try")
        totalCost = totalCost + float(item_costs[i])
    if totalCost != float(price):
        return HttpResponse("Something went wrong,  please login again and try")
    user = User.objects.filter(username=request.session["username"])
    user_order = User_order(user=user[0],time_ordered=dt_string,price=float(price))
    user_order.save()
    for i in range(len(item_costs)):
        item = Item.objects.filter(item_name=item_names[i],item_type=item_types[i],item_size=item_sizes[i])
        order = Order(order=user_order,item=item[0],quantity=item_quans[i],item_cost=item_costs[i])
        order.save()    
    return HttpResponse("Ordered Succesfully, Go to Myorders to see updates on your orders")    

def myorders(request , username):
    if "username" not in request.session:
        return redirect('index')
    user = User.objects.filter(username=request.session["username"])        
    user_orders = User_order.objects.filter(user=user[0]).order_by("id")
    user_orders = user_orders.reverse()    
    orders = []
    for i in range(len(user_orders)):
        orders.append(Order.objects.filter(order=user_orders[i]))
        print(orders[i])
    if len(user_orders) == 0:
        context = {
            'msg':"No orders yet"
        }
        return render(request,"pizza/error.html",context)    
    context = {
        'user_orders':user_orders,
        'orders':orders,
        'l':range(len(user_orders)),
        'username':request.session["username"]
    }    
    return render(request,"pizza/myorders.html",context)

def logout_view(request):
    if "username" not in request.session:
        return redirect('index')
    request.session.pop("username")
    return redirect("index")

def convert_string_to_list(x):
    output_list = []
    str = ""
    for i in range(len(x)):
        if x[i] == ',':
            output_list.append(str)
            str = ""
            continue
        str = str + x[i]
    if str != "":
        output_list.append(str)
    return output_list

