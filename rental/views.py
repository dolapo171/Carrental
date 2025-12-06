from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Car
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from .models import Booking
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth import logout





def home(request):
    category = request.GET.get('category')
    if category:
        cars = Car.objects.filter(category=category)
    else:
        cars = Car.objects.all()
    return render(request, 'rental/home.html', {'cars': cars, 'selected_category': category})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'rental/login.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'rental/signup.html', {'form': form})

@login_required
def car_list(request):
    cars = Car.objects.all()  
    return render(request, 'rental/car_list.html', {'cars': cars})

def register_view(request):
    return render(request, 'rental/register.html')
 
def category_view(request, category_name):
    print("Original category:", category_name)
    
    # Normalize input
    if category_name.lower().endswith('s'):
        category_name = category_name[:-1]  
    
    print("Normalized category:", category_name)

    cars = Car.objects.filter(category__iexact=category_name)
    return render(request, 'rental/category.html', {
        'cars': cars,
        'category': category_name
    })

class StyledUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        rental_date_str = request.POST.get('rental_date')
        end_date_str = request.POST.get('end_date')

        try:
            rental_date = datetime.strptime(rental_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('book_car', car_id=car.id)

        if rental_date >= end_date:
            messages.error(request, "End date must be after rental date.")
            return redirect('book_car', car_id=car.id)

        Booking.objects.create(
            user=request.user,
            car=car,
            rental_date=rental_date,
            end_date=end_date
        )
        messages.success(request, f'You have successfully booked {car.name} from {rental_date} to {end_date}.')
        return redirect('booking_success')

    
    return render(request, 'rental/book_car.html', {'car': car})


def booking_success(request):
    return render(request, 'rental/booking_success.html')

def logout_view(request):
    logout(request)
    return redirect('home')


    
