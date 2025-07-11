from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from .forms import *
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required



def home(request):
    featured_items = Item.objects.filter(featured=True)
    categories = Category.objects.all()
    context = {
        "items": featured_items,
        "categories": categories,
    }
    return render(request, "home.html", context)



def about(request):
    return render(request, "about.html")



def contact(request):
    if request.method == "POST":
        firstNameInput = request.POST['firstName']
        lastNameInput = request.POST['lastName']
        emailInput = request.POST['email']
        commentInput = request.POST['comment']

        if firstNameInput and lastNameInput and emailInput and commentInput:
            Contact(
                contact_name=firstNameInput,
                contact_surname=lastNameInput,
                contact_email=emailInput,
                contact_comment=commentInput
            ).save()
            messages.success(request, "Message sent!")
        else:
            messages.error(request, "Message not sent!")
    return render(request, "contact.html")



def gallery(request):
    return render(request, "gallery.html")



def detailitem(request, id):
    try:
        itemInfos = Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise Http404("Item not found")

    context = {"itemInfos": itemInfos}
    return render(request, 'detailitem.html', context)



def categoryPage(request, slug):
    try:
        category_Detail = Category.objects.get(category_slug=slug)
    except Category.DoesNotExist:
        raise Http404("Category not found")

    categoryItems = Item.objects.filter(item_category=category_Detail, featured=False)
    paginator = Paginator(categoryItems, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "categoryDetail": category_Detail,
        "page_obj": page_obj,
    }
    return render(request, "categoryPage.html", context)



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



def loginA(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)



def logoutT(request):
    logout(request)
    return redirect('login')



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

    form = CheckoutForm()  

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
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



def search_view(request):
    query = request.GET.get('q', '')
    if query:
        search_results = Item.objects.filter(item_name__icontains=query)
    else:
        search_results = Item.objects.none()
    return render(request, 'search_results.html', {
        'search_results': search_results,
        'query': query,
    })




def checkout_view(request):
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

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            if not cart_items:
                messages.error(request, "Your cart is empty.")
                return redirect('cart')

            
            order = Order.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                payment_method=form.cleaned_data['payment_method'],
                total_price=total_price
            )

           
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    item_name=cart_item['item'].item_name,
                    quantity=cart_item['quantity'],
                    price=cart_item['item'].item_price
                )

            
            request.session['cart'] = {}
            messages.success(request, "Order placed successfully!")
            return redirect('checkout_success')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CheckoutForm()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
    }
    return render(request, 'checkout.html', context)




def checkout_success(request):
    return render(request, 'checkout_success.html')
