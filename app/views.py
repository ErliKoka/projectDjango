from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import*
from django.contrib import messages
from.forms import*

# Create your views here.
def home(request):
    #te gjithe infot qe ka nje model
    #nga databaza tek view por ende ska kaluar tek html
    items = Item.objects.all() #nese perdoret all tek views tek html perdoret zakonisht for in
    #nga view tek html
    #marr info per category
    categories = Category.objects.all()
    context = {
        "items":items,
        "categories":categories,
        }
    return render(request, "home.html", context)

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        #marrja e infos nga inputet
        #variabelcfaredo = request.POST['vlera e name tek input']
        firstNameInput = request.POST['firstName']
        lastNameInput = request.POST['lastName']
        emailInput = request.POST['email']
        commentInput = request.POST['comment']

        if firstNameInput != "" and lastNameInput !="" and emailInput != "" and commentInput !="" :
           Contact(
            contact_name=firstNameInput,
            contact_surname=lastNameInput,
            contact_email=emailInput,
            contact_comment=commentInput
            ).save()
           messages.success(request, "Messsage send!")
        else:
            messages.error(request, "Message not send!")
    return render(request, "contact.html")
    
def gallery(request):
    return render(request, "gallery.html")

def detailitem(request, id):
    #Marr info vetem per nje element
    #behet dallimi ndermjet elementeve nga id (primary key)
    itemInfos = Item.objects.get(pk=id)
    context = {"itemInfos":itemInfos}
    return render(request, 'detailitem.html', context)

def categoryPage(request, slug):
    category_Detail = Category.objects.get(category_slug=slug)
    #item_category eshte tek modeli Item 
    #categoryDetail eshte emri i variablit ku este ruajtur info per categorine
    categoryItems = Item.objects.filter(item_category=category_Detail)
    context = {"categoryDetail": category_Detail,
               "categoryItems": categoryItems}
    return render(request, "categoryPage.html", context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
            form = RegisterForm()
    return render(request, 'register.html',{'form':form})


def loginA(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'login.html', context)

def logoutT(request):
    logout(request)
    return redirect('login')
