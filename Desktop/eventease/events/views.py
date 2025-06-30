from django.shortcuts import render
from .models import Event

def event_list(request):
    '''events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})'''
    category = request.GET.get('category')
    if category:
        events = Event.objects.filter(category=category)
    else:
        events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

from django.shortcuts import redirect

'''def add_to_cart(request, event_id):
    #event = Event.objects.get(id=event_id)
    cart = request.session.get('cart',{})
    #event_id = str(event_id)
    event_id = int(event_id)
    if event_id in cart:
        cart[event_id] += 1
    else:
        cart[event_id] = 1
    #cart.append(event_id)
    request.session['cart'] =cart
    return redirect('event_list')
'''


def add_to_cart(request, event_id):
    cart = request.session.get('cart', {})
    if isinstance(cart, list):
        new_cart = {}
        for e_id in cart:
            e_id = str(e_id)
            new_cart[e_id] = new_cart.get(e_id, 0) + 1
        cart = new_cart

    event_id = str(event_id)
    if event_id in cart:
        cart[event_id] += 1
    else:
        cart[event_id] = 1

    request.session['cart'] = cart
    return redirect('event_list')


'''def view_cart(request):
    cart = request.session.get('cart', {})
    event_ids=[int(event_id) for event_id in cart.keys()]
    events_in_cart = Event.objects.filter(id__in=event_ids)
    #events_in_cart = Event.objects.filter(id__in=cart.keys()) this is for a list not a dictionary
    return render(request, 'events/view_cart.html', {'events': events_in_cart, 'cart':cart})
'''


def view_cart(request):
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {str(e_id): 1 for e_id in cart}
        request.session['cart'] = cart

    event_ids = [int(event_id) for event_id in cart.keys()]
    events_in_cart = Event.objects.filter(id__in=event_ids)
    return render(request, 'events/view_cart.html', {'events': events_in_cart, 'cart': cart})



def remove_from_cart(request, event_id):
    cart = request.session.get('cart', {})
    event_id = str(event_id)
    if event_id in cart:
        del cart[event_id]
    request.session['cart'] = cart
    return redirect('view_cart')

def update_quantity(request, event_id, action):
    cart = request.session.get('cart', {})
    event_id = str(event_id)

    if event_id in cart:
        if action == 'add':
            cart[event_id] +=1
        elif action == 'subtract':
            cart[event_id] -= 1
            if cart[event_id] <= 0:
                del cart[event_id]

    request.session['cart'] = cart
    return redirect('view_cart')

def checkout(request):
    cart = request.session.get('cart', {})
    if isinstance(cart, list):
        cart = {str(e_id): 1 for e_id in cart}
        request.session['cart'] = cart

    event_ids = [int(event_id) for event_id in cart.keys()]
    events_in_cart = Event.objects.filter(id__in=event_ids)

    total = 0
    for event in events_in_cart:
        quantity = cart.get(str(event.id), 0)
        total += event.price * quantity

    return render(request, 'events/checkout.html', {
        'events': events_in_cart,
        'cart': cart,
        'total': total
    })

from django.http import HttpResponse

'''def confirm_booking(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        request.session['cart'] = {} # this clears the cart
        return HttpResponse(f"<h2>Booking Confirmed via {payment_method}! Your Tickets have been booked.</h2> <a href='/'>Back to Events</a>")
    else:
        return redirect('event_list')
'''
def confirm_booking(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        mpesa_number = request.POST.get('mpesa_number')
        card_number = request.POST.get('card_number')

        if not payment_method:
            return HttpResponse("<h3>Please select a payment method.</h3><a href='/checkout/'>Back to Checkout</a>")

        if payment_method == 'Mpesa' and not mpesa_number:
            return HttpResponse("<h3>Please enter your Mpesa number.</h3><a href='/checkout/'>Back to Checkout</a>")

        if payment_method == 'Card' and not card_number:
            return HttpResponse("<h3>Please enter your Card number.</h3><a href='/checkout/'>Back to Checkout</a>")

        # Clear cart after confirmation
        request.session['cart'] = {}

        return HttpResponse(f"<h2>Booking Confirmed via {payment_method}!</h2><a href='/'>Back to Events</a>")

    else:
        return redirect('event_list')

from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User registered in successfully")
            login(request, user)
            print("User logged in successfully")
            messages.success(request, f'Account created for {user.username}!')
            return redirect('event_list')
    else:
        form = UserRegisterForm()
    return render(request, 'events/register.html', {'form': form})
