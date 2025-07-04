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


# --- Cart Views ---

def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))

        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            messages.error(request, "Item not found.")
            return redirect('home')

        cart = request.session.get('cart', {})

        if item_id in cart:
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity

        request.session['cart'] = cart
        messages.success(request, f"Added {quantity} x {item.item_name} to your cart.")
        return redirect('detailitemPage', id=item_id)

    return redirect('home')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for item_id, quantity in cart.items():
        try:
            item = Item.objects.get(pk=item_id)
            subtotal = item.item_price * quantity
            total_price += subtotal
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Item.DoesNotExist:
            pass

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


def update_cart(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})

        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                item_id = key.replace('quantity_', '')
                try:
                    quantity = int(value)
                    if quantity < 1:
                        quantity = 1
                except ValueError:
                    quantity = 1

                if item_id in cart:
                    cart[item_id] = quantity

        request.session['cart'] = cart
        messages.success(request, "Cart updated successfully.")
        return redirect('cart')

    return redirect('cart')


def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if not item_id:
            messages.error(request, "No item specified to remove.")
            return redirect('cart')

        cart = request.session.get('cart', {})
        if item_id in cart:
            del cart[item_id]
            request.session['cart'] = cart
            messages.success(request, "Item removed from cart.")
        else:
            messages.error(request, "Item not found in cart.")

    return redirect('cart')


