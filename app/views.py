import re
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
# Create your views here.
from app.models import Contact,ProductItems,MyOrders,Medicines



def Home(request):
    myprod = ProductItems.objects.all()
    mymed = Medicines.objects.all()
    context = {"mymed":mymed, "myprod":myprod}
    return render(request,"home.html",context)

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("num")
        desc = request.POST.get("desc")
        query = Contact(name = name , email = email , phoneno = phone , desc = desc)
        query.save()
        messages.info(request,f"Thank You. We Will Get back to you soon {name}")

    return render(request,"contact.html")

def About(request):
    return render(request,"About.html")


def HandleSignup(request):
    
    if request.method == "POST":

        uname = request.POST.get("username")
        email = request.POST.get("email")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        print(uname,email,fname,lname,pass1,pass2)

        if(pass1 != pass2):
            messages.warning(request,"Password is'nt Matching")
            return redirect("/signup")

        try:
            if User.objects.get(username=email):
                messages.info(request,"Username is taken..")
                return redirect("/signup")
        except:
            pass

        myuser = User.objects.create_user(email, uname, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request,"Signup Success")
        return redirect('/login')

    return render(request, "signup.html")


def HandleLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        print(email,pass1)
        myuser = authenticate(username=email, password=pass1)

        if myuser is not None:
            login(request, myuser)
            messages.info(request,"Login Successful")
            return redirect("/")

        else:
            messages.error(request,"Invalid Credentials")
            return redirect("/login")

    return render(request, "login.html")

def HandleLogout(request):
    logout(request)
    messages.warning(request,"Logout")
    return render(request,"login.html")


def medicines(request):
    mymed = Medicines.objects.all()
    context = {"mymed":mymed}
    return render(request,"medicines.html",context)

def products(request):
    myprod = ProductItems.objects.all()
    context = {"myprod":myprod}
    return render(request,"products.html",context)

def myorders(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login to Order")
        return redirect("/login")
    
    mymed = Medicines.objects.all()
    myprod = ProductItems.objects.all()
    current_user=request.user.username
    print(current_user)
    items=MyOrders.objects.filter(email=current_user)
    # items = MyOrders.objects.all()
    print(items)
    context = {"mymed":mymed,"myprod":myprod,"items":items}
    print(context)


    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        item = request.POST.get("items")
        quan = request.POST.get("quantity")
        phone_num = request.POST.get("num")
        address = request.POST.get("address")

        print(name,email,items,quan,phone_num,address)
            
        price = ""
        for i in mymed:
            if item == i.medicine_name:
                price = i.medicine_price
            else:
                pass
        for i in myprod:
            if item == i.prod_name:
                price = i.prod_price
            else:
                pass
            
        totalprice = int(price)*int(quan)
        query = MyOrders(name=name,email=email,items=item,address = address,quantity = quan , price = totalprice , phone_num = phone_num)
        query.save()
        messages.success(request,"Order Successfull")
     
        return redirect("/orders")
          
    return render(request,"orders.html",context)

def deleteOrder(request,id):
    query=MyOrders.objects.get(id=id)
    query.delete()
    messages.success(request,"Order Cancelled Successfully..")
    return redirect("/orders")
