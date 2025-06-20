from django.shortcuts import render
from .models import*
from django.contrib import messages

# Create your views here.
def home(request):
    #te gjithe infot qe ka nje model
    #nga databaza tek view por ende ska kaluar tek html
    items = Item.objects.all() #nese perdoret all tek views tek html perdoret zakonisht for in
    #nga view tek html
    context = {"items":items}
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