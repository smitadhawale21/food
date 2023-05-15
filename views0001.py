from django.shortcuts import render,redirect
from AdminApp.models import Category,Food
from django.http import HttpResponse
from UserApp.models import UserInfo,Cart,Payment,Order_Master
from datetime import datetime

# Create your views here.
def homepage(request):
    cats = Category.objects.all()
    foods=Food.objects.all()
    return render(request,"master.html",{"cats":cats,"foods":foods})

def ShowItems(request,cid):
    cats = Category.objects.all()
    cat = Category.objects.get(id=cid)
    #Filter method is used to fetch more than 1 objects
    #It returns collection of objects
    foods = Food.objects.filter(category=cat)
    return render(request,"master.html",{"cats":cats,"foods":foods})

def ViewDetails(request,id):
    food = Food.objects.get(id=id)
    return render(request,"ViewDetails.html",{"food":food})

def Login(request):
    cats = Category.objects.all()
    if(request.method == "GET"):
        return render(request,"Login.html",{"cats":cats})
    else:
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        try:
            user = UserInfo.objects.get(username = uname,password=pwd)
        except:
            return redirect(Login)
        else:
            request.session["uname"]=uname
            return redirect(homepage)
        
def SignUp(request):
    cats = Category.objects.all()
    if(request.method == "GET"):
        return render(request,"SignUp.html",{"cats":cats,})
    else:
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        email = request.POST["email"]

        user = UserInfo(uname,pwd,email)
        user.save()
        return redirect(homepage)

def Logout(request):
    request.session.clear()
    return redirect(homepage)


def AddToCart(request):
    if(request.method == "POST"):
        if("uname" in request.session):
            user = UserInfo.objects.get(username = request.session["uname"])
            food = Food.objects.get(id = request.POST["food_id"])
            qty = request.POST["qty"]   
            #Before adding to cart we need to check for duplicate entry
            try:
                cart_item = Cart.objects.get(user = user,food=food)
            except:
                #Add item to cart
                cart_item = Cart()
                cart_item.user = user
                cart_item.food = food
                cart_item.qty = qty
                cart_item.save()
                return redirect(homepage)
            else:
                return HttpResponse("Item already in cart")              
        else:
            return redirect(Login)
    else:
        return redirect(Login)


def ShowAllCartItems(request):
    uname = request.session["uname"]
    user = UserInfo.objects.get(username = uname)
    if(request.method == "GET"):       
        items = Cart.objects.filter(user = user)
        cats = Category.objects.all()
        total = 0
        for item  in items:
            total += float(item.food.price) * float(item.qty)
        request.session["total"] = total
        return render(request,"ShowAllCartItems.html",{"items":items,"cats":cats})
    else:
        action = request.POST["action"]
        food_id = request.POST["food_id"]
        food = Food.objects.get(id=food_id)
        item = Cart.objects.get(user=user,food=food)
        
        if(action=="update"):
            qty = request.POST["qty"]
            item.qty = qty
            item.save()
        else:            
            item.delete()            
        return redirect(homepage)

def MakePayment(request):
    if(request.method == "GET"):
        return render(request,"MakePayment.html",{})
    else:
        card_no = request.POST["card_no"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]

        try:
            buyer = Payment.objects.get(card_no=card_no,cvv=cvv,expiry=expiry)
        except:
            return render(request,"MakePayment.html",{"msg":"Invalid card details"})
        else:
            owner = Payment.objects.get(card_no="111",cvv="111",expiry="12/2030")
            total = request.session["total"]
            buyer.balance -= total
            owner.balance += total
            buyer.save()
            owner.save()
            #Delete the cart items
            uname = request.session["uname"]
            user = UserInfo.objects.get(username = uname)
            items = Cart.objects.filter(user=user)
            for item in items:
                item.delete()
            
            return render(request,"master.html")
